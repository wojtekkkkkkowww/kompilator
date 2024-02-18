import PseudoCode as pc

class CodeGenerator:
    def __init__(self,data):
        self.proc_declarations = data[0]
        self.main_declarations = data[1]
        self.free_registers = data[2] 
        self.is_READ_or_WRITE = data[3]
        self.machine_code = []
        self.RA = '?'  
        self.last_command = None

    def translate(self,ast):   
        for procedure in ast[0]:
            proc_name = procedure[0][0]
            proc = self.proc_declarations[proc_name]
            for node in procedure:
                if type(node) is int:
                    continue #numer linii

                if node[0] == 'commands':
                    proc.set_commands(node[1])

        self.translate_main(ast[1])
        self.machine_code.append('HALT')
        return self.machine_code

    def translate_main(self,main):
        for node in main:
            if node[0] == 'commands':
                for command in node[1]:
                    self.translate_command(command,'main')

    def translate_command(self,com,scope):
        if com[0] == 'ASSIGN':
            self.translate_assign(com,scope)
            self.last_command = "ASSIGN"
        if com[0] == 'IF':
            k = self.translate_if(com,scope)
            self.add_jump_to_if(com[1][0],k,len(self.machine_code))
            self.last_command = "IF"
            self.RA = '?'
        if com[0] == 'IFELSE':
            self.translate_ifelse(com,scope)
            self.last_command = "IFELSE"
            self.RA = '?'
        if com[0] == 'WHILE':
            self.RA = '?'
            self.translate_while(com,scope)
            self.last_command = "WHILE"
            self.RA = '?'
        if com[0] == 'REPEAT':
            self.RA = '?'
            self.translate_repeat(com,scope)
            self.last_command = "REPEAT"
            self.RA = '?'
        if com[0] == 'READ':
            self.translate_read(com,scope)
            self.last_command = "READ"
            self.RA = '?'
        if com[0] == 'WRITE':
            self.translate_write(com,scope)
            self.last_command = "WRITE"
            self.RA = '?'
        if com[0] == 'proc_call':
            self.translate_proc_call(com,scope)
            self.last_command = "proc_call"
            self.RA = '?'
    def translate_proc_call(self,com,scope):
        proc_name = com[1]
        proc = self.proc_declarations[proc_name]
        args = []
        for var_name in com[2]:
            var = self.find_var_by_name(scope,var_name)
            args.append(var)
        proc.set_arguments(args)
        for command in proc.commands:
            self.translate_command(command,proc_name)
           



    def translate_assign(self,com,scope):
        iden = com[1]
        exp = com[2]
        if exp[0] == 'val':
            val = exp[1]
            if val[0] == 'number':
                self.machine_code += pc.load_num(val[1],'a') 
            if val[0] == 'iden': 
                self.load_from_iden(scope,val[1],'a')
            self.save_to_iden(scope,iden,'a')
            
        if exp[0] == 'ADD':
            val1 = exp[1]
            val2 = exp[2]

            if val1[0] == 'number' and val2[0] == 'number' :
                const = val1[1] + val2[1]
                self.machine_code += pc.load_num(const,'a')

            elif val1[0] == 'number' and val1[1] < 5 :
                self.load_from_val(scope,val2,'a',True)
                for i in range(val1[1]):
                    self.machine_code.append("INC a")
                self.save_to_iden(scope,iden,'a')
            elif val2[0] == 'number' and val2[1] < 5 :
                self.load_from_val(scope,val1,'a',True)
                for i in range(val2[1]):
                    self.machine_code.append("INC a")
                self.save_to_iden(scope,iden,'a')
            elif val1[1] == val2[1]:
                self.load_from_val(scope,val1,'a',True)
                self.machine_code.append("SHL a")
                self.save_to_iden(scope,iden,'a')

            else:
                self.load_from_val(scope,val1,'b',True) 
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                self.machine_code.append("GET b")
                self.machine_code += pc.gen_expression('+')
                self.save_to_iden(scope,iden,'a')
        
        if exp[0] == 'SUB':
            val1 = exp[1]
            val2 = exp[2]
            if val1[0] == 'number' and val2[0] == 'number' :
                const = val1[1] - val2[1]
                if const < 0:
                    const = 0
                self.machine_code += pc.load_num(const,'a')

            elif val1[0] == 'number' and val1[1] == 0 :
                self.machine_code.append("RST a")
                self.save_to_iden(scope,iden,'a')
            elif val2[0] == 'number' and val2[1] < 5 :
                self.load_from_val(scope,val1,'a',True)
               
                for i in range(val2[1]):
                    self.machine_code.append("DEC a")
                self.save_to_iden(scope,iden,'a')
            
            elif val2[1] == val1[1]:
                self.machine_code.append("RST a")
                self.save_to_iden(scope,iden,'a')
            else:    
                self.load_from_val(scope,val1,'b',True)
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                self.machine_code.append("GET b")
                self.machine_code += pc.gen_expression('-')
                self.save_to_iden(scope,iden,'a')
        
        if exp[0] == 'MUL':
            val1 = exp[1]
            val2 = exp[2]

            if val1[0] == 'number' and val2[0] == 'number':
                const = val1[1] * val2[1]
                self.machine_code += pc.load_num(const,'a')
                
            elif val2[0] == 'number' and val2[1] == 2:
                self.load_from_val(scope,val1,'a',True)
                self.machine_code.append("SHL a")
                self.save_to_iden(scope,iden,'a')

            elif val1[0] == 'number' and val1[1] == 2:
                self.load_from_val(scope,val2,'a',True)
                self.machine_code.append("SHL a")
                self.save_to_iden(scope,iden,'a')

            elif (val1[0] == 'number' and val1[1] == 0) or (val2[0] == 'number' and val2 == 0):
                self.machine_code.append("RST a")
                self.save_to_iden(scope,iden,'a')

            elif val1[0] == 'iden' and val2[0] == 'iden' and val1[1] == val2[1]:
                self.load_from_val(scope,val1,'a',True)
                self.machine_code.append("PUT h")
                self.machine_code += pc.gen_expression('*',len(self.machine_code))
                self.save_to_iden(scope,iden,'a')    


            else:
                self.load_from_val(scope,val1,'b',True)
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                
                self.machine_code.append("GET b")   
                self.machine_code += pc.gen_expression('*',len(self.machine_code))
                self.save_to_iden(scope,iden,'a')    

        if exp[0] == 'DIV':
            val1 = exp[1]
            val2 = exp[2]
            if val1[0] == 'number' and val2[0] == 'number':
                if val2[1] == 0:
                    const = 0
                else:
                    const = val1[1] // val2[1]
                self.machine_code += pc.load_num(const,'a')

            elif val2[0] == 'number' and val2[1] == 2:
                self.load_from_val(scope,val1,'a',True)
                self.machine_code.append("SHR a")
                self.save_to_iden(scope,iden,'a')

            else:
                self.load_from_val(scope,val1,'b',True)
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                
                self.machine_code.append("GET b")
                self.machine_code += pc.gen_expression('/',len(self.machine_code))
                self.save_to_iden(scope,iden,'a')

        if exp[0] == 'MOD':
            val1 = exp[1]
            val2 = exp[2]
                
            if val1[0] == 'number' and val2[0] == 'number':
                if val2[1] == 0:
                    const = 0
                else:
                    const = val1[1] % val2[1]
                self.machine_code += pc.load_num(const,'a')
            elif val2[0] == 'number' and val2[1] == 2:
                self.load_from_val(scope,val1,'a',True)
                self.machine_code.append("PUT h")
                self.machine_code.append("SHR a")
                self.machine_code.append("SHL a")
                self.machine_code.append("PUT c")
                self.machine_code.append("GET h")
                self.machine_code.append("SUB c")
                self.save_to_iden(scope,iden,'a')
                
            else:
                self.load_from_val(scope,val1,'b',True)
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                
                self.machine_code.append("GET b")
                self.machine_code += pc.gen_expression('%',len(self.machine_code))
                self.save_to_iden(scope,iden,'a')


    def translate_write(self,com,scope):
        val = com[1]
        self.load_from_val(scope,val,'a')
        self.machine_code.append("WRITE")

    def translate_read(self,com,scope):
        iden = com[1]
        self.machine_code.append("READ")
        self.save_to_iden(scope,iden,'a')


    def translate_ifelse(self,com,scope):
        k = self.translate_if(com,scope) 
        l = len(self.machine_code)
        self.machine_code.append(" ") 
        elsecommands = com[3][1]
        self.RA = '?'
        for command in elsecommands:
            self.translate_command(command,scope)
        m = len(self.machine_code)
        self.add_jump_to_if(com[1][0],k,l+1)
        self.machine_code[l] = f"JUMP {m}"
        

    def translate_if(self,com,scope):
        cond = com[1]
        commands = com[2][1]
        op = cond[0]
        val1 = cond[1]
        val2 = cond[2]
        self.translate_cond(op,val1,val2,scope)        
        k  = len(self.machine_code)
        self.machine_code.append(" ") 
        
        for command in commands:
            self.translate_command(command,scope)    
        return k



    def add_jump_to_if(self,op,k,l):
        if op == 'LE':
            self.machine_code[k] = f"JPOS {l}"
        if op == 'GE':
            self.machine_code[k] = f"JPOS {l}"
        if op == 'LT':
            self.machine_code[k] = f"JZERO {l}" 
        if op == 'GT':
            self.machine_code[k] = f"JZERO {l}" 
        if op == 'EQ':
            self.machine_code[k] = f"JPOS  {l}" 
        if op == 'NEQ':
            self.machine_code[k] = f"JZERO {l}" 



    def translate_repeat(self,com,scope):
        commands = com[2][1]
        cond = com[1]
        op = cond[0]
        k = len(self.machine_code)
        for command in commands:
            self.translate_command(command,scope)
        val1 = cond[1]
        val2 = cond[2]
        self.translate_cond(self.neg_op(op),val1,val2,scope)
        l = len(self.machine_code) 
        self.machine_code.append(" ") 
        self.machine_code.append(f"JUMP {k}") 

        self.add_jump_to_if(self.neg_op(op),l,len(self.machine_code))    

    def neg_op(self,op):
        if op == 'LE':
            return 'GE'
        if op == 'GE':
            return 'LE'
        if op == 'LT':
            return 'GT'
        if op == 'GT':
            return 'LT'
        if op == 'EQ':
            return 'NEQ'
        if op == 'NEQ':
            return 'EQ'



    def translate_while(self,com,scope):
        commands = com[2][1]
        cond = com[1]
        op = cond[0]
        val1 = cond[1]
        val2 = cond[2]
        k = len(self.machine_code)
        self.translate_cond(op,val1,val2,scope)
        l = len(self.machine_code)
        self.machine_code.append(" ") 
        for command in commands:
            self.translate_command(command,scope)
        self.machine_code.append(f"JUMP {k}") 
        self.add_jump_to_if(op,l,len(self.machine_code))
        

    def translate_cond(self,op,val1,val2,scope):
        if op == 'LE':
            if val1[0] == 'number' and val1[1] == 0 :    
                self.load_from_val(scope,val2,'a',True)
            else:
                self.load_from_val(scope,val1,'b',True)  
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                self.machine_code.append("GET b")   
                self.machine_code.append("SUB h")
        if op == 'GE':
            self.translate_cond('LE',val2,val1,scope)

        if op == 'GT':
            if val2[0] == 'number' and val2[1] == 0 :
                self.load_from_val(scope,val1,'a',True)
            else:
                self.load_from_val(scope,val1,'b',True)  
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                self.machine_code.append("GET b")   
                self.machine_code.append("SUB h")
        if op == 'LT':
            self.translate_cond('GT',val2,val1,scope)

        if op in  {'EQ','NEQ'}:
            if val1[0] == 'number' and val1[1] == 0 :    
                self.load_from_val(scope,val2,'a',True)
            elif val2[0] == 'number' and val2[1] == 0 :    
                self.load_from_val(scope,val1,'a',True)
            else:    
                # (a-h) + (h-a)
                self.load_from_val(scope,val1,'b',True)  
                if val1[1] == 'iden' and val1[1][0] == 'var':
                    self.load_from_val(scope,val2,'h',True)
                else:
                    self.load_from_val(scope,val2,'h')
                self.machine_code.append("GET b")   
                self.machine_code.append("PUT g")
                #a - h
                self.machine_code.append("SUB h")
                self.machine_code.append("PUT f")
                #h - a
                self.machine_code.append("GET h")
                self.machine_code.append("SUB g")
                # (a-h) + (h-a)
                self.machine_code.append("ADD f")   
        self.RA = '?'


    def save_to_iden(self,scope,iden,reg):
        if iden[0] == 'var':
            self.RA = iden[1]
            var = self.find_var_by_name(scope,iden[1])
            self.machine_code += pc.save_to_mem(reg,var,0)

        elif iden[0] == 'arr' or iden[0] == 'arr2':
            self.RA = '?'
            var_name = iden[1]
            var = self.find_var_by_name(scope,var_name)

            if iden[0] == 'arr':
                var2_name = iden[2]
                var2 = self.find_var_by_name(scope,var2_name)
                self.machine_code.append("PUT c")
                self.machine_code += pc.save_arr(reg,var,var2)    
                self.machine_code.append("GET c")
            if iden[0] == 'arr2':
                num = iden[2]
                self.machine_code += pc.save_to_mem(reg,var,num)
        

    def load_from_val(self,scope,val,reg,o = False):
        if val[0] == 'number':
            self.machine_code += pc.load_num(val[1],reg)
        if val[0] == 'iden':
            iden = val[1]
            self.load_from_iden(scope,iden,reg,o)
        return

    def load_from_iden(self,scope,iden,reg,o = False):
        if iden[0] == 'var':
            var = self.find_var_by_name(scope,iden[1])
            if self.last_command == "ASSIGN" and var.name == self.RA and o :
                if reg != 'a':
                    self.machine_code.append(f"PUT {reg}")
            else:
                self.machine_code += pc.load_var(var,reg)
        
        elif iden[0] == 'arr' or iden[0] == 'arr2':
            var_name = iden[1]
            var = self.find_var_by_name(scope,var_name)

            if iden[0] == 'arr':
                var2_name = iden[2]
                var2 = self.find_var_by_name(scope,var2_name)
                self.machine_code += pc.load_arr(var,var2,reg)    
                
            if iden[0] == 'arr2':
                of = iden[2]
                self.machine_code += pc.load_from_mem(var,of,reg)


    def find_var_by_name(self,scope,var_name):
        var = None
        if scope == 'main':
            var = self.main_declarations[var_name]
        else:
            if var_name in self.proc_declarations[scope].declarations:
                var = self.proc_declarations[scope].declarations[var_name]
            else:
                var = self.proc_declarations[scope].arg_map[var_name].var

        return var

