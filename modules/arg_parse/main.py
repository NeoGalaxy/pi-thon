"""
Module for automatic command line arguments parsing, and automatic usage/help
message generation.
"""
import sys

class ArgumentError(Exception):
    """The error raised by the parsing function when an argument is invalid."""
    def __init__(self, position, text, *args, **kargs):
        self.position = position
        self.text = text
        Exception.__init__(self, *args, **kargs)

class Arg:
    """
    Parses a dict into an object describing an argument's properties.
    The values that will be used are :
      "name"(str) -> The name of the argument. Mandatory
      "description" / "descr"(str) -> The description of what the argument does.
      "type"(type) -> The type of the argument.
      "required"/"req"(bool) -> Whether the argument is required or not.
                                Defaults to True
      "default"(any) -> The default value of the argument (if required == False)
    """
    def __init__(self, **kargs):
        try:
            self.name = str(kargs['name'])
        except KeyError as err:
            raise ValueError('There is no valid name given') from err
        self.descr = [str(line) for line in
            (kargs.get('description') or kargs.get('descr') or [])]
        self.type = kargs.get('type')
        if (self.type is not None and not isinstance(self.type,type)):
            raise ValueError('When specified, the type should be a valid type.')
        self.required = kargs['required'] if 'required' in kargs else \
                        kargs['req'] if 'req' in kargs else True
        self.default = kargs.get('default')

    def __getitem__(self, key):
        if key == 'name':
            return self.name
        if key in ['descr', 'desc', 'description']:
            return self.descr
        if key == 'type':
            return self.type
        if key in ['required', 'req']:
            return self.required
        if key == 'default':
            return self.default
        return None

    def __str__(self):
        if not self.required:
            return '['+self.name+']'
        return self.name

class Opt(Arg):
    """
    Parses a dict into an object describing an option's properties.
    The option differs in the way that it can be placed anywhere in the command
    line, and its value may depend on the next arguments in the command line.
    Note that the property "req"/"required" should have no impact since the
    option is considered as non required, and will thus never throw an exception
    on parsing if not specified.

    Also, you should use 'args' instead of 'type'. It allows to specify the
    number of arguments to the option, and their respective type.
    Thus, 'args' has to be a list of Arg (or of dict that can be used to
    initialize a Arg)

    Additionally, there is value of key "effect". When specified, it should be a
    function accepting the arguments specified in "args", and is executed when
    the option of the same name is encountered. If its return value differs from
    None, it will replace the value of the options when parsed.
    """
    def __init__(self, **kargs):
        Arg.__init__(self, **kargs)
        self.args = [] if kargs.get('args') is None else \
            [x if isinstance(x, Arg) else Arg(**x) for x in kargs['args']]
        self.effect = kargs.get('effect')

    def __getitem__(self, key):
        if key == 'args':
            return self.args
        if key == 'effect':
            return self.effect
        return Arg.__getitem__(self, key)

    def __str__(self):
        return self.name + ' '.join(str(x) for x in self.args)


class Parser:
    """
    Class to parse a list of strings and interpret them as arguments.
    To define arguments and options, give to its constructor
    """
    def __init__(self, arguments=None, options=None, descr="", parse_argv=True):
        self.__descr = str(descr)
        self.__args = [] if arguments is None else \
            [x if isinstance(x, Arg) else Arg(**x) for x in arguments]
        self.__opts = [] if options is None else \
            [x if isinstance(x, Opt) else Opt(**x) for x in options]
        self.arguments = None
        self.options = None
        if parse_argv:
            (self.arguments, self.options) = self.parse_arguments()


    def help(self):
        """
        Builds a help message and returns it.
        The format of this help is the following :
        Usage : <command> [OPTIONS] <args>...

        Arguments :
            <argument_name> <argument_description>

        Options :
            <option_name> <option_description>
        """
        # Usage
        text = 'Usage : '+sys.argv[0]
        if self.__opts != []:
            text += " [OPTIONS]" + ''.join(f' {arg}' for arg in self.__args)
        if self.__descr != '' :
            text += f'\n{self.__descr}'
        text += '\n\n'
        # Arguments
        if self.__args != [] :
            text += 'Arguments :\n'
            for arg in self.__args:
                text += f"  {arg.name}\t " \
                    + ('\n   ' + ' '*len(arg.name)+'\t   ').join(arg.descr) \
                    + '\n'
            text += '\n'
        # Options
        if self.__opts != [] :
            text += 'Options :\n'
            for opt in self.__opts:
                profile = f'  -{opt.name}{"".join(f" <{a.name}>" for a in opt.args)}'
                text += profile+'\t ' \
                    + ('\n   ' + ' '*len(profile)+'\t   ').join(opt.descr) \
                    + '\n'
            text += '\n'
        return text

    def __parse_opt(self, opt_name, i, arglist, opts_values):
        try:
            opt = next(o for o in self.__opts if o.name == opt_name)
        except StopIteration as err:
            raise ArgumentError(i, f"Unknown option {opt_name}") from err

        opt_argv = []
        for opt_arg in opt.args:
            if i == len(arglist[i]):
                raise ArgumentError(i, f"Missing option value to {arg}")
            arg = arglist[i]
            i += 1
            opt_argv.append(opt_arg.type(arg) if opt_arg.type else arg)
        if opt.effect is not None:
            ret = opt.effect(*opt_argv)
            if ret is not None:
                opt_argv = ret
        opts_values[opt.name] = opt_argv
        return i

    def parse_arguments(self, argument_list = None):
        """
        Parse argument_list into a tuple of an argument dict
        and an option dict. If the argument/option is specified
        or has a default value, it will be present in the corresponding
        dict with its name as key. If an option has "effect" specified, its
        value in the dict will instead be the return value of "effect"
        (if not None).
        """
        if argument_list is None:
            argument_list = sys.argv

        arguments = self.__args
        options = self.__opts
        arg_values = {}
        opts_values = {o.name : list.copy(o.default)
                       for o in options
                       if o.default is not None}

        i = 1
        argindex = 0 # Index of the current argument, excluding options
        try:
            while i < len(argument_list):
                arg = argument_list[i]
                i += 1 # Permet de modifier i dans le parse des options

                if arg[0] == '-':
                    i = self.__parse_opt(arg[1:], i, argument_list, opts_values)
                    continue

                if argindex >= len(arguments):
                    raise ArgumentError(i,
                        f"Too many arguments : don't know what to do of {arg}")
                #self.__parse_arg(arg, i, arguments[argindex], arg_values)
                if arguments[argindex].type is not None :
                    try:
                        arg = arguments[argindex].type(arg)
                    except Exception as err:
                        raise ArgumentError(i, f"Wrong type for {arguments[argindex]}.") from err
                arg_values[arguments[argindex].name] = arg
                argindex += 1
            for arg_props in arguments[argindex:]:
                if arg_props.required:
                    raise ArgumentError(i, f'Missing argument {arg_props.name}')
                if arg_props.default:
                    arg_values[arg_props.name] = arg_props.default
        except ArgumentError as error:
            if error.position == 0:
                print(self.help())
                sys.exit(0)
            else:
                sys.stderr.write("\u001b[31mError at argument"
                                f" position {error.position}:\u001b[0m\n")
                sys.stderr.write((f"\u001b[33;1m{error.text}\u001b[0m\n\n"))
                sys.stderr.write(self.help())
                sys.exit(1)

        return (arg_values,opts_values)

def disp_help():
    """When called within an arg parsing, results in displaying the help"""
    raise ArgumentError(0,'')
