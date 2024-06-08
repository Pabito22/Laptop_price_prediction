import unittest
from laptop_features_extractor import take_size_type_fromMemory

class MemoryTypeSizeTest(unittest.TestCase):
    """Tests for 'laptop_features_extractor.py'."""
    def test_one_word(self):
        """Are values:
        ['128GB SSD']
         preprocessed right by take_size_type_fromMemory
        function?
        """
        fromated_val = take_size_type_fromMemory('128GB SSD')
        expected = [128.0, 'SSD']
        self.assertEqual(fromated_val, expected)

    def test_2_word(self):
        """Are values:
        ['128GB Flash Storag +  1TB HDD']
         preprocessed right by take_size_type_fromMemory
        function?
        """
        fromated_val = take_size_type_fromMemory('128GB Flash Storag +  1TB HDD')
        expected = [128.0, 'Flash Storag', 1024.0, 'HDD']
        self.assertEqual(fromated_val, expected)

if __name__ == '__main__':
    unittest.main()

