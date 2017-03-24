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

    def run(self, instruction):
        if instruction.asm.startswith("LD"):
            self.run_load(instruction)

    def run_load(self, instruction):
        pass
