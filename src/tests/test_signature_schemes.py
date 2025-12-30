import unittest
from signature_schemes.ecdsa_scheme import ECDSASignatureScheme
from signature_schemes.mldsa_scheme import MLDSASignatureScheme
from ecdsa import BadSignatureError

class TestSignatureSchemes(unittest.TestCase):
    def setUp(self):
        self.message = "Test Message"
        self.tampered_message = "Tampered Message"

        # ECDSA Setup
        self.ecdsa = ECDSASignatureScheme()
        self.ecdsa_sk, self.ecdsa_pk = self.ecdsa.generate_keys()
        self.ecdsa_signature = self.ecdsa.sign(self.ecdsa_sk, self.message)

        # ML-DSA Setup
        self.mldsa = MLDSASignatureScheme()
        self.mldsa_sk, self.mldsa_pk = self.mldsa.generate_keys()
        self.mldsa_signature = self.mldsa.sign(self.mldsa_sk, self.message)

    # --- ECDSA Tests ---

    def test_ecdsa_key_generation(self):
        self.assertIsNotNone(self.ecdsa_sk)
        self.assertIsNotNone(self.ecdsa_pk)

    def test_ecdsa_valid_signature(self):
        self.assertTrue(self.ecdsa.verify(self.ecdsa_pk, self.message, self.ecdsa_signature))

    def test_ecdsa_invalid_signature(self):
        self.assertFalse(self.ecdsa.verify(self.ecdsa_pk, self.tampered_message, self.ecdsa_signature))

    # --- ML-DSA Tests ---

    def test_mldsa_key_generation(self):
        self.assertIsNotNone(self.mldsa_sk)
        self.assertIsNotNone(self.mldsa_pk)

    def test_mldsa_valid_signature(self):
        self.assertTrue(self.mldsa.verify(self.mldsa_pk, self.message, self.mldsa_signature))

    def test_mldsa_invalid_signature(self):
        self.assertFalse(self.mldsa.verify(self.mldsa_pk, self.tampered_message, self.mldsa_signature))

if __name__ == "__main__":
    unittest.main()
