from . import command

def run(options, args):
    if len(args) == 0:
        raise Exception('missing command')

    cmd = args[0]

    if not cmd in command.cmd:
        raise Exception('invalid command')
    else:
        nargs = int(command.cmd[cmd]['args'])
           
        if nargs != len(args) - 1:
            raise Exception('wrong number of arguments (expected %i)' % nargs)
        else:
            command.cmd[cmd]['exec'](options, *args[1:])

