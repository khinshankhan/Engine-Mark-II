from script import run
import sys

if len(sys.argv) == 2:
    print sys.argv[1]
    if sys.argv[1].startswith( 'input/' ):
        run(sys.argv[1])
    else:
        run('input/' + sys.argv[1])
elif len(sys.argv) == 1:
    run(raw_input("please enter the filename of an mdl script file: \n"))
else:
    print "Too many arguments."
