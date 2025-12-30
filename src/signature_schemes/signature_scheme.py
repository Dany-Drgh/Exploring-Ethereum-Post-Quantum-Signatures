# signature_scheme.py
from abc import ABC, abstractmethod

class SignatureScheme(ABC):
    @abstractmethod
    def generate_keys(self):
        pass

    @abstractmethod
    def sign(self, private_key, message):
        pass

    @abstractmethod
    def verify(self, public_key, message, signature):
        pass
