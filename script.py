import mdl
from display import *
from matrix import *
from draw import *

import sys

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    #print "\nSTART FIRST"
    basename = None
    num_frames = None
    for command in commands:
        #print command
        c = command['op']
        args = command['args']
        #print c
        #print args
        if c == 'frames':
            num_frames = args[0]
        if (c == 'basename'):
            basename = args[0]

        if c == 'vary':
            if (not num_frames):
                print "ERROR: vary found without any frame"
                sys.exit("Exiting program")
    
    if (not (num_frames == None) and (basename == None)):
        basename = 'asdf'
        sys.stdout.flush()
        print "WARNING: basename not found, using 'asdf' as basename"
        print "WARNING: if other files with the this name exist, you done goofed"
        print "CHOOSE: 'y' to consent and continue, or any other key to exit and save yourself"
        sys.stdout.flush()
        choice = raw_input()
        sys.stdout.flush()
        if not (choice == "y"):
            sys.exit("Exiting program")
    #print "END FIRST\n"
    return (basename, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames ):
    #print "\nSTART SECOND"
    node_vary = dict([(i, None) for i in range(int(num_frames))])    

    for command in commands:
        c = command['op']
        args = command['args']
            
        if(c == 'vary'):
            knob = command['knob']
            #print args
            start_frame = args[0]
            end_frame = args[1]
            start_val = args[2]
            end_val = args[3]

            d = (end_val - start_val) / (end_frame - start_frame)

            val = start_val
            for i in range(int(start_frame), int(end_frame + 1)):
                if i == (end_frame):
                    val = end_val
                if(node_vary[i] is None):
                    node_vary[i]= {knob: val}
                else:
                    node_vary[i].update({knob: val})
                val += d
            '''
            while (frame < end_frame):
                values = round(start_val + (frame - start_frame) * d, 2)
                #if(node_vary[0] is None):
                val = {knob:values}
                if(node_vary[frame] is None):
                    node_vary[frame] = val
                else:
                    node_vary[frame].update(val)
                frame += 1
            '''
    #print node_vary
    #print "END SECOND\n"
    return node_vary


#progress bar by Rom Ruben! with a few mods
def progress(count, total, fill='#', suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = fill * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    consts = ''
    coords = []
    coords1 = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    #PASSES
    (basename, num_frames) = first_pass(commands)
    #print basename
    #print num_frames
    
    node_vary = second_pass( commands, num_frames )
    #print node_vary

    for frame in range(int(num_frames)):
        #sys.stdout.flush()
        #print ("Frame:", frame)
        #sys.stdout.flush()
        progress(frame, num_frames)
        
        for knob in node_vary[frame]:
            symbols[knob][1] = node_vary[frame][knob]

        for command in commands:
            #print command
            c = command['op']
            args = command['args']
            if not args == None:
                args = command['args'][:]

            if (not args == None) and "knob" in command and (not command["knob"] == None) and c in ["move", "scale", "rotate"]:
                knob = command["knob"]
                #print command
                for i in range(len(args)):
                    if not isinstance(args[i], basestring):
                        args[i] = args[i] * symbols[knob][1]

            if c == 'box':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[-1], str):
                    coords = args[-1]
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'sphere':
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'torus':
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'line':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[3], str):
                    coords = args[3]
                    args = args[:3] + args[4:]
                if isinstance(args[-1], str):
                    coords1 = args[-1]
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                tmp = make_translate(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                tmp = make_scale(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])

        if num_frames > 1:
            save_extension(screen, ("./anim/" + basename + ("%03d" % int(frame)) + ".png"))

        #reset variable for next frame
        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20

    progress(num_frames, num_frames)
    sys.stdout.flush()
    print
    print
    if num_frames > 1:
        make_animation(basename)
