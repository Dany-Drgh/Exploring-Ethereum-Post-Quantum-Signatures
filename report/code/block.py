class Block:
    def __init__(self, index, previous_hash, transactions, validator, signature, signature_scheme, timestamp=None, hash_function=hashlib.sha256):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.signature = signature
        self.signature_scheme = signature_scheme
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_str = ''.join([tx.hash() for tx in self.transactions])
        block_str = f'''{self.index}{self.previous_hash}
        {self.timestamp}{tx_str}{self.validator}
        {self.signature_scheme}'''
        return self.hash_function(block_str.encode()).hexdigest()
    
