from sly import Lexer

class MyLexer(Lexer):
    tokens = {PROGRAM,PROCEDURE,IS,IN,END,IF,
              THEN,ELSE,WHILE,ENDWHILE,ENDIF,DO,UNTIL,REPEAT,READ,WRITE,T,NUM,PIDENTIFIER,
              ASSIGN,NEQ,LE,GE,EQ,LT,GT,PLUS,MINUS,MOD,TIMES,DIV,LP1,RP1,RP2,LP2,COMMA,SEMIC}

    ignore = ' \t'

    @_(r'#.*')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')    

    PROGRAM = r'PROGRAM'
    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'
    ENDIF = r'ENDIF'  
    WHILE = r'WHILE'
    ENDWHILE = r'ENDWHILE'  
    END = r'END'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    DO = r'DO'
    UNTIL = r'UNTIL'
    REPEAT = r'REPEAT'
    READ = r'READ'
    WRITE = r'WRITE'
    T = r'T'
    PIDENTIFIER = r'[_a-z]+'
    ASSIGN = r':='
    NEQ = r'!='
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    EQ = r'='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    MOD = r'%'
    DIV = r'/'
    LP1 = r'\('
    RP1 = r'\)'
    LP2 = r'\['
    RP2 = r'\]'
    COMMA = r','
    SEMIC = r';'

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t
    
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1





