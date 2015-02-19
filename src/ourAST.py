import pdb

class ZAst(object):
    pass

class Program(ZAst):
    
    def __init__(self,stmts):
        self.stmts = [stmts]

    def add(self,stmt):
        self.stmts.append(stmt) 
        return self

class StmtList(ZAst):

    def __init__(self,value):
        self.stmts = [value]

    def add(self,v):
        self.stmts.append(v)
        return self

class Stmt(ZAst):

    def __init__(self,t,value=None):
        self.type = t
        self.value = value

class Func(ZAst):

    def __init__(self,params,body):
        self.params = params
        self.body = body
        self.type = 'func'

class Class(ZAst):

    def __init__(self,pclass,body):
        self.pclass = pclass
        self.body = body
        self.type = 'cls'


class Const(ZAst):

    def __init__(self,value):
        self.value = value

class ParamList(ZAst):

    def __init__(self,params):
        if isinstance(params,list):
            self.params = params
        else:
            self.params = [params]

    def add(self,param):
        self.params.append(param)
        return self

class Param(ZAst):

    def __init__(self,t,v1=None,v2=None):
        self.type = t
        self.name = None
        self.value = None
        if self.type == 'value':
            self.name = v1
            self.value = v2
        elif self.type == 'default':
            self.name = v1
        elif self.type == 'direct':
            self.value = v1

class NameList(ZAst):

    def __init__(self,name):

        self.names = [name]

    def add(self,name):
        self.names.append(name)
        return self 

class Arith(ZAst):

    def __init__(self,op,v1=None,v2=None):
        self.op = op
        self.v1 = v1
        self.v2 = v2

class Suite(ZAst):

    def __init__(self,suite):
        self.suite = suite

class Test(ZAst):
    def __init__(self,op,v1=None,v2=None):
        self.op = op
        self.v1 = v1
        self.v2 = v2

class TrailerList(ZAst):

    def __init__(self,t):
        self.ts = [t]

    def add(self,t):
        self.ts.append(t)
        return self

class Trailer(ZAst):

    def __init__(self,op,value):
        self.op = op
        self.value = value

class Item(ZAst):

    def __init__(self,t,v1=None,v2=None):
        self.type = t
        self.v1 = v1
        self.v2 = v2

class Atom(ZAst):

    def __init__(self,t,value):
        self.type = t
        self.value = value