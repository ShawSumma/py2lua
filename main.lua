--lua
bool_int = {[true]=1, [false]=0}
bool_invert = {[true]=0, [false]=1}
py_unpack = unpack or table.unpack
len = function (x) return #x end
consts = {}
consts[0] = nil
consts[1] = "<code object <listcomp> at 0x1039425d0, file "/Users/shawsumma/Desktop/code/mar-18/py2lua/main.py", line 2>"
consts[2] = "main.<locals>.<listcomp>"
consts[3] = 10
globals = {}
globals[1] = range
stack = {}
names = {}
sp = 0
::_0::
sp = sp + 1
stack[sp] = consts[1]
::_3::
sp = sp + 1
stack[sp] = consts[2]
::_6::

::_9::
sp = sp + 1
stack[sp] = globals[1]
::_12::
sp = sp + 1
stack[sp] = consts[3]
::_15::
args = {}
ap = 0
ap = ap + 1
args[ap] = stack[sp]
sp = sp - 1
fn = stack[sp]
stack[sp] = fn(py_unpack(args))

::_18::

::_21::

::_24::
