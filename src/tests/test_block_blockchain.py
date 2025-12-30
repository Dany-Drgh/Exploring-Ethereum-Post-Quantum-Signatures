import unittest
from blockchain.block import Block
from blockchain.blockchain import Validator, Blockchain
from transactions.transaction import Transaction
from signature_schemes.ecdsa_scheme import ECDSASignatureScheme
from signature_schemes.mldsa_scheme import MLDSASignatureScheme

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.tx1 = Transaction("Alice", "Bob", 10)
        self.tx2 = Transaction("Charlie", "Dave", 5)
        self.block = Block(
            index=1,
            previous_hash="0"*64,
            transactions=[self.tx1, self.tx2],
            validator="Validator1",
            signature=b"fake_sig",
            signature_scheme="ecdsa"
        )

    def test_block_hash_consistency(self):
        hash_1 = self.block.calculate_hash()
        hash_2 = self.block.calculate_hash()
        self.assertEqual(hash_1, hash_2)

    def test_summary_fields(self):
        summary = self.block.summary()
        expected_keys = {"index", "hash", "previous_hash", "validator", "signature_scheme", "timestamp", "num_transactions"}
        self.assertTrue(expected_keys.issubset(summary.keys()))
        self.assertEqual(summary["num_transactions"], 2)


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.ecdsa = ECDSASignatureScheme()
        self.mldsa = MLDSASignatureScheme()
        self.validators = [Validator(f"V{i+1}", self.ecdsa, self.mldsa) for i in range(3)]
        self.blockchain = Blockchain(validators=self.validators, ecdsa_ratio=0.5)

    def test_genesis_block_exists(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_add_block_increases_chain_length(self):
        tx = Transaction("Alice", "Bob", 50)
        self.blockchain.add_block([tx])
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_add_block_signature_and_validator(self):
        tx = Transaction("Eve", "Frank", 25)
        self.blockchain.add_block([tx])
        block = self.blockchain.chain[-1]
        self.assertIn(block.signature_scheme, ["ecdsa", "mldsa"])
        self.assertTrue(block.validator.startswith("V"))

if __name__ == "__main__":
    unittest.main()
