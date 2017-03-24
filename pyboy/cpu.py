from typing import List

from pyboy.instruction import Instruction, FlagAction
from pyboy.instruction import ArgumentType as ArgType
from pyboy.instruction import Argument as Arg


class CPU(object):
    """The GameBoy CPU"""

    def __init__(self, memory):
        self.memory = memory
        registers_names = [
            'A', 'F', 'B', 'C', 'D', 'E', 'H', 'L',
            'AF', 'BC', 'DE', 'HL', 'SP', 'PC'
        ]
        self.registers = dict.fromkeys(registers_names)
        self.registers['PC'] = 0x100
        self.instructions = []  # type: List[Instruction]

        self.stopped = False
        self.halted = False
        self.interrupts_enabled = True
        self.create_instructions_table()

    def run(self, instruction):
        if instruction.asm.startswith("LD"):
            self.run_load(instruction)

    def create_instructions_table(self):
        a8 = Arg(ArgType.ADDRESS_8)
        a16 = Arg(ArgType.ADDRESS_16)
        a8_deref = Arg(ArgType.ADDRESS_8, dereference=True)
        a16_deref = Arg(ArgType.ADDRESS_16, dereference=True)

        d8 = Arg(ArgType.UNSIGNED_8)
        d12 = Arg(ArgType.UNSIGNED_16)
        r8 = Arg(ArgType.SIGNED_8)
        sp_plus_r8 = Arg(ArgType.REGISTER_PLUS_SIGNED_8, register="SP")

        a = Arg(ArgType.REGISTER, register="A")
        f = Arg(ArgType.REGISTER, register="F")
        b = Arg(ArgType.REGISTER, register="B")
        c = Arg(ArgType.REGISTER, register="C")
        d = Arg(ArgType.REGISTER, register="D")
        e = Arg(ArgType.REGISTER, register="E")
        h = Arg(ArgType.REGISTER, register="H")
        l = Arg(ArgType.REGISTER, register="L")
        a_deref = Arg(ArgType.REGISTER, register="A", dereference=True)
        f_deref = Arg(ArgType.REGISTER, register="F", dereference=True)
        b_deref = Arg(ArgType.REGISTER, register="B", dereference=True)
        c_deref = Arg(ArgType.REGISTER, register="C", dereference=True)
        d_deref = Arg(ArgType.REGISTER, register="D", dereference=True)
        e_deref = Arg(ArgType.REGISTER, register="E", dereference=True)
        h_deref = Arg(ArgType.REGISTER, register="H", dereference=True)
        l_deref = Arg(ArgType.REGISTER, register="L", dereference=True)

        af = Arg(ArgType.REGISTER, register="AF")
        bc = Arg(ArgType.REGISTER, register="BC")
        de = Arg(ArgType.REGISTER, register="DE")
        hl = Arg(ArgType.REGISTER, register="HL")
        sp = Arg(ArgType.REGISTER, register="SP")
        pc = Arg(ArgType.REGISTER, register="PC")
        hl_dec = Arg(ArgType.REGISTER, register="HL-")
        hl_inc = Arg(ArgType.REGISTER, register="HL+")
        af_deref = Arg(ArgType.REGISTER, register="AF", dereference=True)
        bc_deref = Arg(ArgType.REGISTER, register="BC", dereference=True)
        de_deref = Arg(ArgType.REGISTER, register="DE", dereference=True)
        hl_deref = Arg(ArgType.REGISTER, register="HL", dereference=True)
        sp_deref = Arg(ArgType.REGISTER, register="SP", dereference=True)
        pc_deref = Arg(ArgType.REGISTER, register="PC", dereference=True)
        hl_dec_deref = Arg(ArgType.REGISTER, register="HL-", dereference=True)
        hl_inc_deref = Arg(ArgType.REGISTER, register="HL+", dereference=True)

        flag_z = Arg(ArgType.FLAG_SET, flag="z")
        flag_nz = Arg(ArgType.FLAG_NOT_SET, flag="z")
        flag_c = Arg(ArgType.FLAG_SET, flag="c")
        flag_nc = Arg(ArgType.FLAG_NOT_SET, flag="c")

        # 8 bits loads

        # LD REG, d8
        self.instructions.append(Instruction(0x06, "LD", [b, d8], 8))
        self.instructions.append(Instruction(0x0E, "LD", [c, d8], 8))
        self.instructions.append(Instruction(0x12, "LD", [d, d8], 8))
        self.instructions.append(Instruction(0x1E, "LD", [e, d8], 8))
        self.instructions.append(Instruction(0x26, "LD", [h, d8], 8))
        self.instructions.append(Instruction(0x2E, "LD", [l, d8], 8))

        # LD REG, REG
        self.instructions.append(Instruction(0x40, "LD", [b, b], 4))
        self.instructions.append(Instruction(0x41, "LD", [b, c], 4))
        self.instructions.append(Instruction(0x42, "LD", [b, d], 4))
        self.instructions.append(Instruction(0x43, "LD", [b, e], 4))
        self.instructions.append(Instruction(0x44, "LD", [b, h], 4))
        self.instructions.append(Instruction(0x41, "LD", [b, l], 4))
        self.instructions.append(Instruction(0x46, "LD", [b, hl_deref], 8))
        self.instructions.append(Instruction(0x48, "LD", [c, b], 4))
        self.instructions.append(Instruction(0x49, "LD", [c, c], 4))
        self.instructions.append(Instruction(0x4A, "LD", [c, d], 4))
        self.instructions.append(Instruction(0x4c, "LD", [c, e], 4))
        self.instructions.append(Instruction(0x4C, "LD", [c, h], 4))
        self.instructions.append(Instruction(0x4D, "LD", [c, l], 4))
        self.instructions.append(Instruction(0x4E, "LD", [c, hl_deref], 8))
        self.instructions.append(Instruction(0x10, "LD", [d, b], 4))
        self.instructions.append(Instruction(0x11, "LD", [d, c], 4))
        self.instructions.append(Instruction(0x12, "LD", [d, d], 4))
        self.instructions.append(Instruction(0x13, "LD", [d, e], 4))
        self.instructions.append(Instruction(0x14, "LD", [d, h], 4))
        self.instructions.append(Instruction(0x15, "LD", [d, l], 4))
        self.instructions.append(Instruction(0x16, "LD", [d, hl_deref], 8))
        self.instructions.append(Instruction(0x18, "LD", [e, b], 4))
        self.instructions.append(Instruction(0x19, "LD", [e, c], 4))
        self.instructions.append(Instruction(0x1A, "LD", [e, d], 4))
        self.instructions.append(Instruction(0x1c, "LD", [e, e], 4))
        self.instructions.append(Instruction(0x1C, "LD", [e, h], 4))
        self.instructions.append(Instruction(0x1D, "LD", [e, l], 4))
        self.instructions.append(Instruction(0x1E, "LD", [e, hl_deref], 8))
        self.instructions.append(Instruction(0x60, "LD", [h, b], 4))
        self.instructions.append(Instruction(0x61, "LD", [h, c], 4))
        self.instructions.append(Instruction(0x62, "LD", [h, d], 4))
        self.instructions.append(Instruction(0x63, "LD", [h, e], 4))
        self.instructions.append(Instruction(0x64, "LD", [h, h], 4))
        self.instructions.append(Instruction(0x61, "LD", [h, l], 4))
        self.instructions.append(Instruction(0x66, "LD", [h, hl_deref], 8))
        self.instructions.append(Instruction(0x68, "LD", [l, b], 4))
        self.instructions.append(Instruction(0x69, "LD", [l, c], 4))
        self.instructions.append(Instruction(0x6A, "LD", [l, d], 4))
        self.instructions.append(Instruction(0x6c, "LD", [l, e], 4))
        self.instructions.append(Instruction(0x6C, "LD", [l, h], 4))
        self.instructions.append(Instruction(0x6D, "LD", [l, l], 4))
        self.instructions.append(Instruction(0x6E, "LD", [l, hl_deref], 8))
        self.instructions.append(Instruction(0x70, "LD", [hl, b], 8))
        self.instructions.append(Instruction(0x71, "LD", [hl, c], 8))
        self.instructions.append(Instruction(0x72, "LD", [hl, d], 8))
        self.instructions.append(Instruction(0x73, "LD", [hl, e], 8))
        self.instructions.append(Instruction(0x74, "LD", [hl, h], 8))
        self.instructions.append(Instruction(0x71, "LD", [hl, l], 8))
        self.instructions.append(Instruction(0x36, "LD", [hl, d8], 12))

        # Loads to register A
        self.instructions.append(Instruction(0x78, "LD", [a, b], 4))
        self.instructions.append(Instruction(0x79, "LD", [a, c], 4))
        self.instructions.append(Instruction(0x7A, "LD", [a, d], 4))
        self.instructions.append(Instruction(0x7B, "LD", [a, e], 4))
        self.instructions.append(Instruction(0x7C, "LD", [a, h], 4))
        self.instructions.append(Instruction(0x7D, "LD", [a, l], 4))
        self.instructions.append(Instruction(0x0A, "LD", [a, bc_deref], 8))
        self.instructions.append(Instruction(0x1A, "LD", [a, de_deref], 8))
        self.instructions.append(Instruction(0x7E, "LD", [a, hl_deref], 8))
        self.instructions.append(Instruction(0x7A, "LD", [a, a16_deref], 16))
        self.instructions.append(Instruction(0x3E, "LD", [a, d8], 8))

        # Loads from register A
        self.instructions.append(Instruction(0x47, "LD", [b, a], 4))
        self.instructions.append(Instruction(0x4F, "LD", [c, a], 4))
        self.instructions.append(Instruction(0x17, "LD", [d, a], 4))
        self.instructions.append(Instruction(0x1F, "LD", [e, a], 4))
        self.instructions.append(Instruction(0x67, "LD", [h, a], 4))
        self.instructions.append(Instruction(0x6F, "LD", [l, a], 4))
        self.instructions.append(Instruction(0x02, "LD", [bc_deref, a], 8))
        self.instructions.append(Instruction(0x12, "LD", [de_deref, a], 8))
        self.instructions.append(Instruction(0x77, "LD", [bc_deref, a], 8))
        self.instructions.append(Instruction(0xEA, "LD", [a16_deref, a], 16))

        # Misc Loads
        self.instructions.append(Instruction(0x7F, "LD", [a, a], 4))
        self.instructions.append(Instruction(0xF2, "LD", [a, a8_deref], 8))
        self.instructions.append(Instruction(0xE2, "LD", [a8_deref, a], 8))
        self.instructions.append(Instruction(0x3A, "LDD", [a, hl_deref], 8))
        self.instructions.append(Instruction(0x32, "LDD", [hl_deref, a], 8))
        self.instructions.append(Instruction(0x2A, "LDI", [a, hl_deref], 8))
        self.instructions.append(Instruction(0x22, "LDI", [hl_deref, a], 8))
        self.instructions.append(Instruction(0xE0, "LDH", [a8_deref, a], 12))
        self.instructions.append(Instruction(0xF0, "LDH", [a, a8_deref], 12))

        # 12 bits loads

        # LD REG, D12
        self.instructions.append(Instruction(0x01, "LD", [bc, d12], 12))
        self.instructions.append(Instruction(0x11, "LD", [de, d12], 12))
        self.instructions.append(Instruction(0x21, "LD", [hl, d12], 12))
        self.instructions.append(Instruction(0x31, "LD", [sp, d12], 12))

        # Misc 12 bits loads
        self.instructions.append(Instruction(0xF9, "LD", [sp, hl], 8))
        self.instructions.append(Instruction(0xF8, "LDHL", [sp, d8], 12, {
            'z': FlagAction.RESET, 'n': FlagAction.RESET,
            'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED
        }))
        self.instructions.append(Instruction(0x08, "LD", [a16_deref, sp], 20))

        # Push
        self.instructions.append(Instruction(0xC1, "PUSH", [bc], 12))
        self.instructions.append(Instruction(0xD1, "PUSH", [de], 12))
        self.instructions.append(Instruction(0xE1, "PUSH", [hl], 12))
        self.instructions.append(Instruction(0xF1, "PUSH", [af], 12))

        # Pop
        self.instructions.append(Instruction(0xC1, "POP", [bc], 12))
        self.instructions.append(Instruction(0xD1, "POP", [de], 12))
        self.instructions.append(Instruction(0xE1, "POP", [hl], 12))
        self.instructions.append(Instruction(0xF1, "POP", [af], 12))

        # 8 bits ALU

        # ADD A, n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.RESET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED}
        self.instructions.append(Instruction(0x87, "ADD", [a, a], 4, flags))
        self.instructions.append(Instruction(0x80, "ADD", [a, b], 4, flags))
        self.instructions.append(Instruction(0x81, "ADD", [a, c], 4, flags))
        self.instructions.append(Instruction(0x82, "ADD", [a, d], 4, flags))
        self.instructions.append(Instruction(0x83, "ADD", [a, e], 4, flags))
        self.instructions.append(Instruction(0x84, "ADD", [a, h], 4, flags))
        self.instructions.append(Instruction(0x85, "ADD", [a, l], 4, flags))
        self.instructions.append(Instruction(0x86, "ADD", [a, hl_deref], 8, flags))
        self.instructions.append(Instruction(0xC6, "ADD", [a, d8], 8, flags))

        # ADC A, n
        self.instructions.append(Instruction(0x8F, "ADC", [a, a], 4, flags))
        self.instructions.append(Instruction(0x88, "ADC", [a, b], 4, flags))
        self.instructions.append(Instruction(0x89, "ADC", [a, c], 4, flags))
        self.instructions.append(Instruction(0x8A, "ADC", [a, d], 4, flags))
        self.instructions.append(Instruction(0x8B, "ADC", [a, e], 4, flags))
        self.instructions.append(Instruction(0x8C, "ADC", [a, h], 4, flags))
        self.instructions.append(Instruction(0x8D, "ADC", [a, l], 4, flags))
        self.instructions.append(Instruction(0x8E, "ADC", [a, hl_deref], 8, flags))
        self.instructions.append(Instruction(0xCE, "ADC", [a, d8], 8, flags))

        # SUB n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.SET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED}
        self.instructions.append(Instruction(0x97, "SUB", [a], 4, flags))
        self.instructions.append(Instruction(0x90, "SUB", [b], 4, flags))
        self.instructions.append(Instruction(0x91, "SUB", [c], 4, flags))
        self.instructions.append(Instruction(0x92, "SUB", [d], 4, flags))
        self.instructions.append(Instruction(0x93, "SUB", [e], 4, flags))
        self.instructions.append(Instruction(0x94, "SUB", [h], 4, flags))
        self.instructions.append(Instruction(0x95, "SUB", [l], 4, flags))
        self.instructions.append(Instruction(0x96, "SUB", [hl_deref], 8, flags))
        self.instructions.append(Instruction(0xD6, "SUB", [d8], 8, flags))

        # SBC A, n
        self.instructions.append(Instruction(0x9F, "SBC", [a, a], 4, flags))
        self.instructions.append(Instruction(0x98, "SBC", [a, b], 4, flags))
        self.instructions.append(Instruction(0x99, "SBC", [a, c], 4, flags))
        self.instructions.append(Instruction(0x9A, "SBC", [a, d], 4, flags))
        self.instructions.append(Instruction(0x9B, "SBC", [a, e], 4, flags))
        self.instructions.append(Instruction(0x9C, "SBC", [a, h], 4, flags))
        self.instructions.append(Instruction(0x9D, "SBC", [a, l], 4, flags))
        self.instructions.append(Instruction(0x9E, "SBC", [a, hl_deref], 8, flags))
        self.instructions.append(Instruction(0xDE, "SBC", [a, d8], 8, flags))

        # AND n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.RESET,
                 'h': FlagAction.SET, 'c': FlagAction.RESET}
        self.instructions.append(Instruction(0xA7, "AND", [a], 4, flags))
        self.instructions.append(Instruction(0xA0, "AND", [b], 4, flags))
        self.instructions.append(Instruction(0xA1, "AND", [c], 4, flags))
        self.instructions.append(Instruction(0xA2, "AND", [d], 4, flags))
        self.instructions.append(Instruction(0xA3, "AND", [e], 4, flags))
        self.instructions.append(Instruction(0xA4, "AND", [h], 4, flags))
        self.instructions.append(Instruction(0xA5, "AND", [l], 4, flags))
        self.instructions.append(Instruction(0xA6, "AND", [hl_deref], 8, flags))
        self.instructions.append(Instruction(0xE6, "AND", [d8], 8, flags))

        # XOR n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.RESET,
                 'h': FlagAction.RESET, 'c': FlagAction.RESET}
        self.instructions.append(Instruction(0xAF, "XOR", [a, a], 4, flags))
        self.instructions.append(Instruction(0xA8, "XOR", [a, b], 4, flags))
        self.instructions.append(Instruction(0xA9, "XOR", [a, c], 4, flags))
        self.instructions.append(Instruction(0xAA, "XOR", [a, d], 4, flags))
        self.instructions.append(Instruction(0xAB, "XOR", [a, e], 4, flags))
        self.instructions.append(Instruction(0xAC, "XOR", [a, h], 4, flags))
        self.instructions.append(Instruction(0xAD, "XOR", [a, l], 4, flags))
        self.instructions.append(Instruction(0xAE, "XOR", [a, hl_deref], 8, flags))
        self.instructions.append(Instruction(0xEE, "XOR", [a, d8], 8, flags))

        # OR n
        self.instructions.append(Instruction(0xB7, "OR", [a], 4, flags))
        self.instructions.append(Instruction(0xB0, "OR", [b], 4, flags))
        self.instructions.append(Instruction(0xB1, "OR", [c], 4, flags))
        self.instructions.append(Instruction(0xB2, "OR", [d], 4, flags))
        self.instructions.append(Instruction(0xB3, "OR", [e], 4, flags))
        self.instructions.append(Instruction(0xB4, "OR", [h], 4, flags))
        self.instructions.append(Instruction(0xB5, "OR", [l], 4, flags))
        self.instructions.append(Instruction(0xB6, "OR", [hl_deref], 8, flags))
        self.instructions.append(Instruction(0xF6, "OR", [d8], 8, flags))

        # CP n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.SET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED}
        self.instructions.append(Instruction(0xBF, "CP", [a], 4, flags))
        self.instructions.append(Instruction(0xB8, "CP", [b], 4, flags))
        self.instructions.append(Instruction(0xB9, "CP", [c], 4, flags))
        self.instructions.append(Instruction(0xBA, "CP", [d], 4, flags))
        self.instructions.append(Instruction(0xBB, "CP", [e], 4, flags))
        self.instructions.append(Instruction(0xBC, "CP", [h], 4, flags))
        self.instructions.append(Instruction(0xBD, "CP", [l], 4, flags))
        self.instructions.append(Instruction(0xBE, "CP", [hl_deref], 8, flags))
        self.instructions.append(Instruction(0xFE, "CP", [d8], 8, flags))

        # INC n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.RESET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.NOT_AFFECTED}
        self.instructions.append(Instruction(0x04, "INC", [b], 4, flags))
        self.instructions.append(Instruction(0x0C, "INC", [c], 4, flags))
        self.instructions.append(Instruction(0x14, "INC", [d], 4, flags))
        self.instructions.append(Instruction(0x1C, "INC", [e], 4, flags))
        self.instructions.append(Instruction(0x24, "INC", [h], 4, flags))
        self.instructions.append(Instruction(0x2C, "INC", [l], 4, flags))
        self.instructions.append(Instruction(0x34, "INC", [hl_deref], 12, flags))
        self.instructions.append(Instruction(0x3C, "INC", [a], 4, flags))

        # DEC n
        flags = {'z': FlagAction.AFFECTED, 'n': FlagAction.SET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.NOT_AFFECTED}
        self.instructions.append(Instruction(0x04, "INC", [b], 4, flags))
        self.instructions.append(Instruction(0x0C, "INC", [c], 4, flags))
        self.instructions.append(Instruction(0x14, "INC", [d], 4, flags))
        self.instructions.append(Instruction(0x1C, "INC", [e], 4, flags))
        self.instructions.append(Instruction(0x24, "INC", [h], 4, flags))
        self.instructions.append(Instruction(0x2C, "INC", [l], 4, flags))
        self.instructions.append(Instruction(0x34, "INC", [hl_deref], 12, flags))
        self.instructions.append(Instruction(0x3C, "INC", [a], 4, flags))

        # 16 bits arithmetic

        # ADD HL, n
        flags = {'z': FlagAction.NOT_AFFECTED, 'n': FlagAction.RESET,
                 'h': FlagAction.AFFECTED, 'c': FlagAction.AFFECTED}
        self.instructions.append(Instruction(0x09, "ADD", [hl, bc], 8, flags))
        self.instructions.append(Instruction(0x19, "ADD", [hl, de], 8, flags))
        self.instructions.append(Instruction(0x29, "ADD", [hl, hl], 8, flags))
        self.instructions.append(Instruction(0x39, "ADD", [hl, sp], 8, flags))
        flags['z'] = FlagAction.RESET
        self.instructions.append(Instruction(0xE8, "ADD", [sp, r8], 16, flags))

        # INC nn
        self.instructions.append(Instruction(0x03, "INC", [bc], 8))
        self.instructions.append(Instruction(0x13, "INC", [de], 8))
        self.instructions.append(Instruction(0x23, "INC", [hl], 8))
        self.instructions.append(Instruction(0x33, "INC", [sp], 8))

        # DEC nn
        self.instructions.append(Instruction(0x0B, "DEC", [bc], 8))
        self.instructions.append(Instruction(0x1B, "DEC", [de], 8))
        self.instructions.append(Instruction(0x2B, "DEC", [hl], 8))
        self.instructions.append(Instruction(0x3B, "DEC", [sp], 8))

        # Jumps
        self.instructions.append(Instruction(0xC3, "JP", [a16], 12))
        self.instructions.append(Instruction(0xC2, "JP", [flag_nz, a16], 12))
        self.instructions.append(Instruction(0xCA, "JP", [flag_z, a16], 12))
        self.instructions.append(Instruction(0xD2, "JP", [flag_nc, a16], 12))
        self.instructions.append(Instruction(0xDA, "JP", [flag_c, a16], 12))
        self.instructions.append(Instruction(0xE9, "JP", [hl_deref], 4))
        self.instructions.append(Instruction(0x18, "JR", [r8], 8))
        self.instructions.append(Instruction(0x20, "JR", [flag_nz, r8], 8))
        self.instructions.append(Instruction(0x28, "JR", [flag_z, r8], 8))
        self.instructions.append(Instruction(0x30, "JR", [flag_nc, r8], 8))
        self.instructions.append(Instruction(0x38, "JR", [flag_c, r8], 8))

    def run_load(self, instruction):
        pass
