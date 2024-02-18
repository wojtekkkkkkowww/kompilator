class Variable:
    def __init__(self,name,type,scope,size = 1):
        self.name = name
        self.type = type
        self.scope = scope
        self.size = size
        self.is_Assigned = False
        self.is_in_register = False 
        self.reg = None
        self.mem = None
    

    def set_register(self,reg):
        self.is_in_register = True
        self.reg = reg
    
    def set_mem(self,mem):
        self.mem = mem

class Procedure:
    def __init__(self,name):
        self.name = name
        self.call_num = 0
        self.declarations = dict() 
        self.arg_map = dict() 
        self.arg_list = [] 
        self.proc_head = ""
        self.commands = [] 

    def set_arguments(self,var_list):
        for i,var in enumerate(var_list):
            self.arg_list[i].set_var(var)
    
    def inc_call_num(self):
        self.call_num += 1    

    def set_commands(self,commands):
        self.commands = commands    
    

class Argument:
    def __init__(self,name,type,proc_name):
        self.name = name
        self.type = type
        self.proc_name = proc_name
        self.mem = None
        self.is_assigning = False

    def set_var(self,var):
        self.var = var
 

