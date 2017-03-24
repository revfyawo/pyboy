from pyboy.instruction import Instruction
from pyboy.instructiontable import InstructionTable


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
        self.instructions = InstructionTable()

        self.stopped = False
        self.halted = False
        self.interrupts_enabled = True
        self.prefixed = False

    def exec(self, opcode: int) -> None:
        if self.prefixed:
            instruction = self.instructions.tables['PREFIX CB'][opcode]
            asm = instruction.asm
        else:
            instruction = self.instructions.tables['default'][opcode]
            asm = instruction.asm

        if asm == "CB":
            self.prefixed = True
            return
        elif asm.startswith("LD"):
            self.exec_load(instruction)
        elif asm == "PUSH":
            self.exec_push(instruction)
        elif asm == "POP":
            self.exec_pop(instruction)
        elif asm in ("ADD", "ADC"):
            self.exec_add(instruction)
        elif asm in ("SUB", "SBC"):
            self.exec_sub(instruction)
        elif asm == "AND":
            self.exec_and(instruction)
        elif asm == "OR":
            self.exec_or(instruction)
        elif asm == "XOR":
            self.exec_xor(instruction)
        elif asm == "CP":
            self.exec_cp(instruction)
        elif asm == "INC":
            self.exec_inc(instruction)
        elif asm == "DEC":
            self.exec_dec(instruction)
        elif asm == "JP":
            self.exec_jp(instruction)
        elif asm == "CALL":
            self.exec_call(instruction)
        elif asm in ("RET", "RETI"):
            self.exec_ret(instruction)
        elif asm == "RST":
            self.exec_rst(instruction)
        elif asm in ("RR", "RRA", "RRC", "RRCA", "SRA", "SRL"):
            self.exec_shiftr(instruction)
        elif asm in ("RL", "RLA", "RLC", "RLCA", "SLA"):
            self.exec_shiftl(instruction)
        elif asm == "SWAP":
            self.exec_swap(instruction)
        elif asm == "BIT":
            self.exec_bit(instruction)
        elif asm == "RES":
            self.exec_res(instruction)
        elif asm == "SET":
            self.exec_set(instruction)
        else:
            self.exec_misc(instruction)

    def exec_load(self, instruction: Instruction) -> None:
        pass

    def exec_push(self, instruction: Instruction) -> None:
        pass

    def exec_pop(self, instruction: Instruction) -> None:
        pass

    def exec_add(self, instruction: Instruction) -> None:
        pass

    def exec_sub(self, instruction: Instruction) -> None:
        pass

    def exec_and(self, instruction: Instruction) -> None:
        pass

    def exec_or(self, instruction: Instruction) -> None:
        pass

    def exec_xor(self, instruction: Instruction) -> None:
        pass

    def exec_cp(self, instruction: Instruction) -> None:
        pass

    def exec_inc(self, instruction: Instruction) -> None:
        pass

    def exec_dec(self, instruction: Instruction) -> None:
        pass

    def exec_jp(self, instruction: Instruction) -> None:
        pass

    def exec_call(self, instruction: Instruction) -> None:
        pass

    def exec_ret(self, instruction: Instruction) -> None:
        pass

    def exec_rst(self, instruction: Instruction) -> None:
        pass

    def exec_shiftr(self, instruction: Instruction) -> None:
        pass

    def exec_shiftl(self, instruction: Instruction) -> None:
        pass

    def exec_swap(self, instruction: Instruction) -> None:
        pass

    def exec_bit(self, instruction: Instruction) -> None:
        pass

    def exec_res(self, instruction: Instruction) -> None:
        pass

    def exec_set(self, instruction: Instruction) -> None:
        pass

    def exec_misc(self, instruction: Instruction) -> None:
        pass
