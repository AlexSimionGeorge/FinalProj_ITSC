
zero = "x0"
ra = "x1"
sp = "x2" 
pc = "x3"

def increment_pc(reg, mappingpc):
    index_in_memory = mappingpc[reg[pc]]
    index_in_memory += 1
    reg[pc] = list(mappingpc.keys())[list(mappingpc.values()).index(index_in_memory)]
    print("core.py: test")
    return reg

def return_address_to_pc(reg, mappingpc):
    index_in_memory = mappingpc[reg[ra]]
    reg[pc] = list(mappingpc.keys())[list(mappingpc.values()).index(index_in_memory)]
    return reg

def jump_and_ra(rd, offset, reg, mappingpc):
    index_in_memory_ra = mappingpc[reg[pc]]
    index_in_memory_ra += 1
    reg[rd] = list(mappingpc.keys())[list(mappingpc.values()).index(index_in_memory_ra)]
    reg[pc] = offset
    return reg

def branch_pc(offset, reg, mappingpc):
    print("______________________________________________________", offset)
    reg[pc] = offset #list(mappingpc.keys())[list(mappingpc.values()).index(mappingpc[offset])]
    return reg

def extend_sign(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def signed2unsigned(value):
    unsigned_value = value & 0x7FFFFFFF + (2**32) * (value >> 32)
    return unsigned_value

def cell2linescolumns(value):
    return (value//10, value%10)

## add ##
def add(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] + reg[rs2]
    reg = increment_pc(reg, mappingpc) 
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## add immediate value ##
def addi(rd, rs1, immediate_value, mem, reg, mappingpc):
    reg[rd] = reg[rs1] + int(immediate_value)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## sub reg to reg ##
def sub(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] - reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## LUI: Load upper immediate ##
def lui(rd, immediate_value, mem, reg, mappingpc):
    reg[rd] = immediate_value << 12
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## AND ##
def and_op(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] & reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## OR ##
def or_op(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] | reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## XOR ##
def xor_op(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] ^ reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Set less than ##
def slt(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = int(reg[rs1] < reg[rs2])
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## AUIPC: Add upper immediate to program counter ##
def auipc(rd, immediate_value, mem, reg, mappingpc):
    reg[rd] = reg[pc] + (immediate_value << 12)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Set less than immediate ##
def slti(rd, rs1, immediate_value, mem, reg, mappingpc):
    reg[rd] = int(reg[rs1] < extend_sign(immediate_value, 12))
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Set less than immediate unsigned ##
def sltiu(rd, rs1, immediate_value, mem, reg, mappingpc):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(extend_sign(immediate_value, 12) & 0xFFFFFFFF)):
        reg[rd] = 1
    else:
        reg[rd] = 0
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Set less than rs2 unsigned
def sltu(rd, rs1, rs2, mem, reg, mappingpc):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(reg[rs2])):
        reg[rd] = 1
    else:
        reg[rd] = 0
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## XOR with immediate value ##
def xori(rd, rs1, immediate_value, mem, reg, mappingpc):
    reg[rd] = reg[rs1] ^ extend_sign(immediate_value, 12)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift left logical ##
def sll(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] << reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift left logical immediate
def slli(rd, rs1, shamt, mem, reg, mappingpc):
    print("INAINTE")
    print(type(int(shamt)), rd, rs1,)
    reg[rd] = reg[rs1] << int(shamt)
    print("DUPA")
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift right logical immediate
def srli(rd, rs1, shamt, mem, reg, mappingpc):
    reg[rd] = reg[rs1] >> shamt
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift right logical ##
def srl(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = (reg[rs1] >> reg[rs2]) & 0xFFFFFFFF
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift right arithmetic ##
def sra(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] >> reg[rs2]
    if reg[rs1] < 0:  # Sign-extend the shift
        reg[rd] |= (0xFFFFFFFF << (32 - reg[rs2]))
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Shift right arithmetic immediate
def srai(rd, rs1, shamt, mem, reg, mappingpc):
    reg[rd] = reg[rs1] >> extend_sign(shamt)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Set equal ##
def seq(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = 1 if reg[rs1] == reg[rs2] else 0
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## AND immediate ##
def andi(rd, rs1, immediate_value, mem, reg, mappingpc):
    print("ANDI:", rd, rs1, immediate_value)
    print("TIP ANDI:", type(rd), type(rs1), type(immediate_value))
    reg[rd] = reg[rs1] & extend_sign(int(immediate_value), 12)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## OR immediate ##
def ori(rd, rs1, immediate_value, mem, reg, mappingpc):
    reg[rd] = reg[rs1] | extend_sign(immediate_value, 12)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## CSR Read and Write ##
def csrrw(rd, csr, rs1, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"CSRRW: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## CSR Read and Set bits in CSR
def csrrs(rd, csr, rs1, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1] or reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"csrrs: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## CSR Read and clear bits in CSR
def csrrc(rd, csr, rs1, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = reg[rs1] and not(reg[rd])
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"csrrc: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## CSR Read and Write immediate
def csrrwi(rd, csr, uimm, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = uimm and 0x0000001F
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"csrrwi: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## CSR Read and Set bits immediate in CSR
def csrrsi(rd, csr, uimm, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = (uimm and 0x0000001F) or reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"csrrsi: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## CSR Read and clear bits immediate in CSR
def csrrci(rd, csr, uimm, mem, reg, mappingpc):
    if rd != reg[zero]:
        lines, columns = cell2linescolumns(csr)
        reg[rd] = mem[lines, columns]
        mem[lines, columns] = (uimm and 0x0000001F) and not(reg[rd])
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"csrrci: {rd} = {reg[rd]}, CSR[{csr}] = {mem[csr]}")
    return mem, reg

## Stops execution
def ecall(mem, reg, mappingpc):
    exit()

## Stops execution
def ebreak(mem, reg, mappingpc):
    print( "core.py", "No debugging mode enabled")
    exit()

def ret(mem, reg, mappingpc):
    reg = return_address_to_pc(reg, mappingpc)
    reg["x5"] = 0
    reg["x6"] = 0
    reg["x7"] = 0
    reg["x28"] = 0
    reg["x29"] = 0
    reg["x30"] = 0
    reg["x31"] = 0
    return mem, reg

def uret(mem, reg, mappingpc):
    print( "core.py", "No user mode enabled")
    exit()

def sret(mem, reg, mappingpc):
    print( "core.py", "No supervised mode enabled")
    exit()

def mret(mem, reg, mappingpc):
    print( "core.py", "No memory mode enabled")
    exit()

def wfi(mem, reg, mappingpc):
    print( "core.py", "No interrups")
    exit()

## Load a 8-bit value from memory
def lb(rd, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    temp = ((temp and 0x80000000) >> 24) or (temp and 0x0000007F)
    reg[rd] = extend_sign(temp, 8)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"LB: {rd} = {reg[rd]}")
    return mem, reg

## Load a 16-bit value from memory
def lh(rd, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    temp = ((temp and 0x80000000) >> 16) or (temp and 0x00007FFF)
    reg[rd] = extend_sign(temp, 16)
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"LH: {rd} = {reg[rd]}")
    return mem, reg

## Load a 32-bit value from memory
def lw(rd, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"LW: {rd} = {reg[rd]}")
    return mem, reg

## Load a 8-bit value from memory zero-extend
def lbu(rd, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp and 0x000000FF
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"LBU: {rd} = {reg[rd]}")
    return mem, reg

## Load a 16-bit value from memory zero-extend
def lhu(rd, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = mem[lines, columns]
    reg[rd] = temp and 0x0000FFFF
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"LHU: {rd} = {reg[rd]}")
    return mem, reg

## Store a 8-bit value in memory
def sb(rs2, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = reg[rs2] and 0x000000FF
    mem[lines, columns] = temp
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"SB: mem[{lines}, {columns}] = {temp}")
    return mem, reg

## Store a 16-bit value in memory
def sh(rs2, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    temp = reg[rs2] and 0x0000FFFF
    mem[lines, columns] = temp
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"SH: mem[{lines}, {columns}] = {temp}")
    return mem, reg

## Store a 32-bit value in memory
def sw(rs2, offset, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[rs1] + extend_sign(offset, 12))
    mem[lines, columns] = reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"SW: mem[{lines}, {columns}] = {reg[rs2]}")
    return mem, reg

## Jump and link (ADRESARE DIRECTA)
def jal(rd, offset, mem, reg, mappingpc):
    reg = jump_and_ra(rd, extend_sign(offset, 20), reg, mappingpc)
    reg["x5"] = 0
    reg["x6"] = 0
    reg["x7"] = 0
    reg["x28"] = 0
    reg["x29"] = 0
    reg["x30"] = 0
    reg["x31"] = 0
    return mem, reg

## Jump and link register (ADRESARE DIRECTA)
def jalr(rd, rs1, offset, mem, reg, mappingpc):
    reg = jump_and_ra(rd, reg[rs1] + extend_sign(offset, 12), reg, mappingpc)
    reg["x5"] = 0
    reg["x6"] = 0
    reg["x7"] = 0
    reg["x28"] = 0
    reg["x29"] = 0
    reg["x30"] = 0
    reg["x31"] = 0
    return mem, reg

## take branch if rs1 == rs2 (ADRESARE DIRECTA)
def beq(rs1, rs2, offset, mem, reg, mappingpc):
    if (reg[rs1] == reg[rs2]):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)

    print("core.py", f"BEQ: {reg[pc]}, comparison: {reg[rs1]} == {reg[rs2]}")
    return mem, reg

## take branch if rs1 != rs2 (ADRESARE DIRECTA)
def bne(rs1, rs2, offset, mem, reg, mappingpc):
    if (reg[rs1] != reg[rs2]):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)
    return mem, reg

## take branch if rs1 < rs2 (ADRESARE DIRECTA)
def blt(rs1, rs2, offset, mem, reg, mappingpc):
    if (reg[rs1] < reg[rs2]):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)
    return mem, reg

## take branch if rs1 >= rs2 (ADRESARE DIRECTA)
def bge(rs1, rs2, offset, mem, reg, mappingpc):
    if (reg[rs1] >= reg[rs2]):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)
    return mem, reg

## take branch if rs1 < rs2 - unsigned (ADRESARE DIRECTA)
def bltu(rs1, rs2, offset, mem, reg, mappingpc):
    if (signed2unsigned(reg[rs1]) < signed2unsigned(reg[rs2])):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)
    return mem, reg

## take branch if rs1 >= rs2 - unsigned (ADRESARE DIRECTA)
def bgeu(rs1, rs2, offset, mem, reg, mappingpc):
    if (signed2unsigned(reg[rs1]) >= signed2unsigned(reg[rs2])):
        reg = branch_pc(extend_sign(offset,12), reg, mappingpc)
    else:
        reg = increment_pc(reg, mappingpc)
    return mem, reg

## Multiplication
def mul(rd, rs1, rs2, mem, reg, mappingpc):
    temp = reg[rs1] * reg[rs2]
    reg[rd] = temp and 0xFFFFFFFF
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Multiplication upper stored
def mulh(rd, rs1, rs2, mem, reg, mappingpc):
    temp = reg[rs1] * reg[rs2]
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Multiplication upper stored rs1 signed, rs2 unsigned
def mulhsu(rd, rs1, rs2, mem, reg, mappingpc):
    temp = reg[rs1] * signed2unsigned(reg[rs2])
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Multiplication upper stored rs1 unsigned, rs2 unsigned
def mulhu(rd, rs1, rs2, mem, reg, mappingpc):
    temp = signed2unsigned(reg[rs1]) * signed2unsigned(reg[rs2])
    reg[rd] = (temp and 0xFFFFFFFF00000000) >> 32
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Division
def div(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] // reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Division unsigned
def divu(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = signed2unsigned(reg[rs1]) // signed2unsigned(reg[rs2])
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Modulo
def rem(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = reg[rs1] % reg[rs2]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## Modulo unsigned
def remu(rd, rs1, rs2, mem, reg, mappingpc):
    reg[rd] = signed2unsigned(reg[rs1]) % signed2unsigned(reg[rs2])
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 swap with rs2
def amoswap_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    temp = reg[rd]
    reg[rd] = reg[rs2]
    reg[rs2] = temp
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 add with rs2 and load result
def amoadd_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] += reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 xor with rs2 and load result
def amoxor_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] ^ reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 and with rs2 and load result
def amoand_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] and reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 or with rs2 and load result
def amoor_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    reg[rd] = reg[rd] or reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 compared with rs2 and load min result
def amomin_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if reg[rd] > reg[rs2]:
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 compared with rs2 and load max result
def amomax_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if reg[rd] < reg[rs2]:
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 compared with rs2 and load min result - unsigned
def amominu_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if signed2unsigned(reg[rd]) > signed2unsigned(reg[rs2]):
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## memory rs1 compared with rs2 and load max result - unsigned
def amomaxu_w(rd, rs2, rs1, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(rs1)
    reg[rd] = mem[lines, columns]
    if signed2unsigned(reg[rd]) < signed2unsigned(reg[rs2]):
        reg[rd] = reg[rs2]
    mem[lines, columns] = reg[rd]
    reg = increment_pc(reg, mappingpc)
    print( "core.py", f"{rd} = {reg[rd]}")
    return mem, reg

## push in stack ## 
def push(rd, a, b, mem, reg, mappingpc):
    print( "core.py", f"{rd} = {reg[rd]}, ")
    lines, columns = cell2linescolumns(reg[sp])
    mem[lines, columns] = reg[rd]
    reg['x2'] = reg['x2']  - 1
    reg = increment_pc(reg, mappingpc) 
    return mem, reg

## pop from stack ## 
def pop(rd, mem, reg, mappingpc):
    lines, columns = cell2linescolumns(reg[sp])
    reg[rd] = mem[lines, columns]
    mem[lines, columns] = 0
    reg = increment_pc(reg, mappingpc) 
    return mem, reg

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




