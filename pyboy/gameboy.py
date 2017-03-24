from pyboy.cpu import CPU
from pyboy.gpu import GPU
from pyboy.memory import Memory


class GameBoy(object):
    """" GameBoy """
    def __init__(self):
        self.cpu = CPU()
        self.gpu = GPU()
        self.memory = Memory()

    def load_rom(self, rom):
        pass

    def run(self, rom):
        self.load_rom(rom)
        self.main_loop()

    def main_loop(self):
        pass
