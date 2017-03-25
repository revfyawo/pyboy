from enum import Enum
from typing import Dict
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

    def __init__(self, arg_type, dereference=False, flag="", register=""):
        self.flag = flag  # type: str
        self.register = register  # type: str
        self.dereference = dereference  # type: bool
        self.arg_type = arg_type  # type: ArgumentType

    def __repr__(self):
        string = ""
        if self.dereference:
            string += "("
        if self.arg_type == ArgumentType.REGISTER:
            string += self.register
        elif self.arg_type in (ArgumentType.FLAG_NOT_SET, ArgumentType.FLAG_SET):
            if self.arg_type == ArgumentType.FLAG_NOT_SET:
                string += "n"
            string += self.flag
        else:
            string += self.arg_type.name
        if self.dereference:
            string += ")"
        return string


class Instruction(object):
    """An opcode"""

    def __init__(self, opcode, asm, args, cycles, flags=None):
        self.flags = flags  # type: Dict[str, FlagAction]
        self.cycles = cycles  # type: int
        self.asm = asm  # type: str
        self.opcode = opcode  # type: int
        self.args = args  # type: List[Argument]

    def __index__(self):
        return self.opcode

    def __repr__(self):
        string = self.__hex() + ": " + self.asm + " "
        for arg in self.args:
            string += repr(arg) + ","
        string = string[:-1]
        return string

    def __hex(self):
        return "{:0=2X}".format(self.opcode)
