import unittest
from ecdsa import BadSignatureError
from signature_schemes.ecdsa_pow_scheme import ECDSAPoWSignatureScheme

class TestECDSAPoWSignatureScheme(unittest.TestCase):
    def setUp(self):
        self.scheme = ECDSAPoWSignatureScheme()
        self.sk, self.vk = self.scheme.generate_keys()
        self.message = "Hello, blockchain!"
        self.signature = self.scheme.sign(self.sk, self.message)

    def test_key_generation(self):
        self.assertIsNotNone(self.sk)
        self.assertIsNotNone(self.vk)
        self.assertTrue(hasattr(self.sk, 'sign'))
        self.assertTrue(hasattr(self.vk, 'verify'))

    def test_sign_and_verify_valid_signature(self):
        is_valid = self.scheme.verify(self.vk, self.message, self.signature)
        self.assertTrue(is_valid)

    def test_sign_and_verify_invalid_signature(self):
        altered_signature = self.signature[:-1] + b'\x00'
        with self.assertRaises(BadSignatureError):
            self.scheme.verify(self.vk, self.message, altered_signature)

    def test_verify_with_wrong_message(self):
        wrong_message = "Wrong message"
        with self.assertRaises(BadSignatureError):
            self.scheme.verify(self.vk, wrong_message, self.signature)

if __name__ == "__main__":
    unittest.main()
