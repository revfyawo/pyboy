class Memory(object):
    """" Memory """
    def __init__(self):
        self.iter_index = -1
        self.mem = [0 for _ in range(0xFFFF + 1)]

    def __len__(self):
        return len(self.mem)

    def __iter__(self):
        self.iter_index = -1
        return self

    def __next__(self):
        self.iter_index += 1
        if self.iter_index > 0xFFFF:
            raise StopIteration
        return self.mem[self.iter_index]

    def __getitem__(self, item):
        return self.mem[item]

    def __setitem__(self, key, value):
        self.mem[key] = value
        return value
