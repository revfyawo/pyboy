class Memory(object):
    """" Memory """
    def __init__(self, cart=None):
        self.iter_index = -1
        self.mem = [0 for _ in range(0xFFFF + 1)]
        self.cart = cart

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
        elif key < 0x8000 or (0xa000 <= key < 0xc000):
            if self.cart is None:
                # according to docs, return 0xff
                raise CartridgeMissing
            else:
                return self.cart[key]
        else:
            return self.mem[key]

    def __setitem__(self, key, value):
        if key < 0 or key > 0xFFFF:
            raise IndexError("Memory access out of bounds, address {} is invalid.".format(key))
        elif key < 0x8000 or (0xa000 <= key < 0xc000):
            if self.cart is None:
                # according to docs, return 0xff
                raise CartridgeMissing
            else:
                self.cart[key] = value
        else:
            self.mem[key] = value
        # return value


class CartridgeMissing(Exception):
    """
    As the name suggests, raised when trying to access the first
    32kB of address space when the cartridge is not present/loaded
    """
