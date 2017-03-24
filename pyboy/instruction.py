from enum import Enum
from typing import List


class FlagAction(Enum):
    SET = "force set"
    RESET = "force reset"
    AFFECTED = "affected as expected by its function"
    NOT_AFFECTED = "not affected at all"


class ArgumentType(Enum):
    SIGNED_8 = "8 bits signed immediate data"
    UNSIGNED_8 = "immediate 8 bits data"
    UNSIGNED_16 = "immediate 16 bits data"
    REGISTER = "register name"
    REGISTER_PLUS_SIGNED_8 = "register value with a value added"
    ADDRESS_8 = "8 bits unsigned data added to 0xFF00 to get an actual address"
    ADDRESS_16 = "16 bits address"
    FLAG_SET = "condition : the flag is set"
    FLAG_NOT_SET = "condition : the flag is not set"


class Argument(object):
    """An argument : an argument type and a bool"""

    def __init__(self, arg_type, dereference=False, flag="", register=''):
        self.flag = flag
        self.register = register
        self.dereference = dereference
        self.arg_type = arg_type


class Instruction(object):
    """An opcode"""

    def __init__(self, opcode, asm, args, cycles, flags={}):
        self.flags = flags
        self.cycles = cycles
        self.asm = asm  # type: str
        self.opcode = opcode  # type: int
        self.args = args  # type: List[Argument]
