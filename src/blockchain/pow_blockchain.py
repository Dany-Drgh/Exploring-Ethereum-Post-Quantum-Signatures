# pow_blockchain.py
import time
import hashlib

from zmq import has
from transactions.transaction import Transaction
from signature_schemes.mldsa_scheme import MLDSASignatureScheme

class PoWBlock:
    def __init__(self, index, previous_hash, transactions, difficulty, timestamp=None, hash_function=hashlib.sha512):
        
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty = difficulty
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = None
        self.hash_function = hash_function

    def calculate_hash(self):
        tx_str = ''.join([tx.hash() for tx in self.transactions])
        block_str = f'{self.index}{self.previous_hash}{self.timestamp}{tx_str}{self.nonce}'
        return self.hash_function(block_str.encode()).hexdigest()

    def mine(self):
        target = '0' * self.difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1

    def summary(self):
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "num_transactions": len(self.transactions),
            "nonce": self.nonce,
            "difficulty": self.difficulty
        }

class PoWBlockchain:
    def __init__(self, difficulty=4, block_hash_function=hashlib.sha512, tx_scheme = MLDSASignatureScheme()):
        self.chain = []
        self.difficulty = difficulty
        self.tx_scheme = tx_scheme
        self.tx_priv_key, self.tx_pub_key = self.tx_scheme.generate_keys()
        self.block_hash_function = block_hash_function
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = PoWBlock(
            index=0,
            previous_hash='0'*64,
            transactions=[],
            difficulty=self.difficulty,
            hash_function=self.block_hash_function
        )
        genesis.mine()
        self.chain.append(genesis)

    def add_block(self, transactions):
        prev_block = self.chain[-1]
        block = PoWBlock(
            index=len(self.chain),
            previous_hash=prev_block.hash,
            transactions=transactions,
            difficulty=self.difficulty,
            hash_function=self.block_hash_function
        )
        block.mine()
        self.chain.append(block)

    def summary(self):
        return [block.summary() for block in self.chain]


# ------------------------------------------
# Example usage
# ------------------------------------------

if __name__ == "__main__":    
    from signature_schemes.mldsa_scheme import MLDSASignatureScheme
    from blockchain.pow_blockchain import PoWBlockchain
    from transactions.transaction import Transaction

    # Instantiate PoW blockchain
    chain = PoWBlockchain(difficulty=3)

    # Create a signed transaction
    scheme = MLDSASignatureScheme()
    sk, pk = scheme.generate_keys()
    msg = "Alice->Bob:10"
    signature = scheme.sign(sk, msg)

    tx = Transaction("Alice", "Bob", 10, signature)

    # Add several mined blocks
    for i in range(5):
        chain.add_block([tx])

    # Display block summaries
    for summary in chain.summary():
        print(summary)