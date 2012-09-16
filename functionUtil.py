# Copyright (c) 2011 Zachary Winnerman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import marshal
import types
import pickle
def packFunction(f):
  # this function takes a method or function and returns a string
  return pickle.dumps((f.__name__,marshal.dumps(f.func_code)))
def unpackFunction(f):
  s=f[1]
  name=f[0]
  # this function takes a string and returns a function or method
  return types.FunctionType(marshal.loads(s),globals(),name)
def packClass(c):
  # this function takes a class and returns a string
  ignoreList=['__module__','__doc__']
  o={}
  for i in dir(c):
    if i in ignoreList: continue
    if type(getattr(c,i))==types.MethodType:
      o[i]=packFunction(getattr(c,i))
    else:
      o[i]=getattr(c,i)
  return pickle.dumps((c.__name__,o))
def unpackClass(s):
  # this function takes a string and returns a class
  name,c=pickle.loads(s)
  o=type(name,(object,),{})
  o.__name__=name
  for i in c:
    if type(c[i])==types.TupleType:
      # its a method
      setattr(o,i,unpackFunction(c[i]))
    else:
      setattr(o,i,c[i])
  return o
def dumps(a):
  # determine what a is
  if type(a) == types.ClassType:
    return pickle.dumps(('c',packClass(a)))
  if (type(a) == types.FunctionType) or (type(a) == types.MethodType):
    return pickle.dumps(('f',packFunction(a)))
  if type(a) == types.InstanceType:
    return pickle.dumps(('i',pickle.dumps((pickle.dumps(a),packClass(a.__class__)))))
def loads(s):
  bla=pickle.loads(s)
  if bla[0]=='c':
    return unpackClass(bla[1])
  if bla[0]=='f':
    return unpackFunction(pickle.loads(bla[1]))
  if bla[0]=='i':
    temp=pickle.loads(bla[1])
    return (temp[0],unpackClass(temp[1]))
