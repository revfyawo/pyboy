from pyboy.mbc import MBC


class Cartridge(object):
    """ Game Cartridge The first 32kB of address space is the game cartridge.
    Addresses 0xa000 to 0xbffff (8kB) are cartridge RAM (if present)
    The first 16kB consist of ROM (aka the first ROM bank), and the following 16kB depend on the cartridge type.
    They can be just another 16kB of ROM space (as in Tetris), or a dynamic load of further ROM banks (or even
    RAM) located inside the cartridge. 
    """
    def __init__(self):
        """
        This is minimalistic for testing/debugging purposes. The Cartridge object
        should not be used before having loaded an actual game "rom" from file
        """
        """ todo: use a dict for ALL internal memory (ROM & RAM), and use __get&set_item__() to call the mbc (maybe 
            have the mbc return the key to facilitate vertical integration (and&or modularity) (this is also more 
            consistent with the "chain of command" in reality """
        self.rom0 = [0 for _ in range(0x3FFF + 1)]
        self.romx = [0 for _ in range(0x3FFF + 1)]
        self.mbc = None

    def load_game_rom(self, rom_file_path):
        """ Load a game binary from file, and store it in the appropriate layout. """
        self.mbc = MBC.infer_from_rom(rom_file_path)

        with open(rom_file_path, 'rb') as rom:
            count = 0
            while rom.peek(1)[:1] is not '':
                if count < 0x4000:
                    self.rom0[count] = rom.read(1)
                elif count < 0x8000:
                    if self.mbc is None:
                        self.romx[count] = rom.read(1)
                    else:
                        # todo: figure out how the extra rom banks are stored in a game rom,
                        # and pass them to the mbc (or handle their storage here)
                        pass
                count += 1
                # todo: interpret cartridge header (bytes 0x100 - 0x14f) (see The docs)
