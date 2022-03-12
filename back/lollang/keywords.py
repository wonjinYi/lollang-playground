from enum import Enum, auto
class Keyword(Enum):
    BLANK = auto()
    VAR_DECLARE = auto()
    VAR_ASSIGN = auto()
    VAR_PRINT = auto()
    VAR_INPUT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FUNCTION = auto()
    FOR = auto()
    SWAP = auto()
    NEWLINE = auto()
    BREAK = auto()
    CONTINUE = auto()
    
    COMMENT = auto()
    CLOSE = auto() # loop out
    
    LT = auto() # <
    LE = auto() # <=
    GT = auto() # >
    GE = auto() # >=