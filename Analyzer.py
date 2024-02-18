from Definitions import Variable
from Definitions import Procedure
from Definitions import Argument
import sys

def error(error_message):
    print("ERROR",error_message)
    sys.exit(1)

class MyAnalyzer:
   
   
    def __init__(self):
        self.k = 0 
        self.main_declarations = dict()  #mapa deklaracji
        self.proc_declarations = dict()  #napa procedur

        self.free_registers = {} 
        self.is_READ_or_WRITE = False 


    def analyze(self,AST): 
        for procedure in AST[0]:
            self.analyze_procedure(procedure)
        self.analyze_main(AST[1])

    def analyze_procedure(self, procedure):
    
        proc_head = procedure[0]
        proc_name = proc_head[0]
        line_number = procedure[-1] 
        arguments = proc_head[1]

        proc = Procedure(proc_name)
        proc.proc_head = self.gen_fun_head(proc_head)
        if proc_name in self.proc_declarations.keys():
            error(f"{line_number}: Procedure name '{proc_name}' already used")
        else:
            self.proc_declarations[proc_name] = proc


        for argument in arguments:
            t = argument[0]
            arr_name = argument[1]
            if t == 'var':
                arr = Argument(arr_name,'var',proc_name)
                proc.arg_map[arr_name] = arr
                proc.arg_list.append(arr)
            else :
                arr = Argument(arr_name,'arr',proc_name)
                proc.arg_map[arr_name] = arr
                proc.arg_list.append(arr)

        for node in procedure:
            if type(node) is int:
                continue

            if node[0] == 'declarations':
                for declaration in node[1]:
                    var_name = declaration[1]
                    line_number = declaration[-1]
                    dec = proc.declarations
                    
                    if (var_name in dec.keys()) or (var_name in proc.arg_map.keys()): 
                        error(f"{line_number}: name '{var_name}' already used")
                    else:
                        if declaration[0]  == 'var':
                            var = Variable(var_name,'var',proc_name)
                            dec[var_name] = var

                        else: 
                            size = declaration[2]
                            var = Variable(var_name,'arr',proc_name,size=size)
                            dec[var_name] = var
        for node in procedure:
            if type(node) is int:
                continue

            if node[0] == 'commands':
                for command in node[1]:
                    self.analyze_command(command,proc.declarations,True,proc_name,proc.arg_map,proc.arg_list)                        


    def analyze_main(self, main):
        for node in main:
            if node[0] == 'declarations':
                for declaration in node[1]:
                    line_number = declaration[-1]
                    var_name = declaration[1]
                    
                    if var_name in self.main_declarations.keys():
                        error(f"{line_number}: name '{var_name}' already used")
                    if declaration[0] == 'arr':
                        size = declaration[2]
                        var = Variable(var_name,'arr','MAIN',size=size)
                        self.main_declarations[var_name] = var
                    else:
                        var = Variable(var_name,'var','MAIN')
                        self.main_declarations[var_name] = var

        for node in main:

            if node[0] == 'commands':
                for command in node[1]:
                    self.analyze_command(command,self.main_declarations)
                    

    def analyze_command(self,command,declarations,is_proc = False,proc_name = None, arg_map = None,arg_list = None):
        
        line_number = command[-1]

        com_type = command[0]
        if com_type == 'ASSIGN':
            iden =  command[1]

            
            if iden[1] not in declarations.keys():
                if is_proc and (iden[1] not in arg_map.keys()): 
                    error(f"{line_number}: '{iden[1]}' not declared")
                if not is_proc:
                    error(f"{line_number}: '{iden[1]}' not declared")
            
            if (iden[1] in declarations.keys()) and declarations[iden[1]].type == 'var':
                declarations[iden[1]].is_Assigned = True

    
            if is_proc and (iden[1] in arg_map.keys()):
                arg_map[iden[1]].is_assigning = True
    

            self.check_iden_syntax(line_number,iden,declarations,is_proc,arg_map)    
            exp = command[2]
 
            if exp[0] == 'val':
                val = exp[1]
                self.check_val_syntax(line_number,val,declarations,is_proc,arg_map)
                        
            
            operator = exp[0]         
            if operator == 'ADD' or operator == 'SUB' or operator == 'MUL' or operator == 'DIV' or operator == 'MOD':
                
                val1 = exp[1]
                val2 = exp[2]

                self.check_val_syntax(line_number,val1,declarations,is_proc,arg_map)
                self.check_val_syntax(line_number,val2,declarations,is_proc,arg_map)


        if com_type in {'IF', 'IFELSE', 'WHILE', 'REPEAT'}:
            
            condition = command[1]
            val1 = condition[1]
            val2 = condition[2]


            if com_type != 'REPEAT':
                self.check_val_syntax(line_number,val1,declarations,is_proc,arg_map)
                self.check_val_syntax(line_number,val2,declarations,is_proc,arg_map)


            if com_type == 'IF':
                if_commands = command[2][1]
            
                for com in if_commands:
                    self.analyze_command(com,declarations,is_proc,proc_name,arg_map,arg_list) 
            
            if com_type == 'IFELSE':
                if_commands = command[2][1]
                else_commands = command[3][1]
            
                for com in if_commands:
                    self.analyze_command(com,declarations,is_proc,proc_name,arg_map,arg_list)
                
                for com in else_commands:
                    self.analyze_command(com,declarations,is_proc,proc_name,arg_map,arg_list)
            
            if com_type == 'WHILE':
                while_commands = command[2][1]
            
                for com in while_commands:
                    self.analyze_command(com,declarations,is_proc,proc_name,arg_map,arg_list)
            
            if com_type == 'REPEAT':
                repeat_commands = command[2][1]
            
                for com in repeat_commands:
                    self.analyze_command(com,declarations,is_proc,proc_name,arg_map,arg_list)

                self.check_val_syntax(line_number,val1,declarations,is_proc,arg_map) 
                self.check_val_syntax(line_number,val2,declarations,is_proc,arg_map)


        if com_type  == 'READ':
            iden = command[1]

            if iden[0] == 'var':
                if (iden[1] in declarations.keys()) and declarations[iden[1]].type == 'var':
                    declarations[iden[1]].is_Assigned = True

            self.check_iden_syntax(line_number,iden,declarations,is_proc,arg_map)
            self.is_READ_or_WRITE = True

        if com_type == 'WRITE':
            val = command[1]
            self.check_val_syntax(line_number,val,declarations,is_proc,arg_map)
            self.is_READ_or_WRITE = True



        if com_type == 'proc_call':
            c_proc_name = command[1]
            args = command[2]

            if c_proc_name not in self.proc_declarations.keys():
                error(f"{line_number}: Procedure '{c_proc_name}' not declared")
            if c_proc_name == proc_name and is_proc:
                error(f"{line_number}: Recursive call in function '{proc_name}'")

            called_proc_args = self.proc_declarations[c_proc_name].arg_list


            if c_proc_name in self.proc_declarations.keys():
                self.proc_declarations[c_proc_name].inc_call_num()

     

            if len(args) != len(called_proc_args):
                error(f"{line_number}: Wrong number of arguments, expected {len(called_proc_args)}")

           
            for i,arg in enumerate(args): 
                if called_proc_args[i].is_assigning == True:
                    if arg in declarations.keys():
                        declarations[arg].is_Assigned = True
                    else: 
                        arg_map[arg].is_assigning = True


            for arg in args:
                if (arg not in declarations.keys()):
                    if is_proc and arg not in arg_map.keys():
                        error(f"{line_number}: '{arg}' not declared")
                    if not is_proc:
                        error(f"{line_number}: '{arg}' not declared")


            called_proc = self.proc_declarations[c_proc_name]
            head = called_proc.proc_head
            for i,arg in enumerate(args):
                if arg in declarations.keys() and declarations[arg].type != self.proc_declarations[c_proc_name].arg_list[i].type:
                    if declarations[arg].type == 'var':
                         error(f"{line_number}: {arg} is not an array, {head}")  
                    else:
                        error(f"{line_number}: {arg} is not a variable {head}")
                
                if is_proc and arg in arg_map.keys(): 
                    if arg_map[arg].type != self.proc_declarations[c_proc_name].arg_list[i].type:
                        if arg_map[arg].type == 'var':
                            error(f"{line_number}: {arg} is not an array, {head}")
                        else:
                            error(f"{line_number}: {arg} is not a variable, {head}")
    
    
   
    def check_val_syntax(self,line_num,val,declarations,is_proc = False,arguments = None):
        if val[0] == 'iden':
            iden = val[1]
            self.check_iden_syntax(line_num,iden,declarations,is_proc,arguments)



    def check_iden_syntax(self,line_num,iden,declarations,is_proc = False,arguments = None):
        if iden[1] not in declarations.keys():
            if is_proc and (iden[1] not in arguments.keys()):
                error(f"{line_num}: {iden[1]} not declared") 
            if not is_proc:
                error(f"{line_num}: {iden[1]} not declared")
         
        if iden[0] == 'var':
            if (iden[1] in declarations.keys()) and declarations[iden[1]].type != 'var':
                error(f"{line_num}: {iden[1]} is array")

            if is_proc and (iden[1] in arguments.keys()) and arguments[iden[1]].type != 'var':
                 error(f"{line_num}: {iden[1]} is array")

            if iden[1] in declarations.keys():
                if not declarations[iden[1]].is_Assigned:
                    error(f"{line_num}: {iden[1]} is not assigned")
         
         
        if iden[0] == 'arr' or iden[0] == 'arr2':
            if  (iden[1] in declarations.keys()) and declarations[iden[1]].type != 'arr':
                error(f"{line_num}: {iden[1]} is not an array")

            if is_proc and (iden[1] in arguments.keys()) and arguments[iden[1]].type != 'arr':
                error(f"{line_num}: {iden[1]} is not an array")


    
            if (iden[2] not in declarations.keys()) and iden[0] != 'arr2':
                if is_proc and (iden[2] not in arguments.keys()):
                    error(f"{line_num}: {iden[1]} not declared")
                   
                if not is_proc:
                    error(f"{line_num}: {iden[1]} not declared")
                          
            if (iden[2] in declarations.keys()) and not declarations[iden[2]].is_Assigned:
                error(f"{line_num}: {iden[2]} is not assigned")
                

    def assign_mem_to_vars(self):
        
        for var_name in self.main_declarations.keys():
            var = self.main_declarations[var_name]
            var.set_mem(self.k)
            self.k = self.k + var.size
            
       
        for proc_name in self.proc_declarations.keys():
            for var_name in self.proc_declarations[proc_name].declarations.keys():
                var = self.proc_declarations[proc_name].declarations[var_name]
                var.set_mem(self.k)
                self.k = self.k + var.size
           

    def get_data(self):
        
        self.assign_mem_to_vars()

        a = (self.proc_declarations,self.main_declarations,self.free_registers,self.is_READ_or_WRITE)
        
        return a
                   

    def gen_fun_head(self,head):
        name = head[0]
        args = head[1]
        st = f"{name}(" 
        for arg in args:
            if arg[0] == 'var':
                st += f"{arg[1]},"
            else:
                st += f"T {arg[1]},"
        
        st = st[:-1] + ")"
        return st