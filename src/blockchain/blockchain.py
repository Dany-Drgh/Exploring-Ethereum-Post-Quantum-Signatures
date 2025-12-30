# blockchain.py
import random
from blockchain.block import Block

class Validator:
    def __init__(self, address, ecdsa_scheme, mldsa_scheme):
        self.address = address
        self.ecdsa_scheme = ecdsa_scheme
        self.mldsa_scheme = mldsa_scheme
        self.ecdsa_sk, self.ecdsa_pk = ecdsa_scheme.generate_keys()
        self.mldsa_sk, self.mldsa_pk = mldsa_scheme.generate_keys()

    def sign(self, message, scheme_name):
        if scheme_name == "ecdsa":
            return self.ecdsa_scheme.sign(self.ecdsa_sk, message)
        elif scheme_name == "mldsa":
            return self.mldsa_scheme.sign(self.mldsa_sk, message)
        else:
            raise ValueError(f"Unknown scheme: {scheme_name}")

    def get_scheme(self, scheme_name):
        if scheme_name == "ecdsa":
            return self.ecdsa_scheme
        elif scheme_name == "mldsa":
            return self.mldsa_scheme
        else:
            raise ValueError(f"Unknown scheme: {scheme_name}")

class Blockchain:
    def __init__(self, validators, ecdsa_ratio=1.0):
        self.chain = []
        self.validators = validators  # List of Validator objects
        self.ecdsa_ratio = ecdsa_ratio
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(
            index=0,
            previous_hash='0'*64,
            transactions=[],
            validator='genesis',
            signature=b'genesis_signature',
            signature_scheme='none'
        )
        self.chain.append(genesis)

    def choose_signature_scheme(self):
        return "ecdsa" if random.random() < self.ecdsa_ratio else "mldsa"

    def select_validator(self):
        return random.choice(self.validators)

    def add_block(self, transactions):
        prev_block = self.chain[-1]
        validator = self.select_validator()
        scheme = self.choose_signature_scheme()

        # Block data to sign = tx hashes + prev block hash
        tx_hash_data = ''.join([tx.hash() for tx in transactions]) + str(prev_block.hash)
        signature = validator.sign(tx_hash_data, scheme)

        new_block = Block(
            index=len(self.chain),
            previous_hash=prev_block.hash,
            transactions=transactions,
            validator=validator.address,
            signature=signature,
            signature_scheme=scheme
        )
        self.chain.append(new_block)

    def summary(self):
        return [block.summary() for block in self.chain]

# ------------------------------------------
# Example usage
# ------------------------------------------
if __name__ == "__main__":
    from transactions.transaction import Transaction
    from signature_schemes.ecdsa_scheme import ECDSASignatureScheme
    from signature_schemes.mldsa_scheme import MLDSASignatureScheme

    ecdsa = ECDSASignatureScheme()
    mldsa = MLDSASignatureScheme()

    # Create 5 validators that support both schemes
    validators = [Validator(f"V{i+1}", ecdsa, mldsa) for i in range(5)]

    # Blockchain with 60% ECDSA, 40% ML-DSA
    blockchain = Blockchain(validators, ecdsa_ratio=0.6)

    # Add blocks
    for i in range(10):
        txs = [Transaction("Alice", "Bob", i + 1)]
        blockchain.add_block(txs)

    # Print summaries
    for summary in blockchain.summary():
        print(summary)
