"""Stupid Docstring"""
import sys

class ArgumentError(ValueError):
    """The error raised when an argument is invalid"""

class Arg:
    """Argument definition parser"""
    def __init__(self, **kargs):
        try:
            self.name = str(kargs['name'])
        except KeyError as err:
            raise ValueError('There is no valid name given') from err
        self.desc = [str(line) for line in
            (kargs.get('description') or kargs.get('descr') or [])]
        self.type = kargs.get('type')
        if (self.type is not None and not isinstance(self.type,type)):
            raise ValueError('When specified, the type should be a vaild type.')
        self.required = kargs['required'] if 'required' in kargs else \
                        kargs['req'] if 'req' in kargs else True
        self.default = kargs.get('default')

    def __getitem__(self, key):
        if key == 'name':
            return self.name
        if key in ['descr', 'desc', 'description']:
            return self.desc
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
    """Option definition parser"""
    def __init__(self, **kargs):
        Arg.__init__(self, **kargs)
        try:
            self.nbr = int(kargs.get('nb') or 0)
        except TypeError as err:
            raise ValueError('The option argument number should be a int') from err
        self.args = [] if kargs.get('args') is None else \
            [x if isinstance(x, Arg) else Arg(**x) for x in kargs['args']]

    def __getitem__(self, key):
        if key == 'args':
            return self.args
        return Arg.__getitem__(self, key)

    def __str__(self):
        return self.name + ' '.join(str(x) for x in self.args)


class Parser:
    """Parse and manege command-line arguments"""
    def __init__(self, arguments = None, options = None, descr = ""):
        self.__descr = str(descr)
        self.__args = [] if arguments is None else \
            [x if isinstance(x, Arg) else Arg(**x) for x in arguments]
        self.__opts = [] if options is None else \
            [x if isinstance(x, Opt) else Opt(**x) for x in options]
        self.arguments = None
        self.options = None
        (self.arguments, self.options) = self.parse_arguments()


    def help(self):
        """Returns the help of the command"""
        text = 'Usage : '+sys.argv[0]
        if self.__opts != []:
            text += " [OPTIONS]"
        for opt in self.__args :
            text += ' ' + str(opt)
        if self.__descr != '' :
            text += '\n' + self.__descr
        text += '\n\n'
        if self.__opts != [] :
            text += 'Options :\n'
            for opt in self.__opts:
                text += '  -'+opt.name+'\t '
                text += ('\n   ' + ' '*len(opt['name'])+'\t   ').join(opt['descr'])
                text += '\n'
            text += '\n'

        if self.__args != [] :
            text += 'Arguments :\n'
            for opt in self.__args:
                text += '  '+opt['name']+'\t '
                text += ('\n   ' + ' '*len(opt['name'])+'\t   ').join(opt['descr'])
                text += '\n'
            text += '\n'
        return text

    def __mk_error(self, position, text = ""):
        sys.stderr.write("\u001b[31mError at argument"
            + f" position {position}:\u001b[0m\n")
        sys.stderr.write(('\u001b[33;1m'+text+"\u001b[0m\n\n"))
        sys.stderr.write(self.help())
        return ArgumentError(text)

    def parse_one_opt(self, opt_name, i, arglist, opts_values):
        try:
            opt = next(o for o in self.__opts if o.name == opt_name)
        except StopIteration as _:
            raise self.__mk_error(i, f"Unknown option {opt_name}")

        opt_values = []
        for opt_arg in opt.args:
            if i == len(arglist[i]):
                raise self.__mk_error(i,
                    f"Missing option value to {arg}")
            arg = arglist[i]
            i += 1
            opt_values.append(opt_arg.type(arg) if opt_arg.type else arg)

        opts_values[opt.name] = opt_values
        return i

    def parse_one_arg(self, arg_value, i, arg_props, arg_values):
        if arg_props.type is not None :
            try:
                arg_value = arg_props.type(arg_value)
            except Exception as err:
                raise self.__mk_error(i,
                    f"Wrong type for {arg_props}.") from err
        arg_values[arg_props.name] = arg_value

    def parse_arguments(self, argument_list = None):
        """Parse the argument_list"""
        if argument_list is None:
            argument_list = sys.argv
        if argument_list is sys.argv and self.arguments is not None :
            return(self.arguments, self.options)

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
                    i = self.parse_one_opt(arg[1:], i, argument_list, opts_values)
                    continue

                if argindex >= len(arguments):
                    raise self.__mk_error(i,
                        f"Too many arguments : don't know what to do of {arg}")
                self.parse_one_arg(arg, i, arguments[argindex], arg_values)
                argindex += 1
            for arg_props in arguments[argindex:]:
                if arg_props.required:
                    raise self.__mk_error(i, f'Missing argument {arg_props.name}')
                if arg_props.default:
                    arg_values[arg_props.name] = arg_props.default
        except ArgumentError:
            sys.exit(1)

        return (arg_values,opts_values)
