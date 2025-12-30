import unittest
from blockchain.pow_blockchain import PoWBlockchain
from signature_schemes.ecdsa_pow_scheme import ECDSAPoWSignatureScheme
from transactions.transaction import Transaction

class TestPoWBlockchain(unittest.TestCase):
    def setUp(self):
        self.difficulty = 3
        self.blockchain = PoWBlockchain(difficulty=self.difficulty)
        self.scheme = ECDSAPoWSignatureScheme()
        self.sk, self.pk = self.scheme.generate_keys()
        self.msg = "Alice->Bob:10"
        self.signature = self.scheme.sign(self.sk, self.msg)
        self.tx = Transaction("Alice", "Bob", 10, self.signature)

    def test_genesis_block_exists(self):
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)

    def test_add_block(self):
        self.blockchain.add_block([self.tx])
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(self.blockchain.chain[-1].transactions[0].amount, 10)

    def test_multiple_blocks(self):
        for _ in range(5):
            self.blockchain.add_block([self.tx])
        self.assertEqual(len(self.blockchain.chain), 6)

    def test_difficulty_requirement(self):
        self.blockchain.add_block([self.tx])
        last_block = self.blockchain.chain[-1]
        self.assertTrue(last_block.hash.startswith('0' * self.difficulty))

    def test_block_summary_structure(self):
        self.blockchain.add_block([self.tx])
        summary = self.blockchain.chain[-1].summary()
        expected_keys = {"index", "hash", "previous_hash", "timestamp", "num_transactions", "nonce", "difficulty"}
        self.assertTrue(expected_keys.issubset(summary.keys()))

if __name__ == '__main__':
    unittest.main()
