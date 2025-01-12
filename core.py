reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

pc = 0
gp = "gp" 


reg[gp] = 0  

def extend_sign(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def signed2unsigned(value):
    unsigned_value = value & 0x7FFFFFFF + (2**32) * (value >> 32)
    return unsigned_value

## add ##
def add(rd, rs1, rs2):
    reg[rd] = reg[rs1] + reg[rs2]
    reg[gp] += 1  
    print(f"{rd} = {reg[rd]}")


## add immediate value ##
def addi(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] + immediate_value
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## sub reg to reg ##
def sub(rd, rs1, rs2):
    reg[rd] = reg[rs1] - reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## LUI: Load upper immediate ##
def lui(rd, immediate_value):
    reg[rd] = immediate_value << 12
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## AND ##
def and_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] & reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## OR ##
def or_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] | reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## XOR ##
def xor_op(rd, rs1, rs2):
    reg[rd] = reg[rs1] ^ reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## Set less than ##
def slt(rd, rs1, rs2):
    reg[rd] = int(reg[rs1] < reg[rs2])
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## AUIPC: Add upper immediate to program counter ##
def auipc(rd, immediate_value):
    reg[rd] = pc + (immediate_value << 12)
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## Set less than immediate ##
def slti(rd, rs1, immediate_value):
    reg[rd] = int(reg[rs1] < extend_sign(immediate_value, 12))
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## Set less than immediate unsigned ## 
def sltiu(rd, rs1, immediate_value):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(extend_sign(immediate_value, 12) & 0xFFFFFFFF)):
        reg[rd] = 1
    else:
        reg[rd] = 0 
    reg[gp] += 4
    print(f"{rd} = {reg[rd]}")

## Set less than rs2 unsigned ## NOT IN DICT YET ////////////////////////////////////////////////////////
def sltu(rd, rs1, rs2):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(reg[rs2])):
        reg[rd] = 1
    else:
        reg[rd] = 0 
    reg[gp] += 4
    print(f"{rd} = {reg[rd]}")


## XOR with immediate value ##
def xori(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] ^ extend_sign(immediate_value, 12)
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## Shift left logical ##
def sll(rd, rs1, rs2):
    reg[rd] = reg[rs1] << reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Shift left logical immediate ## NOT IN DICT YET ////////////////////////////////////////////////////////
def slli(rd, rs1, shamt):
    reg[rd] = reg[rs1] << shamt
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Shift right logical immediate ## NOT IN DICT YET ////////////////////////////////////////////////////////
def srli(rd, rs1, shamt):
    reg[rd] = reg[rs1] >> shamt
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Shift right logical ## 
def srl(rd, rs1, rs2):
    reg[rd] = (reg[rs1] >> reg[rs2]) & 0xFFFFFFFF
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## Shift right arithmetic ##
def sra(rd, rs1, rs2):
    reg[rd] = reg[rs1] >> reg[rs2]
    if reg[rs1] < 0:  # Sign-extend the shift 
        reg[rd] |= (0xFFFFFFFF << (32 - reg[rs2]))
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Shift right arithmetic immediate ## NOT IN DICT YET ////////////////////////////////////////////////////////
def srai(rd, rs1, shamt):
    reg[rd] = reg[rs1] >> reg[rs2]
    if reg[rs1] < 0:  # Sign-extend the shift
        reg[rd] |= (0xFFFFFFFF << (32 - shamt))
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Set equal ##
def seq(rd, rs1, rs2):
    reg[rd] = 1 if reg[rs1] == reg[rs2] else 0
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## AND immediate ##
def andi(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] & extend_sign(immediate_value, 12)
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## OR immediate ##
def ori(rd, rs1, immediate_value):
    reg[rd] = reg[rs1] | extend_sign(immediate_value, 12)
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## CSR Read and Write ##
def csrrw(rd, csr, rs1):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = reg[rs1]
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Set bits in CSR ## NOT IN DICT YET ////////////////////////////////////////////////////////
def csrrs(rd, csr, rs1):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = reg[rs1] or reg[rd]
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and clear bits in CSR ## NOT IN DICT YET ////////////////////////////////////////////////////////
def csrrc(rd, csr, rs1):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = reg[rs1] and not(reg[rd])
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Write immediate ## NOT IN DICT YET ////////////////////////////////////////////////////////
def csrrwi(rd, csr, uimm):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = uimm and 0x0000001F
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Set bits immediate in CSR ## NOT IN DICT YET ////////////////////////////////////////////////////////
def csrrsi(rd, csr, uimm):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = (uimm and 0x0000001F) or reg[rd]
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and clear bits immediate in CSR ## NOT IN DICT YET ////////////////////////////////////////////////////////
def csrrci(rd, csr, uimm):
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = (uimm and 0x0000001F) and not(reg[rd])
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

##  ## NOT IN DICT YET ////////////////////////////////////////////////////////
def ecall():
    if rd != "R0":
        reg[rd] = mem.get(csr, 0)
        mem[csr] = (uimm and 0x0000001F) and not(reg[rd])
    reg[gp] += 1
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
        "110": ori
    },
    "1110011": csrrw,
}


def use(instr, opers):
    instr_set = {
        "ADD": add,
        "ADDi": addi,
        "SUB": sub
    }
    
    op = instr_set.get(instr)
    if op:
        op(*opers)
    else:
        print("Unknown instruction")


reg["R0"] = 5
reg["R1"] = 15
use("ADD", ["R2", "R0", "R1"])  # Example usage
