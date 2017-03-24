from pyboy.instruction import Argument as Arg
from pyboy.instruction import ArgumentType as ArgType
from pyboy.instruction import Instruction, FlagAction


class InstructionTable(object):
    def __init__(self):
        self.a8 = Arg(ArgType.ADDRESS_8)
        self.a8_deref = Arg(ArgType.ADDRESS_8, dereference=True)
        self.a16 = Arg(ArgType.ADDRESS_16)
        self.a16 = Arg(ArgType.ADDRESS_16)

        self.d8 = Arg(ArgType.UNSIGNED_8)
        self.d16 = Arg(ArgType.UNSIGNED_16)
        self.r8 = Arg(ArgType.SIGNED_8)

        self.a = Arg(ArgType.REGISTER, register="A")
        self.f = Arg(ArgType.REGISTER, register="F")
        self.b = Arg(ArgType.REGISTER, register="B")
        self.c = Arg(ArgType.REGISTER, register="C")
        self.d = Arg(ArgType.REGISTER, register="D")
        self.e = Arg(ArgType.REGISTER, register="E")
        self.h = Arg(ArgType.REGISTER, register="H")
        self.l = Arg(ArgType.REGISTER, register="L")
        self.a_deref = Arg(ArgType.REGISTER, register="A", dereference=True)
        self.f_deref = Arg(ArgType.REGISTER, register="F", dereference=True)
        self.b_deref = Arg(ArgType.REGISTER, register="B", dereference=True)
        self.c_deref = Arg(ArgType.REGISTER, register="C", dereference=True)
        self.d_deref = Arg(ArgType.REGISTER, register="D", dereference=True)
        self.e_deref = Arg(ArgType.REGISTER, register="E", dereference=True)
        self.h_deref = Arg(ArgType.REGISTER, register="H", dereference=True)
        self.l_deref = Arg(ArgType.REGISTER, register="L", dereference=True)

        self.af = Arg(ArgType.REGISTER, register="AF")
        self.bc = Arg(ArgType.REGISTER, register="BC")
        self.de = Arg(ArgType.REGISTER, register="DE")
        self.hl = Arg(ArgType.REGISTER, register="HL")
        self.sp = Arg(ArgType.REGISTER, register="SP")
        self.pc = Arg(ArgType.REGISTER, register="PC")
        self.hl_dec = Arg(ArgType.REGISTER, register="HL-")
        self.hl_inc = Arg(ArgType.REGISTER, register="HL+")
        self.af_deref = Arg(ArgType.REGISTER, register="AF", dereference=True)
        self.bc_deref = Arg(ArgType.REGISTER, register="BC", dereference=True)
        self.de_deref = Arg(ArgType.REGISTER, register="DE", dereference=True)
        self.hl_deref = Arg(ArgType.REGISTER, register="HL", dereference=True)

        self.flag_z = Arg(ArgType.FLAG_SET, flag="z")
        self.flag_nz = Arg(ArgType.FLAG_NOT_SET, flag="z")
        self.flag_c = Arg(ArgType.FLAG_SET, flag="c")
        self.flag_nc = Arg(ArgType.FLAG_NOT_SET, flag="c")

        self.tables = {}
        self.create_tables()

    def create_tables(self):
        """Initialize the different tables"""
        self.create_default_instruction_table()
        self.create_prefix_cb_instruction_table()

    def create_default_instruction_table(self):
        """Initialize the default table"""
        table = [Instruction(0x00, "NOP", [], 4) for _ in range(0xFF)]
        flags = dict.fromkeys("z n h c".split(" "), FlagAction.NOT_AFFECTED)

        # 8 bits loads

        # LD REG, self.d8
        table[0x06] = Instruction(0x06, "LD", [self.b, self.d8], 8)
        table[0x0E] = Instruction(0x0E, "LD", [self.c, self.d8], 8)
        table[0x12] = Instruction(0x12, "LD", [self.d, self.d8], 8)
        table[0x1E] = Instruction(0x1E, "LD", [self.e, self.d8], 8)
        table[0x26] = Instruction(0x26, "LD", [self.h, self.d8], 8)
        table[0x2E] = Instruction(0x2E, "LD", [self.l, self.d8], 8)

        # LD REG, REG
        table[0x40] = Instruction(0x40, "LD", [self.b, self.b], 4)
        table[0x41] = Instruction(0x41, "LD", [self.b, self.c], 4)
        table[0x42] = Instruction(0x42, "LD", [self.b, self.d], 4)
        table[0x43] = Instruction(0x43, "LD", [self.b, self.e], 4)
        table[0x44] = Instruction(0x44, "LD", [self.b, self.h], 4)
        table[0x41] = Instruction(0x41, "LD", [self.b, self.l], 4)
        table[0x46] = Instruction(0x46, "LD", [self.b, self.hl_deref], 8)
        table[0x48] = Instruction(0x48, "LD", [self.c, self.b], 4)
        table[0x49] = Instruction(0x49, "LD", [self.c, self.c], 4)
        table[0x4A] = Instruction(0x4A, "LD", [self.c, self.d], 4)
        table[0x4B] = Instruction(0x4B, "LD", [self.c, self.e], 4)
        table[0x4C] = Instruction(0x4C, "LD", [self.c, self.h], 4)
        table[0x4D] = Instruction(0x4D, "LD", [self.c, self.l], 4)
        table[0x4E] = Instruction(0x4E, "LD", [self.c, self.hl_deref], 8)
        table[0x10] = Instruction(0x10, "LD", [self.d, self.b], 4)
        table[0x11] = Instruction(0x11, "LD", [self.d, self.c], 4)
        table[0x12] = Instruction(0x12, "LD", [self.d, self.d], 4)
        table[0x13] = Instruction(0x13, "LD", [self.d, self.e], 4)
        table[0x14] = Instruction(0x14, "LD", [self.d, self.h], 4)
        table[0x15] = Instruction(0x15, "LD", [self.d, self.l], 4)
        table[0x16] = Instruction(0x16, "LD", [self.d, self.hl_deref], 8)
        table[0x18] = Instruction(0x18, "LD", [self.e, self.b], 4)
        table[0x19] = Instruction(0x19, "LD", [self.e, self.c], 4)
        table[0x1A] = Instruction(0x1A, "LD", [self.e, self.d], 4)
        table[0x1B] = Instruction(0x1B, "LD", [self.e, self.e], 4)
        table[0x1C] = Instruction(0x1C, "LD", [self.e, self.h], 4)
        table[0x1D] = Instruction(0x1D, "LD", [self.e, self.l], 4)
        table[0x1E] = Instruction(0x1E, "LD", [self.e, self.hl_deref], 8)
        table[0x60] = Instruction(0x60, "LD", [self.h, self.b], 4)
        table[0x61] = Instruction(0x61, "LD", [self.h, self.c], 4)
        table[0x62] = Instruction(0x62, "LD", [self.h, self.d], 4)
        table[0x63] = Instruction(0x63, "LD", [self.h, self.e], 4)
        table[0x64] = Instruction(0x64, "LD", [self.h, self.h], 4)
        table[0x61] = Instruction(0x61, "LD", [self.h, self.l], 4)
        table[0x66] = Instruction(0x66, "LD", [self.h, self.hl_deref], 8)
        table[0x68] = Instruction(0x68, "LD", [self.l, self.b], 4)
        table[0x69] = Instruction(0x69, "LD", [self.l, self.c], 4)
        table[0x6A] = Instruction(0x6A, "LD", [self.l, self.d], 4)
        table[0x6B] = Instruction(0x6B, "LD", [self.l, self.e], 4)
        table[0x6C] = Instruction(0x6C, "LD", [self.l, self.h], 4)
        table[0x6D] = Instruction(0x6D, "LD", [self.l, self.l], 4)
        table[0x6E] = Instruction(0x6E, "LD", [self.l, self.hl_deref], 8)
        table[0x70] = Instruction(0x70, "LD", [self.hl, self.b], 8)
        table[0x71] = Instruction(0x71, "LD", [self.hl, self.c], 8)
        table[0x72] = Instruction(0x72, "LD", [self.hl, self.d], 8)
        table[0x73] = Instruction(0x73, "LD", [self.hl, self.e], 8)
        table[0x74] = Instruction(0x74, "LD", [self.hl, self.h], 8)
        table[0x71] = Instruction(0x71, "LD", [self.hl, self.l], 8)
        table[0x36] = Instruction(0x36, "LD", [self.hl, self.d8], 12)

        # Loads to register A
        table[0x78] = Instruction(0x78, "LD", [self.a, self.b], 4)
        table[0x79] = Instruction(0x79, "LD", [self.a, self.c], 4)
        table[0x7A] = Instruction(0x7A, "LD", [self.a, self.d], 4)
        table[0x7B] = Instruction(0x7B, "LD", [self.a, self.e], 4)
        table[0x7C] = Instruction(0x7C, "LD", [self.a, self.h], 4)
        table[0x7D] = Instruction(0x7D, "LD", [self.a, self.l], 4)
        table[0x0A] = Instruction(0x0A, "LD", [self.a, self.bc_deref], 8)
        table[0x1A] = Instruction(0x1A, "LD", [self.a, self.de_deref], 8)
        table[0x7E] = Instruction(0x7E, "LD", [self.a, self.hl_deref], 8)
        table[0x7A] = Instruction(0x7A, "LD", [self.a, self.a16_deref], 16)
        table[0x3E] = Instruction(0x3E, "LD", [self.a, self.d8], 8)

        # Loads from register A
        table[0x47] = Instruction(0x47, "LD", [self.b, self.a], 4)
        table[0x4F] = Instruction(0x4F, "LD", [self.c, self.a], 4)
        table[0x17] = Instruction(0x17, "LD", [self.d, self.a], 4)
        table[0x1F] = Instruction(0x1F, "LD", [self.e, self.a], 4)
        table[0x67] = Instruction(0x67, "LD", [self.h, self.a], 4)
        table[0x6F] = Instruction(0x6F, "LD", [self.l, self.a], 4)
        table[0x02] = Instruction(0x02, "LD", [self.bc_deref, self.a], 8)
        table[0x12] = Instruction(0x12, "LD", [self.de_deref, self.a], 8)
        table[0x77] = Instruction(0x77, "LD", [self.bc_deref, self.a], 8)
        table[0xEA] = Instruction(0xEA, "LD", [self.a16_deref, self.a], 16)

        # Misc Loads
        table[0x7F] = Instruction(0x7F, "LD", [self.a, self.a], 4)
        table[0xF2] = Instruction(0xF2, "LD", [self.a, self.a8_deref], 8)
        table[0xE2] = Instruction(0xE2, "LD", [self.a8_deref, self.a], 8)
        table[0x3A] = Instruction(0x3A, "LDD", [self.a, self.hl_deref], 8)
        table[0x32] = Instruction(0x32, "LDD", [self.hl_deref, self.a], 8)
        table[0x2A] = Instruction(0x2A, "LDI", [self.a, self.hl_deref], 8)
        table[0x22] = Instruction(0x22, "LDI", [self.hl_deref, self.a], 8)
        table[0xE0] = Instruction(0xE0, "LDH", [self.a8_deref, self.a], 12)
        table[0xF0] = Instruction(0xF0, "LDH", [self.a, self.a8_deref], 12)

        # 12 bits loads

        # LD REG, D12
        table[0x01] = Instruction(0x01, "LD", [self.bc, self.d16], 12)
        table[0x11] = Instruction(0x11, "LD", [self.de, self.d16], 12)
        table[0x21] = Instruction(0x21, "LD", [self.hl, self.d16], 12)
        table[0x31] = Instruction(0x31, "LD", [self.sp, self.d16], 12)

        # Misc 16 bits loads
        table[0xF9] = Instruction(0xF9, "LD", [self.sp, self.hl], 8)
        table.insert(0xF8, Instruction(0xF8, "LDHL", [self.sp, self.d8], 12, {
            'z': FlagAction.RESET, 'n': FlagAction.RESET,
            'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED
        }))
        table[0x08] = Instruction(0x08, "LD", [self.a16_deref, self.sp], 20)

        # Push
        table[0xC1] = Instruction(0xC1, "PUSH", [self.bc], 12)
        table[0xD1] = Instruction(0xD1, "PUSH", [self.de], 12)
        table[0xE1] = Instruction(0xE1, "PUSH", [self.hl], 12)
        table[0xF1] = Instruction(0xF1, "PUSH", [self.af], 12)

        # Pop
        table[0xC1] = Instruction(0xC1, "POP", [self.bc], 12)
        table[0xD1] = Instruction(0xD1, "POP", [self.de], 12)
        table[0xE1] = Instruction(0xE1, "POP", [self.hl], 12)
        table[0xF1] = Instruction(0xF1, "POP", [self.af], 12)

        # 8 bits ALU

        # ADD A, n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.AFFECTED
        table[0x87] = Instruction(0x87, "ADD", [self.a, self.a], 4, flags)
        table[0x80] = Instruction(0x80, "ADD", [self.a, self.b], 4, flags)
        table[0x81] = Instruction(0x81, "ADD", [self.a, self.c], 4, flags)
        table[0x82] = Instruction(0x82, "ADD", [self.a, self.d], 4, flags)
        table[0x83] = Instruction(0x83, "ADD", [self.a, self.e], 4, flags)
        table[0x84] = Instruction(0x84, "ADD", [self.a, self.h], 4, flags)
        table[0x85] = Instruction(0x85, "ADD", [self.a, self.l], 4, flags)
        table[0x86] = Instruction(0x86, "ADD", [self.a, self.hl_deref], 8, flags)
        table[0xC6] = Instruction(0xC6, "ADD", [self.a, self.d8], 8, flags)

        # ADC A, n
        table[0x8F] = Instruction(0x8F, "ADC", [self.a, self.a], 4, flags)
        table[0x88] = Instruction(0x88, "ADC", [self.a, self.b], 4, flags)
        table[0x89] = Instruction(0x89, "ADC", [self.a, self.c], 4, flags)
        table[0x8A] = Instruction(0x8A, "ADC", [self.a, self.d], 4, flags)
        table[0x8B] = Instruction(0x8B, "ADC", [self.a, self.e], 4, flags)
        table[0x8C] = Instruction(0x8C, "ADC", [self.a, self.h], 4, flags)
        table[0x8D] = Instruction(0x8D, "ADC", [self.a, self.l], 4, flags)
        table[0x8E] = Instruction(0x8E, "ADC", [self.a, self.hl_deref], 8, flags)
        table[0xCE] = Instruction(0xCE, "ADC", [self.a, self.d8], 8, flags)

        # SUB n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.SET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.AFFECTED
        table[0x97] = Instruction(0x97, "SUB", [self.a], 4, flags)
        table[0x90] = Instruction(0x90, "SUB", [self.b], 4, flags)
        table[0x91] = Instruction(0x91, "SUB", [self.c], 4, flags)
        table[0x92] = Instruction(0x92, "SUB", [self.d], 4, flags)
        table[0x93] = Instruction(0x93, "SUB", [self.e], 4, flags)
        table[0x94] = Instruction(0x94, "SUB", [self.h], 4, flags)
        table[0x95] = Instruction(0x95, "SUB", [self.l], 4, flags)
        table[0x96] = Instruction(0x96, "SUB", [self.hl_deref], 8, flags)
        table[0xD6] = Instruction(0xD6, "SUB", [self.d8], 8, flags)

        # SBC A, n
        table[0x9F] = Instruction(0x9F, "SBC", [self.a, self.a], 4, flags)
        table[0x98] = Instruction(0x98, "SBC", [self.a, self.b], 4, flags)
        table[0x99] = Instruction(0x99, "SBC", [self.a, self.c], 4, flags)
        table[0x9A] = Instruction(0x9A, "SBC", [self.a, self.d], 4, flags)
        table[0x9B] = Instruction(0x9B, "SBC", [self.a, self.e], 4, flags)
        table[0x9C] = Instruction(0x9C, "SBC", [self.a, self.h], 4, flags)
        table[0x9D] = Instruction(0x9D, "SBC", [self.a, self.l], 4, flags)
        table[0x9E] = Instruction(0x9E, "SBC", [self.a, self.hl_deref], 8, flags)
        table[0xDE] = Instruction(0xDE, "SBC", [self.a, self.d8], 8, flags)

        # AND n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.SET
        flags['c'] = FlagAction.RESET
        table[0xA7] = Instruction(0xA7, "AND", [self.a], 4, flags)
        table[0xA0] = Instruction(0xA0, "AND", [self.b], 4, flags)
        table[0xA1] = Instruction(0xA1, "AND", [self.c], 4, flags)
        table[0xA2] = Instruction(0xA2, "AND", [self.d], 4, flags)
        table[0xA3] = Instruction(0xA3, "AND", [self.e], 4, flags)
        table[0xA4] = Instruction(0xA4, "AND", [self.h], 4, flags)
        table[0xA5] = Instruction(0xA5, "AND", [self.l], 4, flags)
        table[0xA6] = Instruction(0xA6, "AND", [self.hl_deref], 8, flags)
        table[0xE6] = Instruction(0xE6, "AND", [self.d8], 8, flags)

        # XOR n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.RESET
        flags['c'] = FlagAction.RESET
        table[0xAF] = Instruction(0xAF, "XOR", [self.a, self.a], 4, flags)
        table[0xA8] = Instruction(0xA8, "XOR", [self.a, self.b], 4, flags)
        table[0xA9] = Instruction(0xA9, "XOR", [self.a, self.c], 4, flags)
        table[0xAA] = Instruction(0xAA, "XOR", [self.a, self.d], 4, flags)
        table[0xAB] = Instruction(0xAB, "XOR", [self.a, self.e], 4, flags)
        table[0xAC] = Instruction(0xAC, "XOR", [self.a, self.h], 4, flags)
        table[0xAD] = Instruction(0xAD, "XOR", [self.a, self.l], 4, flags)
        table[0xAE] = Instruction(0xAE, "XOR", [self.a, self.hl_deref], 8, flags)
        table[0xEE] = Instruction(0xEE, "XOR", [self.a, self.d8], 8, flags)

        # OR n
        table[0xB7] = Instruction(0xB7, "OR", [self.a], 4, flags)
        table[0xB0] = Instruction(0xB0, "OR", [self.b], 4, flags)
        table[0xB1] = Instruction(0xB1, "OR", [self.c], 4, flags)
        table[0xB2] = Instruction(0xB2, "OR", [self.d], 4, flags)
        table[0xB3] = Instruction(0xB3, "OR", [self.e], 4, flags)
        table[0xB4] = Instruction(0xB4, "OR", [self.h], 4, flags)
        table[0xB5] = Instruction(0xB5, "OR", [self.l], 4, flags)
        table[0xB6] = Instruction(0xB6, "OR", [self.hl_deref], 8, flags)
        table[0xF6] = Instruction(0xF6, "OR", [self.d8], 8, flags)

        # CP n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.SET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.AFFECTED
        table[0xB8] = Instruction(0xB8, "CP", [self.b], 4, flags)
        table[0xB9] = Instruction(0xB9, "CP", [self.c], 4, flags)
        table[0xBA] = Instruction(0xBA, "CP", [self.d], 4, flags)
        table[0xBB] = Instruction(0xBB, "CP", [self.e], 4, flags)
        table[0xBC] = Instruction(0xBC, "CP", [self.h], 4, flags)
        table[0xBD] = Instruction(0xBD, "CP", [self.l], 4, flags)
        table[0xBE] = Instruction(0xBE, "CP", [self.hl_deref], 8, flags)
        table[0xBF] = Instruction(0xBF, "CP", [self.a], 4, flags)
        table[0xFE] = Instruction(0xFE, "CP", [self.d8], 8, flags)

        # INC n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.NOT_AFFECTED
        table[0x04] = Instruction(0x04, "INC", [self.b], 4, flags)
        table[0x0C] = Instruction(0x0C, "INC", [self.c], 4, flags)
        table[0x14] = Instruction(0x14, "INC", [self.d], 4, flags)
        table[0x1C] = Instruction(0x1C, "INC", [self.e], 4, flags)
        table[0x24] = Instruction(0x24, "INC", [self.h], 4, flags)
        table[0x2C] = Instruction(0x2C, "INC", [self.l], 4, flags)
        table[0x34] = Instruction(0x34, "INC", [self.hl_deref], 12, flags)
        table[0x3C] = Instruction(0x3C, "INC", [self.a], 4, flags)

        # DEC n
        flags['z'] = FlagAction.AFFECTED
        flags['n'] = FlagAction.SET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.AFFECTED
        table[0x05] = Instruction(0x05, "INC", [self.b], 4, flags)
        table[0x0D] = Instruction(0x0D, "INC", [self.c], 4, flags)
        table[0x15] = Instruction(0x15, "INC", [self.d], 4, flags)
        table[0x1D] = Instruction(0x1D, "INC", [self.e], 4, flags)
        table[0x25] = Instruction(0x25, "INC", [self.h], 4, flags)
        table[0x2D] = Instruction(0x2D, "INC", [self.l], 4, flags)
        table[0x35] = Instruction(0x35, "INC", [self.hl_deref], 12, flags)
        table[0x3D] = Instruction(0x3D, "INC", [self.a], 4, flags)

        # 16 bits arithmetic

        # ADD HL, n
        flags['z'] = FlagAction.NOT_AFFECTED
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.AFFECTED
        flags['c'] = FlagAction.AFFECTED
        table[0x09] = Instruction(0x09, "ADD", [self.hl, self.bc], 8, flags)
        table[0x19] = Instruction(0x19, "ADD", [self.hl, self.de], 8, flags)
        table[0x29] = Instruction(0x29, "ADD", [self.hl, self.hl], 8, flags)
        table[0x39] = Instruction(0x39, "ADD", [self.hl, self.sp], 8, flags)
        flags['z'] = FlagAction.RESET
        table[0xE8] = Instruction(0xE8, "ADD", [self.sp, self.r8], 16, flags)

        # INC nn
        table[0x03] = Instruction(0x03, "INC", [self.bc], 8)
        table[0x13] = Instruction(0x13, "INC", [self.de], 8)
        table[0x23] = Instruction(0x23, "INC", [self.hl], 8)
        table[0x33] = Instruction(0x33, "INC", [self.sp], 8)

        # DEC nn
        table[0x0B] = Instruction(0x0B, "DEC", [self.bc], 8)
        table[0x1B] = Instruction(0x1B, "DEC", [self.de], 8)
        table[0x2B] = Instruction(0x2B, "DEC", [self.hl], 8)
        table[0x3B] = Instruction(0x3B, "DEC", [self.sp], 8)

        # Jumps
        table[0xC3] = Instruction(0xC3, "JP", [self.a16], 12)
        table[0xC2] = Instruction(0xC2, "JP", [self.flag_nz, self.a16], 12)
        table[0xCA] = Instruction(0xCA, "JP", [self.flag_z, self.a16], 12)
        table[0xD2] = Instruction(0xD2, "JP", [self.flag_nc, self.a16], 12)
        table[0xDA] = Instruction(0xDA, "JP", [self.flag_c, self.a16], 12)
        table[0xE9] = Instruction(0xE9, "JP", [self.hl_deref], 4)
        table[0x18] = Instruction(0x18, "JR", [self.r8], 8)
        table[0x20] = Instruction(0x20, "JR", [self.flag_nz, self.r8], 8)
        table[0x28] = Instruction(0x28, "JR", [self.flag_z, self.r8], 8)
        table[0x30] = Instruction(0x30, "JR", [self.flag_nc, self.r8], 8)
        table[0x38] = Instruction(0x38, "JR", [self.flag_c, self.r8], 8)

        # Calls
        table[0xCD] = Instruction(0xCD, "CALL", [self.a16], 12)
        table[0xC4] = Instruction(0xC4, "CALL", [self.flag_nz, self.a16], 12)
        table[0xCC] = Instruction(0xCC, "CALL", [self.flag_z, self.a16], 12)
        table[0xD4] = Instruction(0xD4, "CALL", [self.flag_nc, self.a16], 12)
        table[0xDC] = Instruction(0xDC, "CALL", [self.flag_c, self.a16], 12)

        # Restarts
        table[0xC7] = Instruction(0xC7, "RST 00H", [], 16)
        table[0xCF] = Instruction(0xCF, "RST 08H", [], 16)
        table[0xD7] = Instruction(0xD7, "RST 10H", [], 16)
        table[0xDF] = Instruction(0xDF, "RST 18H", [], 16)
        table[0xE7] = Instruction(0xE7, "RST 20H", [], 16)
        table[0xEF] = Instruction(0xEF, "RST 28H", [], 16)
        table[0xF7] = Instruction(0xF7, "RST 30H", [], 16)
        table[0xFF] = Instruction(0xFF, "RST 38H", [], 16)

        # Returns
        table[0xC9] = Instruction(0xC9, "RET", [], 8)
        table[0xC0] = Instruction(0xC0, "RET", [self.flag_nz], 8)
        table[0xC8] = Instruction(0xC8, "RET", [self.flag_z], 8)
        table[0xD0] = Instruction(0xD0, "RET", [self.flag_nc], 8)
        table[0xD8] = Instruction(0xD8, "RET", [self.flag_c], 8)
        table[0xD9] = Instruction(0xD9, "RETI", [], 8)

        # Miscellaneous
        table[0x27] = Instruction(0x27, "DAA", [], 4, {
            'z': FlagAction.AFFECTED, 'h': FlagAction.RESET, 'c': FlagAction.AFFECTED
        })
        table[0x2F] = Instruction(0x2F, "CPL", [], 4, {
            'n': FlagAction.SET, 'h': FlagAction.SET
        })
        table[0x3F] = Instruction(0x3F, "CCF", [], 4, {
            'n': FlagAction.RESET, 'h': FlagAction.RESET, 'c': FlagAction.AFFECTED
        })
        table[0x37] = Instruction(0x37, "SCF", [], 4, {
            'n': FlagAction.RESET, 'h': FlagAction.RESET, 'c': FlagAction.SET
        })
        table[0x00] = Instruction(0x00, "NOP", [], 4)
        table[0x76] = Instruction(0x76, "HALT", [], 4)
        table[0x10] = Instruction(0x10, "STOP", [], 4)
        table[0xF3] = Instruction(0xF3, "DI", [], 4)
        table[0xFB] = Instruction(0xFB, "EI", [], 4)
        table[0xCB] = Instruction(0xCB, "PREFIX CB", [], 4)

        # Rotates & Shifts
        flags['z'] = FlagAction.RESET
        flags['n'] = FlagAction.RESET
        flags['h'] = FlagAction.RESET
        flags['c'] = FlagAction.AFFECTED
        table[0x07] = Instruction(0x07, "RLCA", [], 4, flags)
        table[0x17] = Instruction(0x17, "RLA", [], 4, flags)
        table[0x0F] = Instruction(0x0F, "RRCA", [], 4, flags)
        table[0x1F] = Instruction(0x1F, "RRA", [], 4, flags)

        self.tables['default'] = table

    def create_prefix_cb_instruction_table(self):
        """Initialize "PREFIX CB" instruction table"""
        table = [Instruction(0x00, "NOP", [], 4)]

        # Rotates
        flags = dict(z=FlagAction.AFFECTED, n=FlagAction.RESET, h=FlagAction.RESET, c=FlagAction.AFFECTED)
        table[0x00] = Instruction(0x00, "RLC", [self.b], 8)
        table[0x01] = Instruction(0x01, "RLC", [self.c], 8)
        table[0x02] = Instruction(0x02, "RLC", [self.d], 8)
        table[0x03] = Instruction(0x03, "RLC", [self.e], 8)
        table[0x04] = Instruction(0x04, "RLC", [self.h], 8)
        table[0x05] = Instruction(0x05, "RLC", [self.l], 8)
        table[0x06] = Instruction(0x06, "RLC", [self.hl_deref], 16)
        table[0x07] = Instruction(0x07, "RLC", [self.a], 8)
        table[0x08] = Instruction(0x08, "RRC", [self.b], 8)
        table[0x09] = Instruction(0x09, "RRC", [self.c], 8)
        table[0x0A] = Instruction(0x0A, "RRC", [self.d], 8)
        table[0x0B] = Instruction(0x0B, "RRC", [self.e], 8)
        table[0x0C] = Instruction(0x0C, "RRC", [self.h], 8)
        table[0x0D] = Instruction(0x0D, "RRC", [self.l], 8)
        table[0x0E] = Instruction(0x0E, "RRC", [self.hl_deref], 16)
        table[0x0F] = Instruction(0x0F, "RRC", [self.a], 8)
        table[0x10] = Instruction(0x10, "RL", [self.b], 8)
        table[0x11] = Instruction(0x11, "RL", [self.c], 8)
        table[0x12] = Instruction(0x12, "RL", [self.d], 8)
        table[0x13] = Instruction(0x13, "RL", [self.e], 8)
        table[0x14] = Instruction(0x14, "RL", [self.h], 8)
        table[0x15] = Instruction(0x15, "RL", [self.l], 8)
        table[0x16] = Instruction(0x16, "RL", [self.hl_deref], 16)
        table[0x17] = Instruction(0x17, "RL", [self.a], 8)
        table[0x18] = Instruction(0x18, "RR", [self.b], 8)
        table[0x19] = Instruction(0x19, "RR", [self.c], 8)
        table[0x1A] = Instruction(0x1A, "RR", [self.d], 8)
        table[0x1B] = Instruction(0x1B, "RR", [self.e], 8)
        table[0x1C] = Instruction(0x1C, "RR", [self.h], 8)
        table[0x1D] = Instruction(0x1D, "RR", [self.l], 8)
        table[0x1E] = Instruction(0x1E, "RR", [self.hl_deref], 16)
        table[0x1F] = Instruction(0x1F, "RR", [self.a], 8)
        table[0x20] = Instruction(0x20, "SLA", [self.b], 8)
        table[0x21] = Instruction(0x21, "SLA", [self.c], 8)
        table[0x22] = Instruction(0x22, "SLA", [self.d], 8)
        table[0x23] = Instruction(0x23, "SLA", [self.e], 8)
        table[0x24] = Instruction(0x24, "SLA", [self.h], 8)
        table[0x25] = Instruction(0x25, "SLA", [self.l], 8)
        table[0x26] = Instruction(0x26, "SLA", [self.hl_deref], 16)
        table[0x27] = Instruction(0x27, "SLA", [self.a], 8)
        flags['c'] = FlagAction.RESET
        table[0x28] = Instruction(0x28, "SRA", [self.b], 8)
        table[0x29] = Instruction(0x29, "SRA", [self.c], 8)
        table[0x2A] = Instruction(0x2A, "SRA", [self.d], 8)
        table[0x2B] = Instruction(0x2B, "SRA", [self.e], 8)
        table[0x2C] = Instruction(0x2C, "SRA", [self.h], 8)
        table[0x2D] = Instruction(0x2D, "SRA", [self.l], 8)
        table[0x2E] = Instruction(0x2E, "SRA", [self.hl_deref], 16)
        table[0x2F] = Instruction(0x2F, "SRA", [self.a], 8)
        flags['c'] = FlagAction.AFFECTED
        table[0x38] = Instruction(0x38, "SRL", [self.b], 8)
        table[0x39] = Instruction(0x39, "SRL", [self.c], 8)
        table[0x3A] = Instruction(0x3A, "SRL", [self.d], 8)
        table[0x3B] = Instruction(0x3B, "SRL", [self.e], 8)
        table[0x3C] = Instruction(0x3C, "SRL", [self.h], 8)
        table[0x3D] = Instruction(0x3D, "SRL", [self.l], 8)
        table[0x3E] = Instruction(0x3E, "SRL", [self.hl_deref], 16)
        table[0x3F] = Instruction(0x3F, "SRL", [self.a], 8)

        # Swap instructions
        flags.update(zip('z n h c'.split(' '), [FlagAction.AFFECTED if not i else FlagAction.RESET for i in range(4)]))
        table[0x30] = Instruction(0x30, "SWAP", [self.b], 8)
        table[0x31] = Instruction(0x31, "SWAP", [self.c], 8)
        table[0x32] = Instruction(0x32, "SWAP", [self.d], 8)
        table[0x33] = Instruction(0x33, "SWAP", [self.e], 8)
        table[0x34] = Instruction(0x34, "SWAP", [self.h], 8)
        table[0x35] = Instruction(0x35, "SWAP", [self.l], 8)
        table[0x36] = Instruction(0x36, "SWAP", [self.hl_deref], 16)
        table[0x37] = Instruction(0x37, "SWAP", [self.a], 8)

        # Bit instructions
        flags.update(zip('z n h c'.split(' '),
                         [FlagAction.AFFECTED, FlagAction.RESET, FlagAction.SET, FlagAction.NOT_AFFECTED]))
        table[0x40] = Instruction(0x40, "BIT 0", [self.b], 8)
        table[0x41] = Instruction(0x41, "BIT 0", [self.c], 8)
        table[0x42] = Instruction(0x42, "BIT 0", [self.d], 8)
        table[0x43] = Instruction(0x43, "BIT 0", [self.e], 8)
        table[0x44] = Instruction(0x44, "BIT 0", [self.h], 8)
        table[0x45] = Instruction(0x45, "BIT 0", [self.l], 8)
        table[0x46] = Instruction(0x46, "BIT 0", [self.hl_deref], 16)
        table[0x47] = Instruction(0x47, "BIT 0", [self.a], 8)
        table[0x48] = Instruction(0x48, "BIT 1", [self.b], 8)
        table[0x49] = Instruction(0x49, "BIT 1", [self.c], 8)
        table[0x4A] = Instruction(0x4A, "BIT 1", [self.d], 8)
        table[0x4B] = Instruction(0x4B, "BIT 1", [self.e], 8)
        table[0x4C] = Instruction(0x4C, "BIT 1", [self.h], 8)
        table[0x4D] = Instruction(0x4D, "BIT 1", [self.l], 8)
        table[0x4E] = Instruction(0x4E, "BIT 1", [self.hl_deref], 16)
        table[0x4F] = Instruction(0x4F, "BIT 1", [self.a], 8)
        table[0x50] = Instruction(0x50, "BIT 2", [self.b], 8)
        table[0x51] = Instruction(0x51, "BIT 2", [self.c], 8)
        table[0x52] = Instruction(0x52, "BIT 2", [self.d], 8)
        table[0x53] = Instruction(0x53, "BIT 2", [self.e], 8)
        table[0x54] = Instruction(0x54, "BIT 2", [self.h], 8)
        table[0x55] = Instruction(0x55, "BIT 2", [self.l], 8)
        table[0x56] = Instruction(0x56, "BIT 2", [self.hl_deref], 16)
        table[0x57] = Instruction(0x57, "BIT 2", [self.a], 8)
        table[0x58] = Instruction(0x58, "BIT 3", [self.b], 8)
        table[0x59] = Instruction(0x59, "BIT 3", [self.c], 8)
        table[0x5A] = Instruction(0x5A, "BIT 3", [self.d], 8)
        table[0x5B] = Instruction(0x5B, "BIT 3", [self.e], 8)
        table[0x5C] = Instruction(0x5C, "BIT 3", [self.h], 8)
        table[0x5D] = Instruction(0x5D, "BIT 3", [self.l], 8)
        table[0x5E] = Instruction(0x5E, "BIT 3", [self.hl_deref], 16)
        table[0x5F] = Instruction(0x5F, "BIT 3", [self.a], 8)
        table[0x60] = Instruction(0x60, "BIT 4", [self.b], 8)
        table[0x61] = Instruction(0x61, "BIT 4", [self.c], 8)
        table[0x62] = Instruction(0x62, "BIT 4", [self.d], 8)
        table[0x63] = Instruction(0x63, "BIT 4", [self.e], 8)
        table[0x64] = Instruction(0x64, "BIT 4", [self.h], 8)
        table[0x65] = Instruction(0x65, "BIT 4", [self.l], 8)
        table[0x66] = Instruction(0x66, "BIT 4", [self.hl_deref], 16)
        table[0x67] = Instruction(0x67, "BIT 4", [self.a], 8)
        table[0x68] = Instruction(0x68, "BIT 5", [self.b], 8)
        table[0x69] = Instruction(0x69, "BIT 5", [self.c], 8)
        table[0x6A] = Instruction(0x6A, "BIT 5", [self.d], 8)
        table[0x6B] = Instruction(0x6B, "BIT 5", [self.e], 8)
        table[0x6C] = Instruction(0x6C, "BIT 5", [self.h], 8)
        table[0x6D] = Instruction(0x6D, "BIT 5", [self.l], 8)
        table[0x6E] = Instruction(0x6E, "BIT 5", [self.hl_deref], 16)
        table[0x6F] = Instruction(0x6F, "BIT 5", [self.a], 8)
        table[0x70] = Instruction(0x70, "BIT 6", [self.b], 8)
        table[0x71] = Instruction(0x71, "BIT 6", [self.c], 8)
        table[0x72] = Instruction(0x72, "BIT 6", [self.d], 8)
        table[0x73] = Instruction(0x73, "BIT 6", [self.e], 8)
        table[0x74] = Instruction(0x74, "BIT 6", [self.h], 8)
        table[0x75] = Instruction(0x75, "BIT 6", [self.l], 8)
        table[0x76] = Instruction(0x76, "BIT 6", [self.hl_deref], 16)
        table[0x77] = Instruction(0x77, "BIT 6", [self.a], 8)
        table[0x78] = Instruction(0x78, "BIT 7", [self.b], 8)
        table[0x79] = Instruction(0x79, "BIT 7", [self.c], 8)
        table[0x7A] = Instruction(0x7A, "BIT 7", [self.d], 8)
        table[0x7B] = Instruction(0x7B, "BIT 7", [self.e], 8)
        table[0x7C] = Instruction(0x7C, "BIT 7", [self.h], 8)
        table[0x7D] = Instruction(0x7D, "BIT 7", [self.l], 8)
        table[0x7E] = Instruction(0x7E, "BIT 7", [self.hl_deref], 16)
        table[0x7F] = Instruction(0x7F, "BIT 7", [self.a], 8)

        # Res instructions
        table[0x80] = Instruction(0x80, "RES 0", [self.b], 8)
        table[0x81] = Instruction(0x81, "RES 0", [self.c], 8)
        table[0x82] = Instruction(0x82, "RES 0", [self.d], 8)
        table[0x83] = Instruction(0x83, "RES 0", [self.e], 8)
        table[0x84] = Instruction(0x84, "RES 0", [self.h], 8)
        table[0x85] = Instruction(0x85, "RES 0", [self.l], 8)
        table[0x86] = Instruction(0x86, "RES 0", [self.hl_deref], 16)
        table[0x87] = Instruction(0x87, "RES 0", [self.a], 8)
        table[0x88] = Instruction(0x88, "RES 1", [self.b], 8)
        table[0x89] = Instruction(0x89, "RES 1", [self.c], 8)
        table[0x8A] = Instruction(0x8A, "RES 1", [self.d], 8)
        table[0x8B] = Instruction(0x8B, "RES 1", [self.e], 8)
        table[0x8C] = Instruction(0x8C, "RES 1", [self.h], 8)
        table[0x8D] = Instruction(0x8D, "RES 1", [self.l], 8)
        table[0x8E] = Instruction(0x8E, "RES 1", [self.hl_deref], 16)
        table[0x8F] = Instruction(0x8F, "RES 1", [self.a], 8)
        table[0x90] = Instruction(0x90, "RES 2", [self.b], 8)
        table[0x91] = Instruction(0x91, "RES 2", [self.c], 8)
        table[0x92] = Instruction(0x92, "RES 2", [self.d], 8)
        table[0x93] = Instruction(0x93, "RES 2", [self.e], 8)
        table[0x94] = Instruction(0x94, "RES 2", [self.h], 8)
        table[0x95] = Instruction(0x95, "RES 2", [self.l], 8)
        table[0x96] = Instruction(0x96, "RES 2", [self.hl_deref], 16)
        table[0x97] = Instruction(0x97, "RES 2", [self.a], 8)
        table[0x98] = Instruction(0x98, "RES 3", [self.b], 8)
        table[0x99] = Instruction(0x99, "RES 3", [self.c], 8)
        table[0x9A] = Instruction(0x9A, "RES 3", [self.d], 8)
        table[0x9B] = Instruction(0x9B, "RES 3", [self.e], 8)
        table[0x9C] = Instruction(0x9C, "RES 3", [self.h], 8)
        table[0x9D] = Instruction(0x9D, "RES 3", [self.l], 8)
        table[0x9E] = Instruction(0x9E, "RES 3", [self.hl_deref], 16)
        table[0x9F] = Instruction(0x9F, "RES 3", [self.a], 8)
        table[0xA0] = Instruction(0xA0, "RES 4", [self.b], 8)
        table[0xA1] = Instruction(0xA1, "RES 4", [self.c], 8)
        table[0xA2] = Instruction(0xA2, "RES 4", [self.d], 8)
        table[0xA3] = Instruction(0xA3, "RES 4", [self.e], 8)
        table[0xA4] = Instruction(0xA4, "RES 4", [self.h], 8)
        table[0xA5] = Instruction(0xA5, "RES 4", [self.l], 8)
        table[0xA6] = Instruction(0xA6, "RES 4", [self.hl_deref], 16)
        table[0xA7] = Instruction(0xA7, "RES 4", [self.a], 8)
        table[0xA8] = Instruction(0xA8, "RES 5", [self.b], 8)
        table[0xA9] = Instruction(0xA9, "RES 5", [self.c], 8)
        table[0xAA] = Instruction(0xAA, "RES 5", [self.d], 8)
        table[0xAB] = Instruction(0xAB, "RES 5", [self.e], 8)
        table[0xAC] = Instruction(0xAC, "RES 5", [self.h], 8)
        table[0xAD] = Instruction(0xAD, "RES 5", [self.l], 8)
        table[0xAE] = Instruction(0xAE, "RES 5", [self.hl_deref], 16)
        table[0xAF] = Instruction(0xAF, "RES 5", [self.a], 8)
        table[0xB0] = Instruction(0xB0, "RES 6", [self.b], 8)
        table[0xB1] = Instruction(0xB1, "RES 6", [self.c], 8)
        table[0xB2] = Instruction(0xB2, "RES 6", [self.d], 8)
        table[0xB3] = Instruction(0xB3, "RES 6", [self.e], 8)
        table[0xB4] = Instruction(0xB4, "RES 6", [self.h], 8)
        table[0xB5] = Instruction(0xB5, "RES 6", [self.l], 8)
        table[0xB6] = Instruction(0xB6, "RES 6", [self.hl_deref], 16)
        table[0xB7] = Instruction(0xB7, "RES 6", [self.a], 8)
        table[0xB8] = Instruction(0xB8, "RES 7", [self.b], 8)
        table[0xB9] = Instruction(0xB9, "RES 7", [self.c], 8)
        table[0xBA] = Instruction(0xBA, "RES 7", [self.d], 8)
        table[0xBB] = Instruction(0xBB, "RES 7", [self.e], 8)
        table[0xBC] = Instruction(0xBC, "RES 7", [self.h], 8)
        table[0xBD] = Instruction(0xBD, "RES 7", [self.l], 8)
        table[0xBE] = Instruction(0xBE, "RES 7", [self.hl_deref], 16)
        table[0xBF] = Instruction(0xBF, "RES 7", [self.a], 8)

        # Set instructions
        table[0xC0] = Instruction(0xC0, "SET 0", [self.b], 8)
        table[0xC1] = Instruction(0xC1, "SET 0", [self.c], 8)
        table[0xC2] = Instruction(0xC2, "SET 0", [self.d], 8)
        table[0xC3] = Instruction(0xC3, "SET 0", [self.e], 8)
        table[0xC4] = Instruction(0xC4, "SET 0", [self.h], 8)
        table[0xC5] = Instruction(0xC5, "SET 0", [self.l], 8)
        table[0xC6] = Instruction(0xC6, "SET 0", [self.hl_deref], 16)
        table[0xC7] = Instruction(0xC7, "SET 0", [self.a], 8)
        table[0xC8] = Instruction(0xC8, "SET 1", [self.b], 8)
        table[0xC9] = Instruction(0xC9, "SET 1", [self.c], 8)
        table[0xCA] = Instruction(0xCA, "SET 1", [self.d], 8)
        table[0xCB] = Instruction(0xCB, "SET 1", [self.e], 8)
        table[0xCC] = Instruction(0xCC, "SET 1", [self.h], 8)
        table[0xCD] = Instruction(0xCD, "SET 1", [self.l], 8)
        table[0xCE] = Instruction(0xCE, "SET 1", [self.hl_deref], 16)
        table[0xCF] = Instruction(0xCF, "SET 1", [self.a], 8)
        table[0xD0] = Instruction(0xD0, "SET 2", [self.b], 8)
        table[0xD1] = Instruction(0xD1, "SET 2", [self.c], 8)
        table[0xD2] = Instruction(0xD2, "SET 2", [self.d], 8)
        table[0xD3] = Instruction(0xD3, "SET 2", [self.e], 8)
        table[0xD4] = Instruction(0xD4, "SET 2", [self.h], 8)
        table[0xD5] = Instruction(0xD5, "SET 2", [self.l], 8)
        table[0xD6] = Instruction(0xD6, "SET 2", [self.hl_deref], 16)
        table[0xD7] = Instruction(0xD7, "SET 2", [self.a], 8)
        table[0xD8] = Instruction(0xD8, "SET 3", [self.b], 8)
        table[0xD9] = Instruction(0xD9, "SET 3", [self.c], 8)
        table[0xDA] = Instruction(0xDA, "SET 3", [self.d], 8)
        table[0xDB] = Instruction(0xDB, "SET 3", [self.e], 8)
        table[0xDC] = Instruction(0xDC, "SET 3", [self.h], 8)
        table[0xDD] = Instruction(0xDD, "SET 3", [self.l], 8)
        table[0xDE] = Instruction(0xDE, "SET 3", [self.hl_deref], 16)
        table[0xDF] = Instruction(0xDF, "SET 3", [self.a], 8)
        table[0xE0] = Instruction(0xE0, "SET 4", [self.b], 8)
        table[0xE1] = Instruction(0xE1, "SET 4", [self.c], 8)
        table[0xE2] = Instruction(0xE2, "SET 4", [self.d], 8)
        table[0xE3] = Instruction(0xE3, "SET 4", [self.e], 8)
        table[0xE4] = Instruction(0xE4, "SET 4", [self.h], 8)
        table[0xE5] = Instruction(0xE5, "SET 4", [self.l], 8)
        table[0xE6] = Instruction(0xE6, "SET 4", [self.hl_deref], 16)
        table[0xE7] = Instruction(0xE7, "SET 4", [self.a], 8)
        table[0xE8] = Instruction(0xE8, "SET 5", [self.b], 8)
        table[0xE9] = Instruction(0xE9, "SET 5", [self.c], 8)
        table[0xEA] = Instruction(0xEA, "SET 5", [self.d], 8)
        table[0xEB] = Instruction(0xEB, "SET 5", [self.e], 8)
        table[0xEC] = Instruction(0xEC, "SET 5", [self.h], 8)
        table[0xED] = Instruction(0xED, "SET 5", [self.l], 8)
        table[0xEE] = Instruction(0xEE, "SET 5", [self.hl_deref], 16)
        table[0xEF] = Instruction(0xEF, "SET 5", [self.a], 8)
        table[0xF0] = Instruction(0xF0, "SET 6", [self.b], 8)
        table[0xF1] = Instruction(0xF1, "SET 6", [self.c], 8)
        table[0xF2] = Instruction(0xF2, "SET 6", [self.d], 8)
        table[0xF3] = Instruction(0xF3, "SET 6", [self.e], 8)
        table[0xF4] = Instruction(0xF4, "SET 6", [self.h], 8)
        table[0xF5] = Instruction(0xF5, "SET 6", [self.l], 8)
        table[0xF6] = Instruction(0xF6, "SET 6", [self.hl_deref], 16)
        table[0xF7] = Instruction(0xF7, "SET 6", [self.a], 8)
        table[0xF8] = Instruction(0xF8, "SET 7", [self.b], 8)
        table[0xF9] = Instruction(0xF9, "SET 7", [self.c], 8)
        table[0xFA] = Instruction(0xFA, "SET 7", [self.d], 8)
        table[0xFB] = Instruction(0xFB, "SET 7", [self.e], 8)
        table[0xFC] = Instruction(0xFC, "SET 7", [self.h], 8)
        table[0xFD] = Instruction(0xFD, "SET 7", [self.l], 8)
        table[0xFE] = Instruction(0xFE, "SET 7", [self.hl_deref], 16)
        table[0xFF] = Instruction(0xFF, "SET 7", [self.a], 8)

        self.tables['PREFIX CB'] = table
