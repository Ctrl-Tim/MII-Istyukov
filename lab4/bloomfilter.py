import math
from bitarray import bitarray

class BloomFilter(object):
    def __init__(self, size, number_expected_elements=100):
        self.size = size
        self.number_expected_elements = number_expected_elements
        self.filter = bitarray(self.size)
        self.filter.setall(0)
        self.number_hash_functions = round((self.size / self.number_expected_elements) * math.log(2))

    def _hash_djb2(self, s):
        hash = 5381
        for x in s:
            hash = ((hash << 5) + hash) + ord(x)
        return hash % self.size

    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)

    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.filter[self._hash(item, i)] = 1

    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.filter[self._hash(item, i)] == 0:
                return True
        return False
