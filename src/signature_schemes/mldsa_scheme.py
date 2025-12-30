# mldsa_scheme.py
from signature_schemes.signature_scheme import SignatureScheme
import hashlib
import pqcrypto.sign.ml_dsa_65 as mldsa

class MLDSASignatureScheme(SignatureScheme):
    def generate_keys(self):
        # Note: public key comes first
        pk, sk = mldsa.generate_keypair()
        return sk, pk # Switch places for continuity with other shcemes and ensure only the byte array is returned

    def sign(self, private_key, message):
        if isinstance(message, str):
            message_encoded = message.encode()
        return mldsa.sign(private_key, message_encoded)

    def verify(self, public_key, message, signature):
        if isinstance(message, str):
            message_encoded = message.encode()
        try:
            return mldsa.verify(public_key, message_encoded, signature)
        except Exception:
            return False

# ------------------------------------------
# Example usage
# ------------------------------------------

if __name__ == "__main__":
    # Example usage
    scheme = MLDSASignatureScheme()
    secret_key, public_key = scheme.generate_keys()


    message = "Hello, this is a test message."
    signature = scheme.sign(secret_key, message)
    print("Message:", message)
    # print("Signature:", signature)
    
    print("Signature valid:", scheme.verify(public_key, message, signature))
    
    # Tampered message
    tampered_message = "Hello, this is a tampered message."
    print("Signature valid for tampered message:", scheme.verify(public_key, tampered_message, signature))