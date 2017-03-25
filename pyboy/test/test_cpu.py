import unittest
from unittest import TestCase
from pyboy.cpu import CPU
from pyboy.memory import Memory


class TestCPU(TestCase):
    def setUp(self):
        super().setUp()
        self.mem = Memory()
        self.cpu = CPU(self.mem)

    def write_to_mem(self, data):
        for byte in data:
            self.mem[self.cpu.registers["PC"]] = byte & 0xFF
            self.cpu.registers["PC"] += 1
        self.cpu.registers["PC"] = 0x100

    def test_exec_load(self):
        # LD A,0xFF
        # LD (0xFFFE),A
        data = [0x3E, 0xFF, 0xEA, 0xFE, 0xFF]
        self.write_to_mem(data)
        self.cpu.exec_next()
        self.assertEqual(self.cpu.registers['A'], 0xFF)
        self.assertEqual(self.cpu.registers['PC'], 0x102)
        self.cpu.exec_next()
        self.assertEqual(self.mem[0xFFFE], 0xFF)
        self.assertEqual(self.cpu.registers['PC'], 0x105)

    def test_get_next_byte(self):
        # LD A,0xFF
        # LD (0xFFFE),A
        data = [0x3E, 0xFF, 0xFA, 0xFE, 0xFF]
        self.write_to_mem(data)
        self.assertEqual(self.cpu.get_next_byte(), 0x3E)
        self.assertEqual(self.cpu.get_next_byte(), 0xFF)
        self.assertEqual(self.cpu.get_next_byte(), 0xFA)
        self.assertEqual(self.cpu.get_next_byte(), 0xFE)
        self.assertEqual(self.cpu.get_next_byte(), 0xFF)

    def test_signed(self):
        self.assertEquals(CPU.signed(0xFF), -1)

if __name__ == "__main__":
    unittest.main()
