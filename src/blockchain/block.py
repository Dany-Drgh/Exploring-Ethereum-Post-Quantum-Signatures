# block.py
import time
import hashlib

class Block:
    def __init__(self, index, previous_hash, transactions, validator, signature, signature_scheme, timestamp=None, hash_function=hashlib.sha512):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.signature = signature
        self.signature_scheme = signature_scheme
        self.timestamp = timestamp or time.time()
        self.hash_function = hash_function
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_str = ''.join([tx.hash() for tx in self.transactions])
        block_str = f'{self.index}{self.previous_hash}{self.timestamp}{tx_str}{self.validator}{self.signature_scheme}'
        return self.hash_function(block_str.encode()).hexdigest()

    def summary(self):
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "validator": self.validator,
            "signature_scheme": self.signature_scheme,
            "timestamp": self.timestamp,
            "num_transactions": len(self.transactions)
        }

# ------------------------------------------
# Example usage
# ------------------------------------------
if __name__ == "__main__":
    from transactions.transaction import Transaction

    # Dummy transaction list
    txs = [
        Transaction("Alice", "Bob", 10),
        Transaction("Charlie", "Dave", 5)
    ]

    # Fake keys and signature for testing
    fake_validator = "0xValidator123"
    fake_signature = b"fake_signature_bytes"
    sig_scheme = "ecdsa"

    block = Block(
        index=1,
        previous_hash='0'*64,
        transactions=txs,
        validator=fake_validator,
        signature=fake_signature,
        signature_scheme=sig_scheme
    )

    print("Block Summary:")
    print(block.summary())
