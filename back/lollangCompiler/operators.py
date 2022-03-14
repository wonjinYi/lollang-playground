class Operator:
    GT = "ㄱ"
    GE = "ㅋ"
    LT = "ㄷ"
    LE = "ㅌ"
    EQ = "ㅁ"
    ONE = "ㅠ"
    ADD = "ㅜ"
    SUB = "ㅡ"
    MUL = "ㅓ"
    DIV = "ㅏ"
    INT_DIV = "ㅕ"
    REM = "ㅑ"
    SEP = ","
    END = "."
    op = [",", ">",">=","<","<=", "==","+","-","*","/","//","%"]
        
    @staticmethod
    def getOp():
        return [Operator.SEP, Operator.GT, Operator.GE, Operator.LT, Operator.LE, Operator.EQ, Operator.ADD, Operator.SUB,Operator.MUL,Operator.DIV,Operator.INT_DIV,Operator.REM]