import os
import sys

def run():
    sys.stdout.flush()
    print '\'windows\' will convert files to work with a windows system'
    print 'assumes you have the windows_display.py file in the directory'
    print 'note this time around, the script is hacky and allows you to use whatever script you would use on linux'
    print '\'revert\' will convert files back to normal linux use'
    print
    print 'Now choose either: windows or revert'
    sys.stdout.flush()
    choice = raw_input()
    if (choice == "windows" or choice == "revert"):
        if (choice == "windows"):
            os.rename('display.py', 'revert_display.py')
            os.rename('windows_display.py', 'display.py')
        elif (choice == "revert"):
            os.rename('display.py', 'windows_display.py')
            os.rename('revert_display.py', 'display.py')
    else:
        print
        print 'Invalid choice'
    
run()
