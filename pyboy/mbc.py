""" Memory Bank Controller - Handles the extra ROM and/or RAM present in the cartridge """


def fromROM(rom_file_path: str):
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
        self.rom = [[0] * 2**14] * 128  # 2**14 = 16 * 2**10 = 16KB
        self.ram = [[0] * 2**13] * 4  # etc
        self.ram_enabled = False
        self.mode = 'rom banking'

        # "switched-in" ROM & RAM banks
        self._romi_lower_5_bits = 1
        self._romi_upper_2_bits = 0
        self.rami = 0

        super().__init__()

    @property
    def romi(self):
        """The rom bank 7 bit id is stored separably as it's 5 lower and 2 upper bits"""
        return self._romi_lower_5_bits + (self._romi_upper_2_bits << 5)

    def __len__(self):
        return (2**6 + 1) * 2**15  # 2MB + 32KB

    def __getitem__(self, address: int):
        if 0 <= address < 0x4000:
            return self.rom[0][address]
        elif 0x4000 <= address < 0x8000:
            return self.rom[self.romi][address % 0x3fff]  # each ROM bank is addressed from 0x0000 to 0x3fff
        elif 0xa000 <= address < 0xc0000:
            return self.ram[self.rami if (self.mode == 'ram banking') else 0][address % 0x3fff]
        else:
            raise IndexError("MBC received invalid address : {}".format(str(address)))

    def __setitem__(self, address: int, value: int):
        """See http://bgb.bircd.org/pandocs.htm#mbc1max2mbyteromandor32kbyteram for a detailed list of the
        different "control zones" (address intervals) the MBC1 uses"""
        if address < 0x2000:
            self.ram_enabled = (value & 0x0f == 0x0a)
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
        elif 0xa000 <= address < 0xc000:
            if self.ram_enabled:
                self.ram[self.rami] = value


class MBC2(object):
    """
    MBC2: 256KB ROM, 2KB RAM
    256KB ROM / 16 KB bank size = 16 ROM banks
    2KB RAM / 4 bits bank size = 512 RAM banks
    This MBC only has 4 physical data lines linking it with the cpu via the cartridge,
    thus the 4 bit RAM banks size and the 2**4 ROM banks
    (This is basically a ROM-heavy, RAM-light cartridge)
    """

    def __init__(self):
        self.rom = [[0] * 2**14] * 16  # see MBC1
        self.ram = [[0] * 4] * 512
        self.ram_enabled = False
        # "switched-in" banks
        self.romi = 1
        self.rami = 0

    def __len__(self):
        return (2**8 + 1) * 2**10  # 256KB ROM + 2KB RAM

    def __getitem__(self, address: int):
        if 0 <= address < 0x4000:
            return self.rom[0][address]
        elif 0x4000 <= address < 0x8000:
            return self.rom[self.romi][address % 0x3fff]  # each ROM bank is addressed from 0x0000 to 0x3fff
        elif 0xa000 <= address < 0xa200:
            # only the last 4 bits are transmitted, the rest are
            # supposed to be ignored by the game's programmer
            return 0xf0 | self.ram[self.rami][address % 0x3fff]
        else:
            raise IndexError("MBC received invalid address : {}".format(str(address)))

    def __setitem__(self, address: int, value: int):
        """See http://bgb.bircd.org/pandocs.htm#mbc1max2mbyteromandor32kbyteram for a detailed list of the
        different "control zones" (address intervals) the MBC1 uses"""
        if 0 <= address < 0x2000:
            # 0x0a written in lower 4 bits enables, all others disable
            self.ram_enabled = (0x0f & value == 0x0a)
        elif 0x2000 <= address < 0x4000:
            # lsb of upper byte must be 1
            if 0x10 & value == 0x10:
                self.romi = 0x0f & value  # lower 4 bits == bank number
                # ROM bank 0 can never be mapped to the switchable
                if self.romi == 0:
                    self.romi = 1
        elif 0xa000 <= address < 0xa200:
            # only the last 4 bits are received
            self.ram[self.rami] = 0xf & value
