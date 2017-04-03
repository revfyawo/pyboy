class Cartridge(object):
    """ Game Cartridge
    The first 32kB of address space is the game cartridge.
    The first 16kB consist of ROM (aka the first ROM bank), and the following
    16kB depend on the cartridge type. They can be just another 16kB of ROM space
    (as in Tetris), or a dynamic load of further ROM banks (or even RAM).
    """
    def __init__(self):
        """
        This is minimalistic for testing/debugging purposes. The Cartridge object
        should not be used before having loaded an actual game "rom" from file
        """
        self.rom0 = [0 for _ in range(0x7FFF + 1)]

    def load_game_rom(rom_file_path):
        with open(rom_file_path, 'rb') as rom:
            pass
            #todo: read byte by byte
            

class MBC(object):
    """ Memory Bank Controller - Handles the extra ROM and/or RAM present in the cartridge """
    pass

class Memory(object):
    """" Memory """
    def __init__(self):
        self.iter_index = -1
        self.mem = [0 for _ in range(0xFFFF + 1)]

    def __iter__(self):
        self.iter_index = -1
        return self

    def __next__(self):
        self.iter_index += 1
        if self.iter_index > 0xFFFF:
            raise StopIteration
        return self.mem[self.iter_index]

    def __getitem__(self, key):
        if key < 0 or key > 0xFFFF:
            raise IndexError("Memory access out of bounds, address {} is invalid.".format(key))
        elif key < 0x8000:
            if self.cart is None:
                raise CartridgeMissing
            else:
                return self.cart[key]
        else:
            return self.mem[key]

    def __setitem__(self, key, value):
        if key < 0 or key > 0xFFFF:
            raise IndexError("Memory access out of bounds, address {} is invalid.".format(key))
        elif key < 0x8000:
            if self.cart is None:
                raise CartridgeMissing
            else:
                self.cart[key] = value
        else:
            self.mem[key] = value
        return value

class CartridgeMissing(Exception):
    """
    As the name suggests, raised when trying to access the first
    32kB of address space when the cartridge is not present/loaded
    """
