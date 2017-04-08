from enum import Enum


class MBC(object):
    """ Memory Bank Controller - Handles the extra ROM and/or RAM present in the cartridge """
    class BankType(Enum):
        ROM = 'rom bank'
        RAM = 'ram bank'

    def switch_bank(self, bank_type=BankType.ROM, bank_number=1):
        """ switches which internal memory bank is visible to the cpu (through the memory) """
        pass

    @classmethod
    def infer_from_rom(cls, rom_file_path):
        """ Creates the proper MBC instance from byte 0x147 of the cartridge """
        pass
