import unittest

reg = {f"R{i}": 0 for i in range(32)}
mem = {(line, column): 0 for line in range(37) for column in range(10)}

gp = "R3"
sp = "R2"
reg[gp] = 0
reg[sp] = 369

def extend_sign(value, bits=12):
    mask = (1 << bits) - 1
    if value & (1 << (bits - 1)):
        return value | ~mask
    return value & mask

def signed2unsigned(value):
    return value & 0xFFFFFFFF

def jal(rd, offset):
    reg[rd] = reg[gp] + 1
    reg[gp] += offset
    reg["R5"] = reg["R6"] = reg["R7"] = reg["R28"] = reg["R29"] = reg["R30"] = reg["R31"] = 0

def jalr(rd, rs1, offset):
    reg[rd] = reg[gp] + 1
    reg[gp] = (reg[rs1] + extend_sign(offset, 12)) & ~1
    reg["R5"] = reg["R6"] = reg["R7"] = reg["R28"] = reg["R29"] = reg["R30"] = reg["R31"] = 0

def beq(rs1, rs2, offset):
    if reg[rs1] == reg[rs2]:
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

def bne(rs1, rs2, offset):
    if reg[rs1] != reg[rs2]:
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

def blt(rs1, rs2, offset):
    if reg[rs1] < reg[rs2]:
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

def bge(rs1, rs2, offset):
    if reg[rs1] >= reg[rs2]:
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

def bltu(rs1, rs2, offset):
    if signed2unsigned(reg[rs1]) < signed2unsigned(reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

def bgeu(rs1, rs2, offset):
    if signed2unsigned(reg[rs1]) >= signed2unsigned(reg[rs2]):
        reg[gp] += extend_sign(offset)
    else:
        reg[gp] += 1

class TestRiscVInstructions(unittest.TestCase):

    def setUp(self):
        global reg, gp, sp
        reg = {f"R{i}": 0 for i in range(32)}
        gp = "R3"
        sp = "R2"
        reg[gp] = 0
        reg[sp] = 369

    def test_jal(self):
        jal("R1", 4)
        self.assertEqual(reg["R1"], 1)
        self.assertEqual(reg[gp], 4)

    def test_jalr(self):
        reg["gp"] = 0
        reg["R1"] = 100
        jalr("R3", "R1", 8)
        self.assertEqual(reg["R3"], 108)

    def test_beq(self):
        reg["R1"] = 10
        reg["R2"] = 10
        beq("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 5
        beq("R1", "R2", 4)
        self.assertEqual(reg[gp], 1)

    def test_bne(self):
        reg["R1"] = 10
        reg["R2"] = 5
        bne("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 10
        bne("R1", "R2", 4)
        self.assertEqual(reg[gp], 1)

    def test_blt(self):
        reg["R1"] = 5
        reg["R2"] = 10
        blt("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 5
        blt("R1", "R2", 4)
        self.assertEqual(reg[gp], 1)

    def test_bge(self):
        reg["R1"] = 10
        reg["R2"] = 5
        bge("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 10
        bge("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)

    def test_bltu(self):
        reg["R1"] = 5
        reg["R2"] = 10
        bltu("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 5
        bltu("R1", "R2", 4)
        self.assertEqual(reg[gp], 1)

    def test_bgeu(self):
        reg["R1"] = 10
        reg["R2"] = 5
        bgeu("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)
        reg[gp] = 0
        reg["R2"] = 10
        bgeu("R1", "R2", 4)
        self.assertEqual(reg[gp], 4)

if __name__ == "__main__":
    unittest.main()
