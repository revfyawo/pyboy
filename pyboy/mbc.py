""" Memory Bank Controller - Handles the extra ROM and/or RAM present in the cartridge """
from enum import Enum


class CartridgeType(Enum):
    """The different cartridge types as indicated by the 0x147th byte in the cartridge rom"""
    ROM_ONLY = 0
    ROM_MBC1 = 1
    ROM_MBC1_RAM = 2
    ROM_MBC1_RAM_BATT = 3
    ROM_MBC2 = 5
    ROM_MBC2_BATTERY = 6
    ROM_RAM = 8
    ROM_RAM_BATTERY = 9
    ROM_MMM01 = 0xb
    ROM_MMM01_SRAM = 0xc
    ROM_MMM01_SRAM_BATT = 0xd
    ROM_MBC3_TIMER_BATT = 0xF
    ROM_MBC3_TIMER_RAM_BATT = 0x10
    ROM_MBC3 = 0x11
    ROM_MBC3_RAM = 0x12
    ROM_MBC3_RAM_BATT = 0x13
    ROM_MBC5 = 0x19
    ROM_MBC5_RAM = 0x1a
    ROM_MBC5_RAM_BATT = 0x1b
    ROM_MBC5_RUMBLE = 0x1c
    ROM_MBC5_RUMBLE_SRAM = 0x1d
    ROM_MBC5_RUMBLE_SRAM_BATT = 0x1e
    Pocket_Camera = 0x1f
    Bandai_TAMA5 = 0xfd
    Hudson_HuC_3 = 0xfe
    Hudson_HuC_1 = 0xff


def fromROM(rom_file_path: str):
    """ Creates the proper MBC instance from byte 0x147 of the cartridge """
    with open(rom_file_path, 'rb') as rom:
        # skip to cartridge type indicator
        rom.seek(0x147)
        cart_type = int(rom.read(1).hex(), 16)
        rom_size = int(rom.read(1).hex(), 16)
        ram_size = int(rom.read(1).hex(), 16)

        if rom_size == 0x52:
            num_rom_banks = 72
        elif rom_size == 0x53:
            num_rom_banks = 80
        elif rom_size == 0x54:
            num_rom_banks = 96
        else:
            num_rom_banks = 2**(rom_size + 1)  # this is valid for 0 <= rom_size <= 6

        num_ram_banks = 0
        if 1 <= ram_size <= 2:
            num_ram_banks = 1
        elif ram_size == 3:
            num_ram_banks = 4
        elif ram_size == 4:
            num_ram_banks = 16

    if cart_type == CartridgeType.ROM_ONLY:
        return ROMOnly()
    elif cart_type in (CartridgeType.ROM_MBC1, CartridgeType.ROM_MBC1_RAM, CartridgeType.ROM_MBC1_RAM_BATT):
        return MBC1(num_rom_banks, num_ram_banks)
    elif cart_type in (CartridgeType.ROM_MBC2, CartridgeType.ROM_MBC2_BATTERY):
        return MBC2(num_rom_banks)
    elif cart_type in (CartridgeType.ROM_MBC3, CartridgeType.ROM_MBC3_RAM, CartridgeType.ROM_MBC3_RAM_BATT):
        return MBC3(num_rom_banks, num_rom_banks, RTC=False)
    elif cart_type in (CartridgeType.ROM_MBC3_TIMER_BATT, CartridgeType.ROM_MBC3_TIMER_RAM_BATT):
        return MBC3(num_rom_banks, num_ram_banks, RTC=True)
    elif cart_type in (CartridgeType.ROM_MBC5,
                       CartridgeType.ROM_MBC5_RAM,
                       CartridgeType.ROM_MBC5_RAM_BATT,
                       CartridgeType.ROM_MBC5_RUMBLE,
                       CartridgeType.ROM_MBC5_RUMBLE_SRAM,
                       CartridgeType.ROM_MBC5_RUMBLE_SRAM_BATT):
        return MBC5(num_rom_banks, num_ram_banks)
    else:
        raise NotImplemented("Cartridge/MBC type not implemented: {}".format(cart_type))


class ROMOnly(object):
    """
    No MBC, just 32KB of ROM
    """
    def __init__(self):
        self.rom = [[0] * 2**14] * 2  # 2**14 = 16KB -> 2 banks

    def __len__(self):
        return 2**15

    def __getitem__(self, address: int):
        if 0 <= address < 0x8000:
            # address // 2**14 gives either 0 or 1 -> decides the ROM bank
            # address % 0x4000 gives a value in (0, 0x3fff) -> decides the ROM bank's cell address
            return self.rom[address // 2**14][address % 0x4000]
        else:
            message = 'ROM only cartridge was read at {}.\n\
                This value should be in (0, 32 * 2**10) (== 32KB).\n\
                If it is in (0xa000, 0xc000( then RAM was accessed while it does not exist'
            raise IndexError(message.format(address))

    def __setitem__(self, address: int, value: int):
        if 0 <= address < 0x8000:
            # cf __getitem__
            self.rom[address // 2**14][address % 0x4000] = value
        else:
            message = 'ROM only cartridge was written to at {}.\n\
                This value should be in (0, 32 * 2**10) (== 32KB).\n\
                If it is in (0xa000, 0xc000( then RAM was accessed while it does not exist'
            raise IndexError(message.format(address))


class MBC1(object):
    """
    MBC1: max 2MB ROM, 32KB RAM
    2MB ROM / 16KB bank size = 128 ROM banks
    32KB RAM / 8KB bank size = 4 RAM banks
    RAM must be enabled before use
    Must switch between 2 different modes to access RAM and switch between certain ROM banks
    """
    def __init__(self, num_rom_banks: int, num_ram_banks: int):
        self.rom = [[0] * 2**14] * num_rom_banks  # 2**14 = 16 * 2**10 = 16KB
        self.ram = [[0] * 2**13] * num_ram_banks  # etc
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

    def __len__(self):
        return len(self.rom) + len(self.ram)

    def __getitem__(self, address: int):
        if 0 <= address < 0x4000:
            return self.rom[0][address]
        elif 0x4000 <= address < 0x8000:
            return self.rom[self.romi][address % 0x3fff]  # each ROM bank is addressed from 0x0000 to 0x3fff
        elif 0xa000 <= address < 0xc0000:
            if self.ram_enabled:
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
    MBC2: max 256KB ROM, 2KB RAM
    256KB ROM / 16 KB bank size = 16 ROM banks
    2KB RAM / 4 bits bank size = 512 RAM banks
    This MBC only has 4 physical data lines linking it with the cpu via the cartridge,
    thus the 4 bit RAM bank size and the 2**4 ROM banks
    (This is basically a ROM-heavy, RAM-light cartridge)
    """

    def __init__(self, num_rom_banks: int):
        self.rom = [[0] * 2**14] * num_rom_banks  # see MBC1
        self.ram = [0] * 512
        self.ram_enabled = False
        # "switched-in" bank
        self.romi = 1

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
            if self.ram_enabled:
                return 0xf0 | self.ram[address % 0x200]  # there are 0x200 = 512 cells
        else:
            raise IndexError("MBC received invalid address : {}".format(str(address)))

    def __setitem__(self, address: int, value: int):
        """See http://bgb.bircd.org/pandocs.htm#mbc2max2mbyteromandor32kbyteram for a detailed list of the
        different "control zones" (address intervals) the MBC2 uses"""
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
            if self.ram_enabled:
                self.ram[address % 0x200] = 0xf & value  # 0x200 = 512 cells


class MBC3(object):
    """
    MBC3: max 2MB ROM and/or 32KB RAM and Timer
    The timer is 
    """
    def __init__(self, num_rom_banks, num_ram_banks, RTC=False):
        pass


class MBC5(object):
    """MBC5: max """
