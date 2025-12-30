class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, hash_function=hashlib.sha256):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.hash_function = hash_function

    def serialize(self):
        return f'{self.sender}->{self.recipient}:{self.amount}'

    def hash(self):
        return self.hash_function(self.serialize().encode()).hexdigest()