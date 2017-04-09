from enum import Enum


""" Memory Bank Controller - Handles the extra ROM and/or RAM present in the cartridge """


class BankType(Enum):
    """Represents either a ROM bank or a RAM bank in a GameBoy cartridge.
    Controlled by the MBC"""
    ROM = 'rom bank'
    RAM = 'ram bank'


def infer_mbc_from_rom(rom_file_path: str):
    """ Creates the proper MBC instance from byte 0x147 of the cartridge """
    pass


class MBC1(object):
    """
    MBC1: 2MB ROM, 32KB RAM
    2MB ROM / 16KB bank size = 128 ROM banks
    32KB RAM / 8KB bank size = 4 RAM banks
    RAM must be enabled before use
    Must switch between 2 different modes to access RAM and switch between certain ROM banks
    """
    def __init__(self):
        self.rom = [[0] * 2**14] * 128 # 2**14 = 16 * 2**10 = 16KB
        self.ram = [[0] * 2**13] * 4   # etc
        self.ram_enabled = False
        self.mode = 'rom banking'

        # "switched-in" ROM & RAM banks
        self._romi_lower_5_bits = 1
        self._romi_upper_2_bits = 0
        self.rami = 0

    @property
    def romi(self):
        """The rom bank 7 bit id is stored separably as it's 5 lower and 2 upper bits"""
        return self._romi_lower_5_bits + (self._romi_upper_2_bits << 5)

    def __getitem__(self, address: int):
        if address < 0x4000:
            return self.rom[0][address]
        elif address < 0x8000:
            return self.rom[self.romi][address % 0x3fff]  # each ROM bank is addressed from 0x0000 to 0x3fff
        elif 0xa000 <= address < 0xc0000:
            return self.ram[self.rami if (self.mode == 'ram banking') else 0][address % 0x3fff]
        else:
            raise Exception("MBC received invalid address : {}".format(str(address)))

    def __setitem__(self, address, value):
        """See http://bgb.bircd.org/pandocs.htm#mbc1max2mbyteromandor32kbyteram for a detailed list of the
        different "control zones" (address intervals) the MBC1 uses"""
        if address < 0x2000:
            self.ram_enabled = (value & 0xff == 0x0a)
        elif address < 0x4000:
            self._romi_lower_5_bits = value & 0b11111
            # ROM bank 0 can never be mapped to the switchable
            if self._romi_lower_5_bits == 0:
                self._romi_lower_5_bits = 1
        elif address < 0x6000:
            if self.mode == 'rom':
                self._romi_upper_2_bits = value & 0b11
            else:
                self.rami = value & 0b11
        elif address < 0x8000:
            if value & 0b1 == 1:
                self.mode = 'ram banking'
                self._romi_upper_2_bits = 0
            else:
                self.mode = 'rom banking'


class MBC2(MBC1):
    """MBC2"""
    pass
