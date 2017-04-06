from pyboy.instruction import Instruction
from pyboy.instruction import ArgumentType as ArgType
from pyboy.instructiontable import InstructionTable


class OpcodeException(BaseException):
    pass


class CPU(object):
    """The GameBoy CPU"""

    def __init__(self, memory):
        self.memory = memory
        registers_names = [
            'A', 'F', 'B', 'C', 'D', 'E', 'H', 'L',
            'AF', 'BC', 'DE', 'HL', 'SP', 'PC'
        ]
        self.registers = dict.fromkeys(registers_names, 0)
        self.registers['PC'] = 0x100
        self.registers['SP'] = 0xFFFE
        self.instructions = InstructionTable()

        self.stopped = False
        self.halted = False
        self.interrupts_enabled = True
        self.prefixed = False

    def exec_next(self):
        self.exec(self.get_next_byte())

    def exec(self, opcode: int) -> None:
        if self.prefixed:
            instruction = self.instructions.tables['PREFIX CB'][opcode]
            self.prefixed = False
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
        store_to = instruction.args[0]
        store_from = instruction.args[1]
        value = 0
        asm = instruction.asm
        opcode = instruction.opcode
        # differentiate between the different load instructions
        if asm == "LD":
            if store_to.arg_type == ArgType.REGISTER:
                if store_from.arg_type == ArgType.REGISTER:
                    if store_from.dereference:
                        value = self.memory[self.registers[store_from.register]]
                    else:
                        value = self.registers[store_from.register]
                elif store_from.arg_type == ArgType.UNSIGNED_8:
                    value = self.get_next_byte()
                elif store_from.arg_type == ArgType.UNSIGNED_16:
                    value = self.get_next_byte()
                    value += self.get_next_byte() << 8
                elif store_from.arg_type == ArgType.ADDRESS_16 and store_from.dereference:
                    address = self.get_next_byte()
                    address += self.get_next_byte() << 8
                    value = self.memory[address]

                if store_to.dereference:
                    if store_to.register == "C":
                        self.memory[0xFF00 + self.registers["C"]] = value
                    else:
                        self.memory[self.registers[store_to.register]] = value
                else:
                    self.registers[store_to.register] = value
            elif store_to.arg_type == ArgType.ADDRESS_16 and store_to.dereference:
                address = self.get_next_byte() + (self.get_next_byte() << 8)
                self.memory[address] = self.registers[store_from.register]
            else:
                raise OpcodeException("{} not implemented".format(repr(instruction)))
        elif asm in ("LDD", "LDI"):
            if store_to.register == "A":
                self.registers["A"] = self.memory[self.registers["HL"]]
            else:
                self.memory[self.registers["HL"]] = self.registers["A"]
            self.registers["HL"] += 1 if asm == "LDI" else -1
        elif opcode == 0xE0:  # LDH (a8),A
            self.memory[0xFF00 + self.get_next_byte()] = self.registers["A"]
        elif opcode == 0xF0:  # LDH A,(a8)
            self.registers["A"] = self.memory[0xFF00 + self.get_next_byte()]
        elif asm == "LDHL": # LD HL, SP+n
            self.registers["HL"] = self.registers["SP"] + self.signed(self.get_next_byte())
        else:
            raise OpcodeException("{} not implemented".format(repr(instruction)))

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

    def get_next_byte(self):
        value = self.memory[self.registers['PC']]
        self.registers['PC'] += 1
        return value

    @staticmethod
    def signed(byte):
        if byte > 0x80:
            return (byte & 0x7F) - 128
        return byte
