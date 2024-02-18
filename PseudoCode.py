c = 0



def load_var(var,reg):
    codeBlock = []
    codeBlock += load_from_mem(var,0,reg)
        
    return codeBlock

def save_to_mem(reg,var,of): 
    codeBlock = []
    if reg != 'a':
        codeBlock.append(f"PUT {reg}")
    codeBlock += load_num(var.mem + of,'h')
    codeBlock.append("STORE h")
    return codeBlock


def load_from_mem(var,of,reg):
    codeBlock = []
    codeBlock += load_num(var.mem + of,reg)
    codeBlock.append(f"LOAD {reg}")
    if reg != 'a':
        codeBlock.append(f"PUT {reg}")
    return codeBlock


def load_arr(var1,var2,reg):
    codeBLock = []
    codeBLock += load_var(var2,'h') 
    
    codeBLock += load_num(var1.mem,'a') 
    
    codeBLock.append("ADD h")
    codeBLock.append("LOAD a")
    if reg != 'a':
        codeBLock.append(f"PUT {reg}")
    return codeBLock

def save_arr(reg,var1,var2): 
    codeBlock = []
    if reg != 'a' and reg != 'g':
        codeBlock.append(f"GET {reg}")
    if reg != 'g':
        codeBlock.append("PUT g") 
        
    codeBlock += load_var(var2,'h') 
    codeBlock += load_num(var1.mem,'a')  
    codeBlock.append("ADD h")
    codeBlock.append("PUT h")
    codeBlock.append("GET g")
    codeBlock.append("STORE h")
    return codeBlock


def gen_expression(op, k = 0):
    codeBlock = []
    if op == '+':
        codeBlock.append("ADD h")
    elif op == '-':
        codeBlock.append("SUB h")
    elif op == '*':
        codeBlock += make_mult(k)
    elif op == '/':
        codeBlock += make_div(k)
    elif op == '%': 
        codeBlock += make_mod(k)

    return codeBlock




"""
def multiply_log(a, b):
    result = 0

    while b > 0:
        if b % 2 == 1:
            result += a
        a *= 2
        b //= 2

    return result
"""

def make_mult(k):
    codeBlock = []   
    codeBlock.append("PUT g")
    codeBlock.append("SUB h") 
    codeBlock.append(f"JPOS {k+6}")
    codeBlock.append("GET h")     
    codeBlock.append("PUT f")  
    codeBlock.append(f"JPOS {k+10}")  
    codeBlock.append("GET g")  
    codeBlock.append("PUT f")
    codeBlock.append("GET h")
    codeBlock.append("PUT g")
    codeBlock.append("RST h")  
    codeBlock.append("GET g")  
    codeBlock.append(f"JZERO {k+24}")
    codeBlock.append("SHR a")  
    codeBlock.append("SHL a") 
    codeBlock.append("INC a") 
    codeBlock.append("SUB g")  
    codeBlock.append(f"JPOS {k+21}") 
    codeBlock.append("GET h")
    codeBlock.append("ADD f")
    codeBlock.append("PUT h")
    codeBlock.append("SHL f")
    codeBlock.append("SHR g")
    codeBlock.append(f"JUMP {k+11}")
    codeBlock.append("GET h")
    return codeBlock


"""
def div_log(a,b):
    result = 0
    while a >= b:
        power = 1
        div = b
        while a >= div*2:
            div *= 2
            power *= 2
        a -= div
        result += power
    return result
"""    

def make_div(k):
    codeBlock = []
    codeBlock.append("PUT f")
    codeBlock.append("GET h")
    codeBlock.append(f"JZERO {k+26}")
    codeBlock.append("PUT g")
    codeBlock.append("RST h")
    codeBlock.append("GET g")
    codeBlock.append("SUB f")
    codeBlock.append(f"JPOS {k + 26}")
    codeBlock.append("RST e")
    codeBlock.append("INC e")
    codeBlock.append("GET g")
    codeBlock.append("PUT d")
    codeBlock.append("GET d")
    codeBlock.append("SHL a")
    codeBlock.append("SUB f")
    codeBlock.append(f"JPOS {k + 19}")
    codeBlock.append("SHL d")
    codeBlock.append("SHL e")
    codeBlock.append(f"JUMP {k + 12}")
    codeBlock.append("GET f")
    codeBlock.append("SUB d")
    codeBlock.append("PUT f")   
    codeBlock.append("GET h")
    codeBlock.append("ADD e")
    codeBlock.append("PUT h")
    codeBlock.append(f"JUMP {k + 5}")
    codeBlock.append("GET h")
    return codeBlock


"""
def mod_log(a, b):
    while a >= b:
        power = 1
        div = b
        while a >= div * 2:
            div *= 2
            power *= 2
        a -= div
    return a
"""
def make_mod(k):
    codeBlock = []
    codeBlock.append("PUT f")
    codeBlock.append("GET h")
    codeBlock.append(f"JZERO {k+23}")
    codeBlock.append("PUT g")
    codeBlock.append("GET g")
    codeBlock.append("SUB f")
    codeBlock.append(f"JPOS {k + 22}")
    codeBlock.append("RST e")
    codeBlock.append("INC e")
    codeBlock.append("GET g")
    codeBlock.append("PUT d")
    codeBlock.append("GET d")
    codeBlock.append("SHL a")
    codeBlock.append("SUB f")
    codeBlock.append(f"JPOS {k + 18}")
    codeBlock.append("SHL d")
    codeBlock.append("SHL e")
    codeBlock.append(f"JUMP {k + 11}")
    codeBlock.append("GET f")
    codeBlock.append("SUB d")
    codeBlock.append("PUT f")   
    codeBlock.append(f"JUMP {k + 4}")
    codeBlock.append("GET f")
    codeBlock.append("RST h") 
    return codeBlock






def prep_num(num):
    bin_r = bin(num)[2:]
    ones = 0
    l = []
    for i in bin_r:
        if i == '1':
            ones+= 1
        if i == '0':
            if ones > 0:
                l.append(ones)
            l.append(0)
            ones = 0
    if ones > 0:
        l.append(ones)

    return l

def load_num(num, reg):
    codeBlock = []
    b = prep_num(num)
    if b[0] == 0:
        codeBlock.append(f"RST {reg}")
        return codeBlock
    if b[0] < 3:
        codeBlock.append(f"RST {reg}")
        for i in range(b[0]):
            if i != 0:
                codeBlock.append(f"SHL {reg}")
            codeBlock.append(f"INC {reg}")
    else:
        codeBlock.append(f"RST {reg}")
        codeBlock.append(f"INC {reg}")
        for i in range(b[0]):
            codeBlock.append(f"SHL {reg}")
        codeBlock.append(f"DEC {reg}")

    for a in b[1:]:
        if a == 0 :
            codeBlock.append(f"SHL {reg}")
        elif a == 1 :
            codeBlock.append(f"SHL {reg}")
            codeBlock.append(f"INC {reg}")
        elif a == 2 :
            codeBlock.append(f"SHL {reg}")
            codeBlock.append(f"INC {reg}")
            codeBlock.append(f"SHL {reg}")
            codeBlock.append(f"INC {reg}")
        
        elif  a > 2:    
            codeBlock.append(f"INC {reg}")
            for i in range(a):
                codeBlock.append(f"SHL {reg}")
            codeBlock.append(f"DEC {reg}")    

    return codeBlock

