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