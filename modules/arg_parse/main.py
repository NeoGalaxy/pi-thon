"""Stupid Docstring"""
import sys

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
                text += ('\n   ' + ' '*len(opt['name'])+'\t ').join(opt['descr'])
                text += '\n'

        if self.__args != [] :
            text += 'Arguments :\n'
            for opt in self.__args:
                text += '  '+opt['name']+'\t '
                text += ('\n   ' + ' '*len(opt['name'])+'\t ').join(opt['descr'])
                text += '\n'
        return text

    def parse_arguments(self, argument_list = None) :
        """Parse the argument_list"""
        if argument_list is None:
            argument_list = sys.argv
        if argument_list is sys.argv and self.arguments is not None :
            return(self.arguments, self.options)

        def raise_error(text = ""):
            sys.stderr.write(("\u001b[31mError at argument"
                + " positition {}:\u001b[0m\n").format(i))
            sys.stderr.write(('\u001b[33;1m'+text+"\u001b[0m\n\n"))
            sys.stderr.write(self.help())
            sys.exit(1)

        arguments = self.__args
        options = self.__opts
        arg_values = {}
        opts_values = {
                o.name:o.default for o in options if o.default is not None}

        i = 1
        argindex = 0 # Index of the current argument, excluding options
        while i < len(argument_list):
            arg = argument_list[i]
            i += 1
            if arg[0] == '-':
                try:
                    opt = next(o for o in options if o.name == arg[1:])
                except StopIteration as _:
                    raise_error(f"Unknown option {arg}")

                opt_values = []
                for opt_arg in opt.args:
                    if i == len(argument_list[i]):
                        raise_error(f"Missing option value to {arg}")
                    arg = argument_list[i]
                    i += 1
                    opt_values.append(opt_arg.type(arg) if opt_arg.type else arg)

                opts_values[opt.name] = opt_values
                continue

            # if it is a normal argument
            if arguments[argindex].type is not None :
                try:
                    arg = arguments[argindex]['type'](arg)
                except ValueError as _:
                    raise_error("Wrong type for {}.".format(arguments[argindex]))
            arg_values[arguments[argindex]['name']] = arg
            argindex += 1

        indx = argindex
        while indx < len(arguments):
            if arguments[indx].required:
                raise_error('Missing argument '+ arguments[indx].name)
            if arguments[indx].default:
                arg_values[arguments[indx].name] = arguments[indx].default
            indx += 1

        return (arg_values,opts_values)
