class Operator:
    GT = "ㄱ"
    GE = "ㅋ"
    LT = "ㄷ"
    LE = "ㅌ"
    ONE = "ㅠ"
    ADD = "ㅜ"
    SUB = "ㅡ"
    MUL = "ㅓ"
    DIV = "ㅏ"
    INT_DIV = "ㅕ"
    REM = "ㅑ"
    op = [">",">=","<","<=","+","-","*","/","//","%"]
        
    @staticmethod
    def getOp():
        return [Operator.GT, Operator.GE, Operator.LT, Operator.LE, Operator.ADD, Operator.SUB,Operator.MUL,Operator.DIV,Operator.INT_DIV,Operator.REM]