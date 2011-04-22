# Sample python script, to be run by our gcc plugin (see "make test")
#print "hello world"

import gcc

#import sys
#print 'sys.path:', sys.path
#help(gcc)

def my_pass_execution_callback(*args, **kwargs):
    print('my_pass_execution_callback was called: args=%r  kwargs=%r' % (args, kwargs))
    #help(args[0])
    (optpass, fun) = args
    print 'optpass: %r' % optpass
    print 'fun: %r' % fun
    if fun:
        print 'fun.cfg: %r' % fun.cfg
        if fun.cfg:
            print help(fun.cfg)

def my_pre_genericize_callback(*args, **kwargs):
    print('my_pre_genericize_callback was called: args=%r  kwargs=%r' % (args, kwargs))
    #help(args[0])
    t = args[0]
    print(t)
    print(dir(t))
    print(type(t))
    print(repr(t))
    print(str(t))
    print(help(t))

    print 't.name: %r' % t.name
    print 't.addr: %s' % hex(t.addr)
    print 't.type: %r' % t.type
    print 't.function: %r' % t.function
    print help(t.function)

    print 't.type.type: %r' % t.type.type

    loc = t.location

    print(loc)
    print(dir(loc))
    print(type(loc))
    print(repr(loc))
    #print(help(loc))
    print 'loc.file: %r' % loc.file
    print 'loc.line: %r' % loc.line

    # raise RuntimeError('what happens if we get an error here?')


gcc.register_callback(gcc.PLUGIN_PASS_EXECUTION,
                      my_pass_execution_callback)
gcc.register_callback(gcc.PLUGIN_PRE_GENERICIZE,
                      my_pre_genericize_callback)

# Try some insane values:
#gcc.register_callback(-1, my_callback)

# Stupid hack idea: a UI for gcc:
#import gtk
#w = gtk.Window(gtk.WINDOW_TOPLEVEL)
#w.show()
#gtk.main()

#from pprint import pprint
#pprint(tree.subclass_for_code)
