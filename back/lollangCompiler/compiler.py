from lollangCompiler.keywords import Keyword
from lollangCompiler.operators import Operator
from lollangCompiler.variable import Variable, TYPE, FunVariable

class Compiler:
    def __init__(self):
        self.codes = list()
        self.stack = list()
        self.out = list()
        
        self.var = Variable()
        self.funVar = FunVariable()
        
        self.valid = False
        self.indent = 0
        self.currentLine = 0
        
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
        if "오라고" in code:
            return Keyword.CONTINUE
        if "가라고" in code:
            return Keyword.BREAK
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
        if "계속오네" in code:
            return Keyword.FUN_DECLARE
        if "나가라 그냥" in code:
            return Keyword.RETURN
        if "진짜" in code:
            return Keyword.FUN_CALL
    
    def removeDeclare(self, elements): # 선언과 동시에 입력, 대입시 "님" 제거
        return [element[:-1] if element[-1] == '님' else element for element in elements]
        
    def varCheck(self, elements):
        for element in elements:
            if element[-1] == "님":
                self.var.insert(element[:-1])
            elif not self.var.get(element):
                raise KeyError
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
        
        self.varCheck(elements)
            
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
        self.varCheck(elements)
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
                raise TypeError
            self.out.append(out)
            
    def makeAssignStmt(self, code, ix = 0):
        stmt = ""
        op = Operator.getOp()
        
        if code[:2] == "진짜":
            name = code[2:]
            stmt+=f"{self.funVar.get(name)}("
            return stmt
        
        if ix == len(op):
            element = code
            l = len(element)
            numLeftParenthesis, numRightParenthesis = self.getNumLeftParenthesis(element), self.getNumRightParenthesis(element)
            stmt+="("*numLeftParenthesis
            if element[0] == Operator.ONE:
                if element.count(Operator.ONE) != l:
                    # 컴파일에러
                    raise KeyError
                else:
                    stmt+=f"{l}"
            else:
                stmt+=f"{self.var.get(element)}"
            stmt+=")"*numRightParenthesis
            return stmt
            
        elements = code.split(op[ix])
        l = len(elements)
        for i, element in enumerate(elements):
            flag = element[-1] == "."
            if flag:
                element = element[:-1]
            numLeftParenthesis, numRightParenthesis = self.getNumLeftParenthesis(element), self.getNumRightParenthesis(element)
            stmt += "(" * numLeftParenthesis
            stmt += self.makeAssignStmt(element[numLeftParenthesis:len(element)-numRightParenthesis], ix+1)
            stmt += ")" * numRightParenthesis
            if flag:
                stmt+=")"
            if i < l-1:
                stmt += Operator.op[ix]
        stmt = stmt.replace("(,", "(")
        return stmt

    def varAssign(self, code):
        out = self.getNewLine()
        elements = code.split(" ")
        elements = [element for element in elements if element != ""]
        self.varCheck([elements[0]])
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
    
    def continueStmt(self):
        out = self.getNewLine()
        out += "continue"
        self.out.append(out)
    
    def breakStmt(self):
        out = self.getNewLine()
        out += "break"
        self.out.append(out)
    
    def funDeclare(self, code):
        out = self.getNewLine()
        elements = code.split(" ")[:-1]
        name, args = elements[0], elements[1:]
        
        self.funVar.insert(name)
        
        out += f"def {self.funVar.get(name)}("
        for i, arg in enumerate(args):
            self.var.insert(arg)
            if i:
                out+=","
            out+=self.var.get(arg)
        out+="):"
        
        self.indent += 1
        self.out.append(out)
    
    def funCall(self, code): # ret변수 : True -> 함수 호출이 한줄임, False -> 다른 구문 사이에 껴있음
        out = self.getNewLine()
        elements = code[2:].split(",")
        
        name, args = elements[0], elements[1:]
        out+=f"{self.funVar.get(name)}("
        for i, arg in enumerate(args):
            if i:
                out+=","
            out+=self.makeAssignStmt(arg)
        out = out.replace("(,", "(")
        self.out.append(out)

    def returnStmt(self, code):
        out = self.getNewLine()
        out += "return"
        code = code[:code.find("나가라 그냥")].strip()
        elements = code.split(" ")
        if len(elements) > 1: # 반환값은 1개 이하여야 함
            raise SyntaxError
        if len(elements) == 1:
            out+=f" {self.makeAssignStmt(elements[0])}"
        self.out.append(out)
    
    def compileLine(self, code):
        code = self.checkComment(code)
        if self.isEmptyLine(code):
            return
        TYPE = self.getType(code)
        if TYPE == Keyword.CONTINUE:
            self.continueStmt()
        if TYPE == Keyword.BREAK:
            self.breakStmt()
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
        if TYPE == Keyword.FUN_DECLARE:
            self.funDeclare(code)
        if TYPE == Keyword.FUN_CALL:
            self.funCall(code)
        if TYPE == Keyword.RETURN:
            self.returnStmt(code)
    
    def getNumLeftParenthesis(self, code):
        for i, v in enumerate(code):
            if v!="ㄴ":
                return i
        raise ValueError
    
    def getNumRightParenthesis(self, code):
        for i, v in enumerate(code[::-1]):
            if v!="ㄹ":
                return i
        raise ValueError
    
    def isEmptyLine(self, code):
        for i in code:
            if i != " ":
                return False
        return True
    
    def compile(self, codes):
        for ix, code in enumerate(codes):
            self.currentLine = ix + 1
            if ix > 0 and ix < len(codes) - 1:
                self.compileLine(code)
            elif ix == 0 and code != "우리 잘해보죠" or ix == len(codes) - 1 and code != "팀차이 ㅈㅈ":
                raise SyntaxError
        if self.indent:
            raise SyntaxError
    
    def compileFile(self, path, outPath = "out.py"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                codelines = [i.strip() for i in file.readlines()]
                self.compile(codelines)
        except TypeError:
            print(f"{self.currentLine}번째 적이 학살중입니다!!")
        except SyntaxError:
            print(f"{self.currentLine}번째 적은 전설적입니다!!")
        except ValueError:
            print(f"{self.currentLine}번째 적을 도저히 막을 수 없습니다!!")
        except KeyError:
            print(f"{self.currentLine}번째 적이 전장을 지배하고 있습니다!!")
        except FileNotFoundError:
            print("서버에 연결할 수 없습니다.")
        else:
            self.save(outPath)
            self.run(outPath)
    
    def run(self, path = "out.py"):
        try:
            exec(open(path).read())
        except ZeroDivisionError:
            print(f"적이 전장의 화신입니다!!")
        except:
            print("소환사 한명이 게임을 종료했습니다.")


# if __name__ == "__main__":
#     compiler = Compiler()
#     compiler.compileFile("example/while.lo")
#     compiler.save()
#     compiler.run()