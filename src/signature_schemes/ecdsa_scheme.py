# ecdsa_scheme.py
from re import I
from ecdsa import SigningKey, SECP256k1, BadSignatureError
from signature_schemes.signature_scheme import SignatureScheme


class ECDSASignatureScheme(SignatureScheme):
    def generate_keys(self):
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.verifying_key
        return sk, vk

    def sign(self, private_key, message):
        return private_key.sign(message.encode())

    def verify(self, public_key, message, signature):
        if isinstance(message, str):
            message = message.encode()
        try:
            return public_key.verify(signature, message)
        except BadSignatureError:
            return False
    
# ------------------------------------------
# Example usage
# ------------------------------------------

if __name__ == "__main__":
    # Example usage
    scheme = ECDSASignatureScheme()
    secret_key, public_key = scheme.generate_keys()

    message = "Hello, this is a test message."
    signature = scheme.sign(secret_key, message)
    print("Message:", message)
    print("Signature:", signature.hex())

    print("Signature valid:", scheme.verify(public_key, message, signature))

    # Tampered message
    tampered_message = "Hello, this is a tampered message."
    print("Signature valid for tampered message:", scheme.verify(public_key, tampered_message, signature))



