import unittest

def extend_sign(value, bits):
    """Extend sign for a given value and bit width."""
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def cell2address(address):
    """Map address directly to memory index."""
    return address % len(mem)

def increment_pc(reg, mappingpc):
    """Increment the program counter."""
    reg[mappingpc] += 1
    return reg

## Load an 8-bit value from memory (sign-extended)
def lb(rd, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    temp = mem[addr]
    reg[rd] = extend_sign(temp & 0xFF, 8)
    reg = increment_pc(reg, mappingpc)
    print(f"LB: {rd} = {reg[rd]}")
    return mem, reg

## Load a 16-bit value from memory (sign-extended)
def lh(rd, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    temp = mem[addr] | (mem[addr + 1] << 8)
    reg[rd] = extend_sign(temp & 0xFFFF, 16)
    reg = increment_pc(reg, mappingpc)
    print(f"LH: {rd} = {reg[rd]}")
    return mem, reg

## Load a 32-bit value from memory
def lw(rd, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    temp = (
        mem[addr]
        | (mem[addr + 1] << 8)
        | (mem[addr + 2] << 16)
        | (mem[addr + 3] << 24)
    )
    reg[rd] = temp
    reg = increment_pc(reg, mappingpc)
    print(f"LW: {rd} = {reg[rd]}")
    return mem, reg

## Load an 8-bit value from memory (zero-extended)
def lbu(rd, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    reg[rd] = mem[addr] & 0xFF
    reg = increment_pc(reg, mappingpc)
    print(f"LBU: {rd} = {reg[rd]}")
    return mem, reg

## Load a 16-bit value from memory (zero-extended)
def lhu(rd, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    temp = mem[addr] | (mem[addr + 1] << 8)
    reg[rd] = temp & 0xFFFF
    reg = increment_pc(reg, mappingpc)
    print(f"LHU: {rd} = {reg[rd]}")
    return mem, reg

## Store an 8-bit value in memory
def sb(rs2, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    mem[addr] = reg[rs2] & 0xFF
    reg = increment_pc(reg, mappingpc)
    print(f"SB: mem[{addr}] = {mem[addr]}")
    return mem, reg

## Store a 16-bit value in memory
def sh(rs2, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    mem[addr] = reg[rs2] & 0xFF
    mem[addr + 1] = (reg[rs2] >> 8) & 0xFF
    reg = increment_pc(reg, mappingpc)
    print(f"SH: mem[{addr}] = {mem[addr]} | mem[{addr + 1}] = {mem[addr + 1]}")
    return mem, reg

## Store a 32-bit value in memory
def sw(rs2, offset, rs1, mem, reg, mappingpc):
    addr = cell2address(reg[rs1] + extend_sign(offset, 12))
    mem[addr] = reg[rs2] & 0xFF
    mem[addr + 1] = (reg[rs2] >> 8) & 0xFF
    mem[addr + 2] = (reg[rs2] >> 16) & 0xFF
    mem[addr + 3] = (reg[rs2] >> 24) & 0xFF
    reg = increment_pc(reg, mappingpc)
    print(f"SW: mem[{addr}] = {reg[rs2]}")
    return mem, reg

## Unit tests
class TestMemoryInstructions(unittest.TestCase):

    def setUp(self):
        global reg, mem, gp, sp, mappingpc
        reg = {f"R{i}": 0 for i in range(32)}
        mem = [0] * 1024  # Linear memory of 1024 bytes
        gp = "R3"
        sp = "R2"
        mappingpc = gp  # Assume GP as the program counter for simplicity
        reg[gp] = 0
        reg[sp] = 369

    def test_lb(self):
        mem[25] = 0x81  # Memory contains a signed 8-bit value
        reg["R1"] = 35
        lb("R4", -10, "R1", mem, reg, gp)
        self.assertEqual(reg["R4"], -127)

    def test_lh(self):
        mem[25] = 0x01
        mem[26] = 0x80  # Memory contains a signed 16-bit value
        reg["R1"] = 35
        lh("R4", -10, "R1", mem, reg, gp)
        self.assertEqual(reg["R4"], -32767)

    def test_lw(self):
        mem[25] = 0xEF
        mem[26] = 0xCD
        mem[27] = 0xAB
        mem[28] = 0x89  # Memory contains a 32-bit value
        reg["R1"] = 35
        lw("R4", -10, "R1", mem, reg, gp)
        self.assertEqual(reg["R4"], 0x89ABCDEF)

    def test_lbu(self):
        mem[25] = 0xFF  # Memory contains an unsigned 8-bit value
        reg["R1"] = 35
        lbu("R4", -10, "R1", mem, reg, gp)
        self.assertEqual(reg["R4"], 255)

    def test_lhu(self):
        mem[25] = 0xFF
        mem[26] = 0xFF  # Memory contains an unsigned 16-bit value
        reg["R1"] = 35
        lhu("R4", -10, "R1", mem, reg, gp)
        self.assertEqual(reg["R4"], 65535)

    def test_sb(self):
        reg["R2"] = 0xAB
        reg["R1"] = 35
        sb("R2", -10, "R1", mem, reg, gp)
        self.assertEqual(mem[25], 0xAB)

    def test_sh(self):
        reg["R2"] = 0x1234
        reg["R1"] = 35
        sh("R2", -10, "R1", mem, reg, gp)
        self.assertEqual(mem[25], 0x34)
        self.assertEqual(mem[26], 0x12)

    def test_sw(self):
        reg["R2"] = 0xDEADBEEF
        reg["R1"] = 35
        sw("R2", -10, "R1", mem, reg, gp)
        self.assertEqual(mem[25], 0xEF)
        self.assertEqual(mem[26], 0xBE)
        self.assertEqual(mem[27], 0xAD)
        self.assertEqual(mem[28], 0xDE)

if __name__ == "__main__":
    unittest.main()