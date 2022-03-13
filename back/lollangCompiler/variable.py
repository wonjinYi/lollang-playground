from enum import Enum, auto

class TYPE(Enum): # 자료형
    INT = auto()
    STR = auto()

class Variable:
    def __init__(self):
        self.var = dict()
    
    def insert(self, name):
        try:
            self.var[name]
        except KeyError:
            self.var[name] = [f"var_{len(self.var)}", TYPE.INT]
    
    def get(self, name):
        return self.var[name][0]
    
    def getType(self, name):
        return self.var[name][1]
    
    def setType(self, name, newType):
        self.var[name][1] = newType

class FunVariable(Variable):
    def __init__(self):
        super().__init__()
    
    def insert(self, name):
        try:
            self.var[name]
            raise SyntaxError
        except KeyError:
            self.var[name] = [f"fun_{len(self.var)}"]