import unittest
from transactions.transaction import Transaction
import hashlib

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.tx = Transaction("Alice", "Bob", 100)

    def test_serialize(self):
        self.assertEqual(self.tx.serialize(), "Alice->Bob:100")

    def test_hash(self):
        expected_hash = hashlib.sha256("Alice->Bob:100".encode()).hexdigest()
        self.assertEqual(self.tx.hash(), expected_hash)

    def test_optional_signature(self):
        signed_tx = Transaction("Alice", "Bob", 100, signature=b'signature')
        self.assertEqual(signed_tx.signature, b'signature')

if __name__ == "__main__":
    unittest.main()
