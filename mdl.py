import lex, yacc

tokens = (
    "STRING",
    "ID",
    "XYZ",
    "DOUBLE",
    "INT",
    "COMMENT",
    "LIGHT",
    "CONSTANTS",
    "SAVE_COORDS",
    "CAMERA",
    "AMBIENT",
    "TORUS",
    "SPHERE",
    "BOX", 
    "LINE", 
    "MESH", 
    "TEXTURE", 
    "SET", 
    "MOVE", 
    "SCALE", 
    "ROTATE", 
    "BASENAME", 
    "SAVE_KNOBS", 
    "TWEEN", 
    "FRAMES", 
    "VARY", 
    "PUSH", 
    "POP", 
    "SAVE", 
    "GENERATE_RAYFILES", 
    "SHADING", 
    "SHADING_TYPE", 
    "SET_KNOBS", 
    "FOCAL", 
    "DISPLAY", 
    "SCREEN", 
    "WEB", 
    "CO"
)

reserved = {
    "x" : "XYZ", 
    "y" : "XYZ", 
    "z" : "XYZ", 
    "screen" : "SCREEN", 
    "light" : "LIGHT",
    "constants" : "CONSTANTS",
    "save_coord_system" : "SAVE_COORDS", 
    "camera" : "CAMERA",
    "ambient" : "AMBIENT",
    "torus" : "TORUS",
    "sphere" : "SPHERE",
    "box" : "BOX",
    "line" : "LINE",
    "mesh" : "MESH",
    "texture" : "TEXTURE",
    "set" : "SET",
    "move" : "MOVE",
    "scale" : "SCALE",
    "rotate" : "ROTATE",
    "basename" : "BASENAME",
    "save_knobs" : "SAVE_KNOBS",
    "tween" : "TWEEN",
    "frames" : "FRAMES",
    "vary" : "VARY",
    "push" : "PUSH",
    "pop" : "POP",
    "save" : "SAVE",
    "generate_rayfiles" : "GENERATE_RAYFILES",
    "shading" : "SHADING",
    "phong" : "SHADING_TYPE",
    "flat" : "SHADING_TYPE",
    "gouraud" : "SHADING_TYPE",
    "raytrace" : "SHADING_TYPE",
    "wireframe" : "SHADING_TYPE",
    "setknobs" : "SET_KNOBS",
    "focal" : "FOCAL",
    "display" : "DISPLAY",
    "web" : "WEB"
}

t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if reserved.has_key(t.value):
        t.type = reserved.get(t.value)
    return t

def t_STRING(t):
    r'\.[a-zA-Z_0-9]*[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_DOUBLE(t):
    r"""\-?\d+\.\d*|\-?\.\d+ |
        \-?\d+"""
    t.value = float(t.value)
    return t

def t_COMMENT(t):
    r"//.*"
    return t

def t_CO(t):
    r":"
    return t

def t_error(t):
    print "TOKEN ERROR: " + str(t)

lex.lex()

#----------------------------------------------------------

commands = []
symbols = {}

def p_input(p):
    """input :
            | command input"""
    pass

def p_command_comment(p):
    'command : COMMENT'
    pass

def p_SYMBOL(p):
    """SYMBOL : XYZ
              | ID"""
    p[0] = p[1]

def p_TEXT(p):
    """TEXT : SYMBOL
            | STRING"""
    p[0] = p[1]

def p_NUMBER(p):
    """NUMBER : DOUBLE"""
    p[0] = p[1]

def p_command_stack(p):
    """command : POP
                 | PUSH"""
    commands.append({'op' : p[1], 'args' : None})

def p_command_screen(p):
    """command : SCREEN NUMBER NUMBER
                 | SCREEN"""
    if len(p) == 2:
        commands.append({'op' : p[1], 'width' : 500, 'height': 500})
    else:
        commands.append({'op' : p[1], 'width' : p[2], 'height': p[3]})

def p_command_save(p):
    """command : SAVE TEXT TEXT"""
    commands.append({'op' : p[1], 'args' : [p[2]]})

def p_command_show(p):
    """command : DISPLAY"""
    commands.append({'op' : p[1], 'args' : None})

def p_command_sphere(p):
    """command : SPHERE NUMBER NUMBER NUMBER NUMBER
               | SPHERE SYMBOL NUMBER NUMBER NUMBER NUMBER
               | SPHERE NUMBER NUMBER NUMBER NUMBER SYMBOL
               | SPHERE SYMBOL NUMBER NUMBER NUMBER NUMBER SYMBOL"""
    cmd = {'op' : p[1], 'constants' : None, 'cs' : None, 'args':[]}
    arg_start = 2
    if isinstance(p[2], str):
        cmd['constants'] = p[2]
        arg_start = 3
    if len(p) == 7 and isinstance(p[6], str):
        cmd['cs'] = p[6]
    if len(p) == 8 and isinstance(p[7], str):
          cmd['cs'] = p[7]
    cmd['args'] = p[arg_start:arg_start+4]
    commands.append(cmd)

def p_command_torus(p):
    """command : TORUS NUMBER NUMBER NUMBER NUMBER NUMBER
               | TORUS NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL
               | TORUS SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER
               | TORUS SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL"""
    cmd = {'op' : p[1], 'constants' : None, 'cs' : None, 'args':[]}
    arg_start = 2
    if isinstance(p[2], str):
        cmd['constants'] = p[2]
        arg_start = 3
    if len(p) == 8 and isinstance(p[7], str):
        cmd['cs'] = p[7]
    if len(p) == 9 and isinstance(p[8], str):
          cmd['cs'] = p[8]
    cmd['args'] = p[arg_start:arg_start+5]
    commands.append(cmd)

def p_command_box(p):
    """command : BOX NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
               | BOX NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL
               | BOX SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
               | BOX SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL"""
    cmd = {'op' : p[1], 'constants' : None, 'cs' : None, 'args':[]}
    arg_start = 2
    if isinstance(p[2], str):
        cmd['constants'] = p[2]
        arg_start = 3
    if len(p) == 9 and isinstance(p[8], str):
        cmd['cs'] = p[8]
    if len(p) == 10 and isinstance(p[9], str):
          cmd['cs'] = p[9]
    cmd['args'] = p[arg_start:arg_start+6]
    commands.append(cmd)

def p_command_line(p):
    """command : LINE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
               | LINE NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL
               | LINE NUMBER NUMBER NUMBER SYMBOL NUMBER NUMBER NUMBER
               | LINE NUMBER NUMBER NUMBER SYMBOL NUMBER NUMBER NUMBER SYMBOL
               | LINE SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
               | LINE SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER SYMBOL
               | LINE SYMBOL NUMBER NUMBER NUMBER SYMBOL NUMBER NUMBER NUMBER
               | LINE SYMBOL NUMBER NUMBER NUMBER SYMBOL NUMBER NUMBER NUMBER SYMBOL"""
    cmd = {'op' : p[1], 'constants' : None, 'cs0' : None, 'cs1' : None, 'args':[]}
    arg_start = 2
    if isinstance(p[2], str):
        cmd['constants'] = p[2]
        arg_start = 3
    cmd['args'] = p[arg_start:arg_start+3]
    arg_start = arg_start+3
    if isinstance(p[arg_start], str):
        cmd['cs0'] = p[arg_start]
        arg_start+= 1
    cmd['args']+= p[arg_start:arg_start+3]
    if len(p) == 9 and isinstance(p[8], str):
        cmd['cs1'] = p[8]
    if len(p) == 10 and isinstance(p[9], str):
        cmd['cs1'] = p[9]
    if len(p) == 11 and isinstance(p[10], str):
        cmd['cs1'] = p[10]
    commands.append(cmd)

def p_command_move(p):
    """command : MOVE NUMBER NUMBER NUMBER SYMBOL
               | MOVE NUMBER NUMBER NUMBER"""
    cmd = {'op' : p[1], 'args' : p[2:5], 'knob' : None}
    if len(p) == 6:
        cmd['knob'] = p[5]
        symbols[p[5]] = ['knob', 0]
    commands.append(cmd)

def p_command_scale(p):
    """command : SCALE NUMBER NUMBER NUMBER SYMBOL
                 | SCALE NUMBER NUMBER NUMBER"""
    cmd = {'op' : p[1], 'args' : p[2:5], 'knob' : None}
    if len(p) == 6:
        cmd['knob'] = p[5]
        symbols[p[5]] = ['knob', 0]
    commands.append(cmd)

def p_command_rotate(p):
    """command : ROTATE XYZ NUMBER SYMBOL
                 | ROTATE XYZ NUMBER"""
    cmd = {'op' : p[1], 'args' : p[2:4], 'knob' : None}
    if len(p) == 5:
        cmd['knob'] = p[4]
        symbols[p[4]] = ['knob', 0]
    commands.append(cmd)

def p_command_frames(p):
    """command : FRAMES NUMBER"""
    cmd = {'op' : p[1], 'args' : [p[2]]}
    commands.append(cmd)

def p_command_basename(p):
    """command : BASENAME TEXT"""
    cmd = {'op' : p[1], 'args' : [p[2]]}
    commands.append(cmd)

def p_command_vary(p):
    """command : VARY SYMBOL NUMBER NUMBER NUMBER NUMBER"""
    cmd = {'op' : p[1], 'args' : p[3:], 'knob' : p[2]}
    symbols[p[2]] = ['knob', 0]
    commands.append(cmd)

def p_command_knobs(p):
    """command : SET SYMBOL NUMBER
               | SET_KNOBS NUMBER"""
    cmd = {'op' : p[1], 'args' : [], 'knob' : None}
    if p[1] == 'SET':
        cmd['knob'] = p[2]
        cmd['args'].append(p[3])
        symbols[p[2]] = p[3]
    else:
        cmd['args'].append(p[2])
    commands.append(cmd)

def p_command_ambient(p):
    "command : AMBIENT NUMBER NUMBER NUMBER"
    symbols['ambient'] = ['ambient'] + p[2:]
    cmd = {'op':p[1], 'args':p[2:]}
    commands.append(cmd)

def p_command_constants(p):
    """command : CONSTANTS SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
               | CONSTANTS SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"""
    symbols[p[2]] = ['constants', {'red' : p[3:6], 'green' : p[6:9], 'blue' : p[9:]}]
    cmd = {'op':p[1], 'args' : None, 'constants' : p[2] }
    commands.append(cmd)

def p_command_light(p):
    "command : LIGHT SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"
    symbols[p[2]] = ['light', {'location' : p[3:6], 'color' : p[6:]}]
    cmd = {'op':p[1], 'args' : None, 'light' : p[2] }
    commands.append(cmd)

def p_command_shading(p):
    "command : SHADING SHADING_TYPE"
    symbols['shading'] = ['shade_type', p[2]]
    cmd = {'op':p[1], 'args' : None, 'shade_type' : p[2] }
    commands.append(cmd)

def p_command_camera(p):
    "command : CAMERA NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"
    symbols['camera'] = ['camera', {'eye': p[2:4], 'aim': p[4:]} ]
    commands.append({'op':p[1], 'args':None})

def p_command_generate_rayfiles(p):
    "command : GENERATE_RAYFILES"
    commands.append({'op':p[1], 'args':None})

def p_command_mesh(p):
    """command : MESH CO TEXT
               | MESH SYMBOL CO TEXT
               | MESH CO TEXT SYMBOL
               | MESH SYMBOL CO TEXT SYMBOL"""
    cmd = {'op':p[1], 'args' : [], 'cs':None, 'constants':None}
    arg_start = 2
    if isinstance(p[2], str):
        cmd['constants'] = p[2]
        arg_start+= 1
    cmd['args'].append(p[arg_start])
    if len(p) == 4 and isinstance(p[3], str):
        cmd['cs'] = p[3]
    if len(p) == 5 and isinstance(p[4], str):
        cmd['cs'] = p[4]
    commands.append(cmd)

def p_save_knobs(p):
    "command : SAVE_KNOBS SYMBOL"
    cmd = {'op':p[1], 'args':None, 'knob_list':p[2]}
    symbols[p[2]] = ['knob_list', []]
    commands.append(cmd)

def p_save_coords(p):
    "command : SAVE_COORDS SYMBOL"
    cmd = {'op':p[1], 'args':None, 'cs':p[2]}
    symbols[p[2]] = ['coord_sys', []]
    commands.append(cmd)


def p_tween(p):
    "command : TWEEN NUMBER NUMBER SYMBOL SYMBOL"
    cmd = {'op':p[1], 'args':p[2:4], 'knob_list0':p[4], 'knob_list1':p[5]}
    commands.append(cmd)

def p_focal(p):
    "command : FOCAL NUMBER"
    commands.append({'op':p[1], 'args':[p[2]]})

def p_web(p):
    "command : WEB"
    commands.append({'op':p[1], 'args':None})

def p_texture(p):
    "command : TEXTURE SYMBOL NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER"
    symbols[p[2]] = ['texture', p[3:]]

def p_error(p):
    print 'SYNTAX ERROR: ' + str(p)

yacc.yacc()


from copy import deepcopy

def parseFile(filename):
    """
    This function returns a tuple containing a list of opcodes
    and a list of symbols.
    Every opcode is a tuple of the form
    (commandname, parameter, parameter, ...).
    Every symbol is a tuple of the form (type, name).
    """
    global commands
    global symbols
    commands = []
    symbols = {}
    try:
        f = open(filename, "r")
        for line in f.readlines():
            line = line.strip()
            yacc.parse(line)
        f.close()
        result = (commands[:], deepcopy(symbols))
        commands = []
        symbols = {}
        return result
    except IOError:
        return ()
