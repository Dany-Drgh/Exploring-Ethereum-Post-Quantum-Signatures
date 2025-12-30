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

class PoWBlockchain:
    def __init__(self, difficulty=4, block_hash_function=hashlib.sha512, tx_scheme = MLDSASignatureScheme()):
        self.chain = []
        self.difficulty = difficulty
        self.tx_scheme = tx_scheme # Transaction scheme for signing transactions
        self.tx_priv_key, self.tx_pub_key = self.tx_scheme.generate_keys() # Transaction keys
        self.block_hash_function = block_hash_function
        self.create_genesis_block()
