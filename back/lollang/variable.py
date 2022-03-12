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
        try:
            return self.var[name][0]
        except KeyError:
            print(f">> Error : 그런 변수명이 없습니다. {name}")
            return False
    
    def getType(self, name):
        try:
            return self.var[name][1]
        except KeyError:
            print(f">> Error : 그런 변수명이 없습니다. {name}")
            return False
    
    def setType(self, name, newType):
        self.var[name][1] = newType