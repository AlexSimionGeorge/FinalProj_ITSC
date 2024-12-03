reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}



def add(rd, rs1, rs2):
    reg[rd] = reg[rs1] + reg[rs2]
    print(reg[rd])
        
def addi(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] + immediate_value
    print(reg[rd])
        
def sub(rd, rs1, rs2):
    reg[rd] = reg[rs1] - reg[rs2]
    print(reg[rd])

  
def use(instr, opers):
        instr_set = {
            "ADD": add,
            "ADDi":addi,
            "SUB":sub
        }
        
        op = instr_set.get(instr)
        if(op):
            op(*opers)
        else:
            print("Unknown line ")



reg["R0"] = 5
reg["R1"] = 15
use("xad", ["R3", "R0", "R1"])
