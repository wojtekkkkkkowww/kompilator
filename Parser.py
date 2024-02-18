from sly import Parser
from Lexer import MyLexer
import sys

class MyParser(Parser):
    tokens = MyLexer.tokens 

    def error(self, token):
        print(f"Syntax Error at line {token.lineno}")
        sys.exit(1)

    
    @_('procedures main')
    def program_all(self,p):
        return (p.procedures,p.main)
    

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self,p):
        p.procedures.append((p.proc_head,('declarations',p.declarations),('commands',p.commands),p.lineno))
        return p.procedures
    
    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self,p):
        p.procedures.append((p.proc_head,('commands',p.commands),p.lineno))
        return p.procedures
    
    @_('')
    def procedures(self, p):
        return []


    @_('PROGRAM IS declarations IN commands END')
    def main(self,p):
        return (('declarations',p.declarations),('commands',p.commands))
    
    @_('PROGRAM IS IN commands END')
    def main(self,p):
        return (('commands',p.commands))
    

    @_('commands command')
    def commands(self,p):
        p.commands.append(p.command)
        return p.commands
    
    @_('command')
    def commands(self,p):
        return [p.command]
    

    @_('identifier ASSIGN expression SEMIC')
    def command(self,p):
        return ('ASSIGN',p.identifier,p.expression,p.lineno)
    
    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self,p):
        return ('IFELSE', p.condition,('if_commands',p.commands0),('else_commands',p.commands1),p.lineno)
    
    @_('IF condition THEN commands ENDIF')
    def command(self,p):
        return ('IF', p.condition,('commands',p.commands),p.lineno)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self,p):
        return ('WHILE',p.condition,('commands',p.commands),p.lineno)
    
    @_('REPEAT commands UNTIL condition SEMIC')
    def command(self,p):
        return ('REPEAT',p.condition,('commands',p.commands),p.lineno)
    
    @_('proc_call SEMIC')
    def command(self,p):
        return  p.proc_call
    
    @_('READ identifier SEMIC')
    def command(self,p):
        return ('READ',p.identifier,p.lineno)
    
    @_('WRITE value SEMIC')
    def command(self,p):
        return ('WRITE',p.value,p.lineno)
    

    @_('PIDENTIFIER LP1 args_decl RP1')
    def proc_head(self,p):
        return (p.PIDENTIFIER,p.args_decl)


    @_('PIDENTIFIER LP1 args RP1')
    def proc_call(self,p):
        return ('proc_call',p.PIDENTIFIER,p.args,p.lineno)  
    

    @_( 'declarations COMMA PIDENTIFIER')
    def declarations(self,p):
        p.declarations.append(('var',p.PIDENTIFIER,p.lineno))
        return p.declarations
    
    @_('declarations COMMA PIDENTIFIER LP2 NUM RP2')
    def declarations(self,p):
        p.declarations.append(('arr',p.PIDENTIFIER,p.NUM,p.lineno))
        return  p.declarations
    
    @_('PIDENTIFIER')
    def declarations(self,p):
        return [('var',p.PIDENTIFIER,p.lineno)]
    
    @_('PIDENTIFIER LP2 NUM RP2')
    def declarations(self,p):
        return [('arr',p.PIDENTIFIER,p.NUM,p.lineno)]



    @_('args_decl COMMA PIDENTIFIER')
    def args_decl(self,p):
        p.args_decl.append(('var',p.PIDENTIFIER))
        return p.args_decl
    
    @_('args_decl COMMA T PIDENTIFIER')
    def args_decl(self,p):
        p.args_decl.append(('arr' ,p.PIDENTIFIER))
        return p.args_decl
    
    @_('PIDENTIFIER')
    def args_decl(self,p):
        return [('var',p.PIDENTIFIER)]
    
    @_('T PIDENTIFIER')
    def args_decl(self,p):
        return [('arr',p.PIDENTIFIER)]
    

    @_('args COMMA PIDENTIFIER')
    def args(self,p):
        p.args.append(p.PIDENTIFIER)
        return p.args
    
    @_('PIDENTIFIER')
    def args(self,p):
        return [p.PIDENTIFIER]
    

    @_('value')
    def expression(self,p):
        return ('val',p.value)
    
    @_('value PLUS value')
    def expression(self,p):
        return ('ADD',p.value0,p.value1)
    
    @_('value MINUS value')
    def expression(self,p):
        return ('SUB',p.value0,p.value1)
    
    @_('value TIMES value')
    def expression(self,p):
        return ('MUL',p.value0,p.value1)
    
    @_('value DIV value')
    def expression(self,p):
        return ('DIV',p.value0,p.value1)
    
    @_('value MOD value')
    def expression(self,p):
        return ('MOD',p.value0,p.value1)
    

    @_('value EQ value')
    def condition(self,p):
        return ('EQ',p.value0,p.value1)
    
    @_('value NEQ value')
    def condition(self,p):
        return ('NEQ',p.value0,p.value1)
    
    @_('value LT value')
    def condition(self,p):
        return ('LT',p.value0,p.value1)
    
    @_('value GT value')
    def condition(self,p):
        return ('GT',p.value0,p.value1)

    @_('value LE value')
    def condition(self,p):
        return ('LE',p.value0,p.value1)

    @_('value GE value')
    def condition(self,p):
        return ('GE',p.value0,p.value1)
    

    @_('NUM')
    def value(self,p):
        return ('number',p.NUM)
    
    @_('identifier')
    def value(self,p):
        return ('iden',p.identifier)
    

    @_('PIDENTIFIER')
    def identifier(self,p):
        return ('var',p.PIDENTIFIER)
    
    @_('PIDENTIFIER LP2 NUM RP2')
    def identifier(self,p):
        return ('arr2',p.PIDENTIFIER,p.NUM)
    
    @_('PIDENTIFIER LP2 PIDENTIFIER RP2')
    def identifier(self,p):
        return ('arr', p[0],p[2])
    


