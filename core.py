reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

gp = "R3"
sp = "R2"
reg[gp] = 0
reg[sp] = 369  

def extend_sign(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def signed2unsigned(value):
    unsigned_value = value & 0x7FFFFFFF + (2**32) * (value >> 32)
    return unsigned_value

def cell2linescolumns(value):
    return value/10, value%10

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

## Set less than rs2 unsigned  
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

## Shift left logical immediate  
def slli(rd, rs1, shamt):
    reg[rd] = reg[rs1] << shamt
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Shift right logical immediate  
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

## Shift right arithmetic immediate  
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
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1]
    reg[gp] += 1
    print(f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Set bits in CSR  
def csrrs(rd, csr, rs1):
    if rd != "R0":
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1] or reg[rd]
    reg[gp] += 1
    print(f"csrrs: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and clear bits in CSR  
def csrrc(rd, csr, rs1):
    if rd != "R0":
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1] and not(reg[rd])
    reg[gp] += 1
    print(f"csrrc: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Write immediate  
def csrrwi(rd, csr, uimm):
    if rd != "R0":
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = uimm and 0x0000001F
    reg[gp] += 1
    print(f"csrrwi: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and Set bits immediate in CSR  
def csrrsi(rd, csr, uimm):
    if rd != "R0":
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = (uimm and 0x0000001F) or reg[rd]
    reg[gp] += 1
    print(f"csrrsi: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## CSR Read and clear bits immediate in CSR  
def csrrci(rd, csr, uimm):
    if rd != "R0":
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = (uimm and 0x0000001F) and not(reg[rd])
    reg[gp] += 1
    print(f"csrrci: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")

## Stops execution  
def ecall():
    exit()

## Stops execution  
def ebreak():
    print("No debugging mode enabled")
    exit()

def ret():
    reg[gp] = reg["R1"]
    reg["R5"] = 0
    reg["R6"] = 0
    reg["R7"] = 0
    reg["R28"] = 0
    reg["R29"] = 0
    reg["R30"] = 0
    reg["R31"] = 0

def uret():
    print("No user mode enabled")
    exit()

def sret():
    print("No supervised mode enabled")
    exit()

def mret():
    print("No memory mode enabled")
    exit()

def wfi():
    print("No interrups")
    exit()

## Load a 8-bit value from memory  
def lb(rd, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    temp = ((temp and 0x80000000) >> 24) or (temp and 0x0000007F)
    reg[rd] = extend_sign(temp, 8)
    reg[gp] += 1
    print(f"LB: {rd} = {reg[rd]}")

## Load a 16-bit value from memory  
def lh(rd, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    temp = ((temp and 0x80000000) >> 16) or (temp and 0x00007FFF)
    reg[rd] = extend_sign(temp, 16)
    reg[gp] += 1
    print(f"LH: {rd} = {reg[rd]}")

## Load a 32-bit value from memory  
def lw(rd, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp
    reg[gp] += 1
    print(f"LW: {rd} = {reg[rd]}")

## Load a 8-bit value from memory zero-extend  
def lbu(rd, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp and 0x000000FF
    reg[gp] += 1
    print(f"LBU: {rd} = {reg[rd]}")

## Load a 16-bit value from memory zero-extend  
def lhu(rd, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp and 0x0000FFFF
    reg[gp] += 1
    print(f"LHU: {rd} = {reg[rd]}")

## Store a 8-bit value in memory  
def sb(rs2, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = reg[rs2] and 0x000000FF
    mem[lines, columns] = temp
    reg[gp] += 1
    print(f"SB: mem[{lines}, {columns}] = {temp}")

## Store a 16-bit value in memory  
def sh(rs2, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = reg[rs2] and 0x0000FFFF
    mem[lines, columns] = temp
    reg[gp] += 1
    print(f"SH: mem[{lines}, {columns}] = {temp}")

## Store a 32-bit value in memory  
def sw(rs2, offset, rs1):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    mem[lines, columns] = reg[rs2]
    reg[gp] += 1
    print(f"SW: mem[{lines}, {columns}] = {reg[rs2]}")

## Jump and link (ADRESARE INDIRECTA) 
def jal(rd, offset):
    reg[rd] = reg[gp] + 1
    reg[gp] += offset ############################################# MUST CHANGE TO ADDRESS LABEL
    reg["R5"] = 0
    reg["R6"] = 0
    reg["R7"] = 0
    reg["R28"] = 0
    reg["R29"] = 0
    reg["R30"] = 0
    reg["R31"] = 0

## Jump and link register (ADRESARE DIRECTA) 
def jalr(rd, rs1, offset):
    reg[rd] = reg[gp] + 1
    reg[gp] = reg[rs1] + extend_sign(offset, 12)#################### MUST CHANGE TO ADDRESS LABEL
    reg["R5"] = 0
    reg["R6"] = 0
    reg["R7"] = 0
    reg["R28"] = 0
    reg["R29"] = 0
    reg["R30"] = 0
    reg["R31"] = 0

## take branch if rs1 == rs2 (ADRESARE INDIRECTA) 
def beq(rs1, rs2, offset):
    if (reg[rs1] == reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## take branch if rs1 != rs2 (ADRESARE INDIRECTA) 
def bne(rs1, rs2, offset):
    if (reg[rs1] != reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## take branch if rs1 < rs2 (ADRESARE INDIRECTA) 
def blt(rs1, rs2, offset):
    if (reg[rs1] < reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## take branch if rs1 >= rs2 (ADRESARE INDIRECTA) 
def bge(rs1, rs2, offset):
    if (reg[rs1] >= reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## take branch if rs1 < rs2 - unsigned (ADRESARE INDIRECTA) 
def bltu(rs1, rs2, offset):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(reg[rs2])):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## take branch if rs1 >= rs2 - unsigned (ADRESARE INDIRECTA) 
def bgeu(rs1, rs2, offset):
    if (signed2unsigned(reg[rs1]) >= signed2unsigned(reg[rs2])):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

## Multiplication  
def mul(rd, rs1, rs2):
    temp = reg[rs1] * reg[rs2]
    reg[rd] = temp and 0xFFFFFFFF 
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Multiplication upper stored  
def mulh(rd, rs1, rs2):
    temp = reg[rs1] * reg[rs2]
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Multiplication upper stored rs1 signed, rs2 unsigned  
def mulhsu(rd, rs1, rs2):
    temp = reg[rs1] * signed2unsigned(reg[rs2])
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Multiplication upper stored rs1 unsigned, rs2 unsigned  
def mulhu(rd, rs1, rs2):
    temp = signed2unsigned(reg[rs1]) * signed2unsigned(reg[rs2])
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Division  
def div(rd, rs1, rs2):
    reg[rd] = reg[rs1] / reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Division unsigned  
def divu(rd, rs1, rs2):
    reg[rd] = signed2unsigned(reg[rs1]) / signed2unsigned(reg[rs2])
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Modulo  
def rem(rd, rs1, rs2):
    reg[rd] = reg[rs1] % reg[rs2]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## Modulo unsigned  
def remu(rd, rs1, rs2):
    reg[rd] = signed2unsigned(reg[rs1]) % signed2unsigned(reg[rs2])
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 swap with rs2  
def amoswap_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    temp = reg[rd]
    reg[rd] = reg[rs2]
    reg[rs2] = temp
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 add with rs2 and load result  
def amoadd_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] += reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 xor with rs2 and load result  
def amoxor_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] ^ reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 and with rs2 and load result  
def amoand_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] and reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 or with rs2 and load result  
def amoor_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] or reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")


## memory rs1 compared with rs2 and load min result  
def amomin_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if reg[rd] > reg[rs2]:
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 compared with rs2 and load max result  
def amomax_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if reg[rd] < reg[rs2]:
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 compared with rs2 and load min result - unsigned  
def amominu_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if signed2unsigned(reg[rd]) > signed2unsigned(reg[rs2]):
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## memory rs1 compared with rs2 and load max result - unsigned  
def amomaxu_w(rd, rs2, rs1):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if signed2unsigned(reg[rd]) < signed2unsigned(reg[rs2]):
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg[gp] += 1
    print(f"{rd} = {reg[rd]}")

## push in stack ## NOT IN DICT YET ////////////////////////////////////////////////////////
def push(rd):
    lines, columns = cell2linescolumns(reg[sp])
    mem[lines, columns] = reg[rd]
    reg[sp] -= 1

## pop from stack ## NOT IN DICT YET ////////////////////////////////////////////////////////
def pop(rd):
    lines, columns = cell2linescolumns(reg[sp])
    reg[rd] = mem[lines, columns]
    mem[lines, columns] = 0
    reg[sp] += 1

instruction_set = {
    "0000011": {
        "000": lb,
        "001": lh,
        "010": lw,
        "100": lbu,
        "101": lhu,
    },
    "0010011": {  
        "000": addi,
        "001": slli,
        "010": slti,
        "011": sltiu,
        "100": xori,
        "101": {
            "00000" : srli,
            "01000" : srai,
        },
        "110": ori,
        "111": andi
    },
    "0010111": auipc,
    "0101111": {
        "010": {
            "00000": amoadd_w,
            "00001": amoswap_w,
            "00100": amoxor_w,
            "01000": amoor_w,
            "01100": amoand_w,
            "10000": amomin_w,
            "10100": amomax_w,
            "11000": amominu_w,
            "11100": amomaxu_w,
        },
    },
    "0100011": {
        "000": sb,
        "001": sh,
        "010": sw, 
    },
    "0110011": {  
        "0000000": {
            "000": add,
            "001": sll,
            "010": slt,
            "011": sltu,
            "100": xor_op,
            "101": srl,
            "110": or_op,
            "111": and_op,
        },
        "0000001": {
            "000": mul,
            "001": mulh,
            "010": mulhsu,
            "011": mulhu,
            "100": div,
            "101": divu,
            "110": rem,
            "111": remu,
        },
        "0100000": {
            "000": sub,
            "101": sra,
            "110": push, 
            "111": pop, 
        },
    },
    "0110111": lui,
    "1100011": {
        "000": beq,
        "001": bne,
        "100": blt,
        "101": bge,
        "110": bltu,
        "111": bgeu,
    },
    "1100111": jalr,
    "1101111": jal,
    "1110011": {
        "000": {
            "00000": ecall,
            "00001": ebreak,
            "00010": {
                "00000": uret,
                "00010": sret,
                "00110": mret,
                "00101": wfi,
                "10000": ret,
            },
        },
        "001": csrrw,
        "010": csrrs,
        "011": csrrc,
        "101": csrrwi,
        "110": csrrsi,
        "111": csrrci
    }
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



