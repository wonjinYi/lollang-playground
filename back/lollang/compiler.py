from keywords import Keyword
from operators import Operator
from variable import Variable, TYPE

class Compiler:
    def __init__(self):
        self.codes = list()
        self.stack = list()
        self.out = list()
        
        self.valid = False
        self.indent = 0
        self.var = Variable()
        
    def getNewLine(self, elseFlag = False):
        return "\t"*(self.indent - int(elseFlag))
    
    def save(self, path = "out.py"):
        with open(path, "w") as file:
            for code in self.out:
                file.write(code+"\n")
    
    def checkComment(self, code):
        ix = code.find("잠만")
        if ix>=0:
            code = code[:ix]
        return code
    
    def getType(self, code):
        if "스왑좀" in code:
            return Keyword.SWAP
        if "캐리좀" in code:
            return Keyword.VAR_ASSIGN
        if "갱좀" in code:
            return Keyword.VAR_PRINT
        if "리쉬좀" in code:
            return Keyword.VAR_INPUT
        if "근데저기" in code:
            return Keyword.ELIF
        if "저기" in code:
            return Keyword.IF
        if "아니" in code:
            return Keyword.FUNCTION
        if "님아" in code:
            return Keyword.FOR
        if "뭐함?" in code:
            return Keyword.CLOSE
        if "잠만" in code:
            return Keyword.COMMENT
        if "님" in code:
            return Keyword.VAR_DECLARE
        if "뭐하냐고" in code:
            return Keyword.NEWLINE
        if "근데" in code:
            return Keyword.ELSE
        if "그니까" in code:
            return Keyword.WHILE
    
    def removeDeclare(self, elements): # 선언과 동시에 입력, 대입시 "님" 제거
        return [element[:-1] if element[-1] == '님' else element for element in elements]
        
    def varCheck(self, elements):
        for element in elements:
            if element[-1] == "님":
                self.var.insert(element[:-1])
            elif not self.var.get(element):
                print(f">> Error : 그런 변수명이 없습니다. {element}")
                return False
        return True
    
    def varDeclare(self, code):
        out = self.getNewLine()
        code = code.replace(" ", "")
        name = code[:code.find("님")]
        self.var.insert(name)
        self.out.append(out + f"{self.var.get(name)} = 0")
    
    def varInput(self, code):
        out = self.getNewLine()
        elements = code.split()
        strFlag = elements[-1] == "리쉬좀요"
        elements = elements[:-1]
        
        if not self.varCheck(elements):
            # 컴파일 에러
            print(">> 변수가 없는게 있습니다!!")
            
        elements = self.removeDeclare(elements)
        for element in elements:
            if self.var.getType(element) == TYPE.INT and strFlag:
                self.var.setType(element, TYPE.STR)
            if self.var.getType(element) == TYPE.STR and not strFlag:
                self.var.setType(element, TYPE.INT)
        if len(elements) == 1:
            if strFlag:
                out += f"{self.var.get(elements[0])} = input()"
            else:
                out += f"{self.var.get(elements[0])} = int(input())"
        else:
            out += f"{self.var.get(elements[0])}"
            for element in elements[1:]:

                out += f", {self.var.get(element)}"
            if strFlag:
                out+=" = input().split()"
            else:
                out+=" = map(int, input().split())"
        self.out.append(out)
    
    def varPrint(self, code):
        out = self.getNewLine()
        out += "print("
        elements = code.split()
        strFlag = elements[-1] == "갱좀요"
        elements = elements[:-1]
        # if not self.varCheck(elements):
        #     # 컴파일 에러
        #     pass
        if strFlag:
            out+=f"chr({self.makeAssignStmt(elements[0])})"
        else:
            out+=f"{self.makeAssignStmt(elements[0])}"
        if len(elements) == 1:
            out+=",end='')"
        else:
            for element in elements[1:]:
                if strFlag:
                    out+=f", chr({self.makeAssignStmt(element)})"
                else:
                    out+=f", {self.makeAssignStmt(element)}"
            out+=",end='')"
        self.out.append(out)
    
    def varSwap(self, code):
        elements = code.split()[:-1]
        if not self.varCheck(elements):
            # 컴파일 에러
            pass
        for element in elements:
            out = self.getNewLine()
            var_type = self.var.getType(element)
            if var_type == TYPE.INT:
                out += f"{self.var.get(element)} = chr({self.var.get(element)})"
                self.var.setType(element, TYPE.STR)
            elif var_type == TYPE.STR:
                out += f"{self.var.get(element)} = ord({self.var.get(element)})"
                self.var.setType(element, TYPE.INT)
            else:
                print(">> 잘못된 타입입니다.")
            self.out.append(out)
            
    def makeAssignStmt(self, code, ix = 0):
        stmt = ""
        op = Operator.getOp()
        if ix == len(op):
            element = code
            l = len(element)
            if element[0] == Operator.ONE:
                if element.count(Operator.ONE) != l:
                    # 컴파일에러
                    print(">> 변수 대입이 잘못되었습니다.")
                else:
                    stmt+=f"{l}"
            else:
                stmt+=f"{self.var.get(element)}"
            return stmt
            
        elements = code.split(op[ix])
        l = len(elements)
        for i, element in enumerate(elements):
            stmt += self.makeAssignStmt(element, ix+1)
            if i < l-1:
                stmt += Operator.op[ix]
        return stmt

    def varAssign(self, code):
        out = self.getNewLine()
        elements = code.split(" ")
        elements = [element for element in elements if element != ""]
        if not self.varCheck([elements[0]]):
            # 컴파일 에러
            pass
        variable = self.removeDeclare([elements[0]])[0]
        out += f"{self.var.get(variable)} = "
        out += self.makeAssignStmt(elements[-1])
        self.out.append(out)
    
    def forStmt(self, code):
        out = self.getNewLine()
        elements = code.split(" ")[:-1]
        
        out+=f"for {self.var.get(elements[0])} in range({self.makeAssignStmt(elements[1])}, {self.makeAssignStmt(elements[2])}):"
        self.indent+=1
        self.out.append(out)
    
    def ifStmt(self, code, elifFlag = False):
        out = self.getNewLine(elifFlag)
        elements = code.split(" ")[1:]
        
        if elifFlag:
            out+=f"elif {self.makeAssignStmt(elements[0])}:"
        else:
            out+=f"if {self.makeAssignStmt(elements[0])}:"
            self.indent+=1
        self.out.append(out)
    
    def closeStmt(self):
        self.indent-=1
        
    def newLine(self):
        out = self.getNewLine()
        out += "print()"
        self.out.append(out)
        
    def elseStmt(self):
        out = self.getNewLine(True)
        out+="else:"
        self.out.append(out)
    
    def whileStmt(self, code):
        out = self.getNewLine()
        elements = code.split(" ")[1:]
        
        out+=f"while {self.makeAssignStmt(elements[0])}:"
        self.indent+=1
        self.out.append(out)
    
    def compileLine(self, code):
        code = self.checkComment(code)
        if self.isEmptyLine(code):
            return
        TYPE = self.getType(code)
        if TYPE == Keyword.VAR_DECLARE:
            self.varDeclare(code)
        if TYPE == Keyword.VAR_ASSIGN:
            self.varAssign(code)
        if TYPE == Keyword.VAR_PRINT:
            self.varPrint(code)
        if TYPE == Keyword.VAR_INPUT:
            self.varInput(code)
        if TYPE == Keyword.SWAP: # 아스키를 숫자로 변환
            self.varSwap(code)
        if TYPE == Keyword.FOR:
            self.forStmt(code)
        if TYPE == Keyword.CLOSE:
            self.closeStmt()
        if TYPE == Keyword.NEWLINE:
            self.newLine()
        if TYPE == Keyword.IF:
            self.ifStmt(code)
        if TYPE == Keyword.ELSE:
            self.elseStmt()
        if TYPE == Keyword.ELIF:
            self.ifStmt(code, True)
        if TYPE == Keyword.WHILE:
            self.whileStmt(code)
    
    def isEmptyLine(self, code):
        for i in code:
            if i != " ":
                return False
        return True
    
    def compile(self, codes):
        if codes[0] != "우리 잘해보죠" or codes[-1] != "팀차이 ㅈㅈ":
            print(">> Error : 코드형식을 확인하세요.")
            return
        codes = codes[1:-1]
        for code in codes:
            if self.isEmptyLine(code):
                continue
            self.compileLine(code)
    
    def compileFile(self, path, outPath = "out.py"):
        with open(path, "r", encoding="utf-8") as file:
            codelines = [i.rstrip() for i in file.readlines()]
            self.compile(codelines)
        self.save(outPath)
        self.run(outPath)
    
    def run(self, path = "out.py"):
        try:
            exec(open(path).read())
        except:
            print("소환사 한명이 게임을 종료했습니다.")
            print(">> 런타임 에러")


# if __name__ == "__main__":
#     compiler = Compiler()
#     compiler.compileFile("example/while.lo")
#     compiler.save()
#     compiler.run()