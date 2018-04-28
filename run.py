import dis
import main


def run(f):

    def nameg(name):
        if isinstance(name, tuple) or isinstance(name, list):
            cos = str(list(name))[1:-1]
            return "{%s}" % cos
        if name is None:
            return 'nil'
        if str(name).isnumeric():
            return name
        return '"%s"' % name
    btc = f.co_code
    cs = f.co_consts
    # vn = f.co_varnames
    con = f.co_names
    dis.disassemble(f)
    # print(cs, vn, con)
    # hold = {
    #     'vn': {},
    #     'globals': {
    #         'print': print,
    #         'int': int
    #     }
    # }
    ret = '--lua'
    ret += '\n'
    ret += 'bool_int = {[true]=1, [false]=0}'
    ret += '\n'
    ret += 'bool_invert = {[true]=0, [false]=1}'
    ret += '\n'
    ret += 'py_unpack = unpack or table.unpack'
    ret += '\n'
    ret += 'len = function (x) return #x end'
    # ret += 'bool_not = {[true]=0. [false]=1}'
    ret += '\n'
    ret += 'consts = {}'
    ret += '\n'
    for pl, i in enumerate(cs):
        ret += 'consts[%s] = %s' % (pl, nameg(i))
        ret += '\n'
    # print(nameg(con))
    ret += 'globals = {}'
    gpl = 1
    for i in con:
        ret += '\n'
        ret += 'globals[%s] = %s' % (gpl, i)
        gpl += 1
    ret += '\n'
    ret += 'stack = {}\n'
    ret += 'names = {}'
    ret += '\n'
    ret += 'sp = 0'
    loops = []
    pl = 0
    while pl+2 < len(btc):
        ret += '\n'
        op, a, b = btc[pl:pl+3]
        name = dis.opname[op]
        print(name)
        # ret += 'print(sp, stack[sp])\n'
        ret += '::_%s::\n' % pl
        if name == 'LOAD_CONST':
            ret += 'sp = sp + 1'
            ret += '\n'
            ret += 'stack[sp] = consts[%s]' % a
        elif name == 'STORE_FAST':
            ret += 'names[%s] = stack[sp]' % a
            ret += '\n'
            ret += 'sp = sp - 1'
        elif name == 'LOAD_FAST':
            ret += 'sp = sp + 1\n'
            ret += 'stack[sp] = names[%s]' % a
            ret += '\n'
        elif name == 'LOAD_GLOBAL':
            ret += 'sp = sp + 1'
            ret += '\n'
            # ret += 'print("    ", sp  , globals[%s])' % (a+1)
            ret += 'stack[sp] = globals[%s]' % (a+1)
        elif name == 'CALL_FUNCTION':
            ret += 'args = {}'
            ret += '\n'
            ret += 'ap = 0'
            for i in range(a):
                ret += '\n'
                ret += 'ap = ap + 1'
                ret += '\n'
                ret += 'args[ap] = stack[sp]'
                ret += '\n'
                ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'fn = stack[sp]\n'
            ret += 'stack[sp] = fn(py_unpack(args))'
            ret += '\n'
        elif name == 'POP_TOP':
            ret += 'sp = sp - 1'
            pl -= 2
        elif name == 'BINARY_ADD':
            ret += '\n'
            ret += 'op_pre = stack[sp-1]'
            ret += '\n'
            ret += 'op_post = stack[sp]'
            ret += '\n'
            ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'if type(op_pre) == "number" then'
            ret += '\n'
            ret += '  stack[sp] = op_pre + op_post'
            ret += '\n'
            ret += 'else'
            ret += '\n'
            ret += '  stack[sp] = op_pre .. op_post'
            ret += '\n'
            ret += 'end'
            pl -= 2
        elif name == 'BINARY_SUBTRACT':
            ret += '\n'
            ret += 'op_pre = stack[sp-1]'
            ret += '\n'
            ret += 'op_post = stack[sp]'
            ret += '\n'
            ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'stack[sp] = op_pre - op_post'
            pl -= 2
        elif name == 'INPLACE_ADD':
            ret += '\n'
            ret += 'op_pre = stack[sp-1]'
            ret += '\n'
            ret += 'op_post = stack[sp]'
            ret += '\n'
            ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'if type(op_pre) == "number" then'
            ret += '\n'
            ret += '  stack[sp] = op_pre + op_post'
            ret += '\n'
            ret += 'else'
            ret += '\n'
            ret += '  stack[sp] = op_pre .. op_post'
            ret += '\n'
            ret += 'end'
            pl -= 2
        elif name == 'INPLACE_SUBTRACT':
            ret += '\n'
            ret += 'op_pre = stack[sp-1]'
            ret += '\n'
            ret += 'op_post = stack[sp]'
            ret += '\n'
            ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'stack[sp] = op_pre - op_post'
            pl -= 2
        elif name == 'COMPARE_OP':
            ret += '\n'
            ret += 'op_pre = stack[sp-1]'
            ret += '\n'
            ret += 'op_post = stack[sp]'
            ret += '\n'
            ret += 'sp = sp - 1'
            ret += '\n'
            ret += 'stack[sp] = bool_int[op_pre %s op_post]' % dis.cmp_op[a]
        elif name == 'POP_JUMP_IF_FALSE':
            # ret += 'print(stack[sp])'
            # ret += 'print(stack[sp] == 0)\n'
            ret += 'if stack[sp] == 0 then goto _%s end\n' % a
            ret += 'sp = sp - 1'
        elif name == 'BUILD_LIST':
            ret += 'args = {}'
            ret += '\n'
            ret += 'ap = 0'
            for i in range(a):
                ret += '\n'
                ret += 'ap = ap + 1'
                ret += '\n'
                ret += 'args[ap] = stack[sp]'
                ret += '\n'
                ret += 'sp = sp - 1'
            ret += 'stack[sp] = args'
            ret += '\n'
        elif name == 'SETUP_LOOP':
            loops.append(a+pl+3)
        elif name == 'BREAK_LOOP':
            *loops, goto = loops
            ret += 'goto _%s' % goto
            pl -= 2
        elif name == 'JUMP_ABSOLUTE':
            # ret += 'print(%s)' % a
            ret += 'goto _%s \n' % a
        elif name == 'JUMP_FORWARD':
            ret += 'goto _%s \n' % (a+pl+2)
        elif name == 'SETUP_LOOP':
            pass
        elif name == 'POP_BLOCK':
            pl -= 2
        else:
            print(name)
        # if name == 'LOAD_CONST':
        #     stack.append(cs[a])
        # elif name == 'STORE_FAST':
        #     hold['vn'][vn[a]] = stack[-1]
        #     stack = stack[:-1]
        # elif name == 'LOAD_FAST':
        #     stack.append(hold['vn'][vn[a]])
        # elif name == 'BINARY_ADD':
        #     holdstack = stack[-2] + stack[-1]
        #     stack = stack[:-2]
        #     stack.append(holdstack)
        #     pl -= 2
        # elif name == 'BUILD_LIST':
        #     stack = stack[:-a] + [stack[-a:]]
        # elif name == 'LOAD_GLOBAL':
        #     stack.append(hold['globals'][con[a]])
        # elif name == 'CALL_FUNCTION':
        #     args = stack[-a:]
        #     stack = stack[:-a]
        #     fn = stack[-1]
        #     stack = stack[:-1]
        #     stack.append(fn(*args))
        # elif name == 'POP_TOP':
        #     stack = stack[:-1]
        #     pl -= 2
        # else:
        #     print(name)
        #     exit()
        pl += 3
    op = btc[pl]
    name = dis.opname[op]
    return ret

open('main.lua', 'w').write(run(main.main.__code__))
