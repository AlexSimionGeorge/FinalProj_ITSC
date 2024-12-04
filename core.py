reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

pc = 0

def extend_sign(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


## add ##
def add(rd, rs1, rs2):
    reg[rd] = reg[rs1] + reg[rs2]
    print(f"{rd} = {reg[rd]}")


##add immediate value##
def addi(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] + immediate_value
    print(f"{rd} = {reg[rd]}")


##sub reg to reg##
def sub(rd, rs1, rs2):
    reg[rd] = reg[rs1] - reg[rs2]
    print(f"{rd} = {reg[rd]}")


## Build 32-bit constants and uses the U-type format. LUI places the U-immediate value in the top 20 bits of the destination register rd, filling in the lowest 12 bits with zeros. ##
def lui(rd, immediate_value):
    reg[rd] = immediate_value << 12
    print(f"{rd} = {reg[rd]}")


## and ##
def and_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] & reg[rs2]
    print(f"{rd} = {reg[rd]}")


## or ##
def or_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] | reg[rs2]
    print(f"{rd} = {reg[rd]}")


## xor ##
def xor_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] ^ reg[rs2]
    print(f"{rd} = {reg[rd]}")


## Place the value 1 in register rd if register rs1 is less than register rs2 when both are treated as unsigned numbers, else 0 is written to rd. ##
def slt(rd, rs1, rs2):
    reg[rd] = int(reg[rs1] < reg[rs2])
    print(f"{rd} = {reg[rd]}")
 
 
## load upped immediate ##
def lui(rd, immediate_value): 
    reg[rd] = immediate_value << 12
    print(f"{rd} = {reg[rd]}")


## add upper immediate to program counter ##
def auipc(rd, immediate_value):
    reg[rd] = pc + (immediate_value << 12)
    print(f"{rd} = {reg[rd]}")


## set less than immediate ##
def slti(rd, rs1, immediate_value):
    reg[rd] = int(reg[rs1] < extend_sign(immediate_value, 12))
    print(f"{rd} = {reg[rd]}")


## set less than immediate but unsigned ##
def sltiu(rd, rs1, immediate_value):
    reg[rd] = int((reg[rs1] & 0xFFFFFFFF) < (extend_sign(immediate_value, 12) & 0xFFFFFFFF))
    print(f"{rd} = {reg[rd]}")


## xor with immediate value ##
def xori(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] ^ extend_sign(immediate_value, 12)
    print(f"{rd} = {reg[rd]}")


## shift left logical ##
def sll(rd, rs1, rs2):
    reg[rd] = reg[rs1] << reg[rs2]
    print(f"{rd} = {reg[rd]}")

## shift right logical ## 
def srl(rd, rs1, rs2):
    reg[rd] = (reg[rs1] >> reg[rs2]) & 0xFFFFFFFF
    print(f"{rd} = {reg[rd]}")

## shift right arithmetic ##
def sra(rd, rs1, rs2):
    reg[rd] = reg[rs1] >> reg[rs2]
    if reg[rs1] < 0:  # Sign-extend the shift
        reg[rd] |= (0xFFFFFFFF << (32 - reg[rs2]))
    print(f"{rd} = {reg[rd]}")
    
## set equal ##
def seq(rd, rs1, rs2):
    reg[rd] = 1 if reg[rs1] == reg[rs2] else 0
    print(f"{rd} = {reg[rd]}")


## and immediate ##

def andi(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] & extend_sign(immediate_value, 12)
    print(f"{rd} = {reg[rd]}")
    
    
## or immediate value ##
def ori(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] | extend_sign(immediate_value, 12)
    print(f"{rd} = {reg[rd]}")
    
    
def csrrw(rd, csr, rs1):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = reg[rs1]
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    
    

instruction_set = {
    "0110111": lui,
    "0010111": auipc,
    "0110011": {  
        "0000000_000": add,
        "0100000_000": sub,
        "0000000_111": and_op, 
        "0000000_110": or_op,
        "0000000_100": xor_op,
        "0000000_010": slt,
        "0000000_001": sll, 
        "0000001_001": srl,
        "0100000_001": sra, 
    },
    "0010011": {  
        "000": addi,
        "010": slti,
        "011": sltiu,
        "100": xori,
        "111": andi,
        "110": ori,
        "101": xori
         
    },
    "0110111": lui,
    "1110011": csrrw,
}















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
