from pyboy.cpu import CPU
from pyboy.gpu import GPU
from pyboy.memory import Memory


class GameBoy(object):
    """" GameBoy """
    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.gpu = GPU()

    def load_rom(self, rom):
        pass

    def run(self, rom):
        self.load_rom(rom)
        self.main_loop()

    def main_loop(self):
        pass
