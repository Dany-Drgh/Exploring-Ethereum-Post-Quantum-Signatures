
Ethereum Post-Quantum Signature Experiment
==========================================

This project implements and simulates the performance of post-quantum signature schemes on a Proof-of-Stake (PoS) Ethereum-like blockchain. It aims to compare classic ECDSA signing with ML-DSA (a lattice-based, NIST-approved post-quantum digital signature algorithm), in terms of:
- Signature performance (signing, verification)
- Gas cost (based on calldata size)
- Blockchain block creation time

A secondary baseline is also provided via a Proof-of-Work (PoW) blockchain simulation using an upscaled ECDSA scheme (NIST P-521) to model Grover-resistant security.

Experiment Setup
----------------

The experiments simulate five blockchain configurations:

1. Phase 1 (100% ECDSA) — Classic PoS with only ECDSA signatures
2. Phase 2 (75% ECDSA, 25% ML-DSA) — Transition phase with minority post-quantum adoption
3. Phase 3 (25% ECDSA, 75% ML-DSA) — Majority of blocks signed with ML-DSA
4. Phase 4 (100% ML-DSA) — Fully post-quantum blockchain
5. Case 5 (PoW + ECDSA P-521) — Grover-resistant proof-of-work chain without signatures

Each phase is benchmarked for:
- Block creation time
- Signature size
- Signature gas cost
- Signing and verification speed

Implementation Structure
--------------
```
src/
├──blockchain/
|   ├── __init__.py                # Package initialization
|   ├── block.py                   # Block structure (common to PoS and PoW)
|   ├── blockchain.py              # Blockchain logic (PoS validator-controlled)
|   └── pow_blockchain.py          # Simplified Bitcoin-like PoW chain
├── transactions/
|   ├── __init__.py                # Package initialization
|   └── transaction.py             # Transaction class (currently minimal)
├── signature_schemes/
|   ├── __init__.py                # Package initialization
|   ├── signature_scheme.py        # Abstract base class for signature schemes
|   ├── ecdsa_scheme.py            # ECDSA (SECP256k1) signing implementation
|   ├── mldsa_scheme.py            # ML-DSA (level 2 = ML-DSA-65) implementation
|   └── ecdsa_pow_scheme.py        # PoW-only ECDSA P-521 implementation (Grover-safe)
│
├── Ethereum_PQC.ipynb             # Jupyter notebook with experiments and plots
├── README.txt                     # This file
└── requirements.txt               # Dependencies for experiments
```
Requirements
------------

To install dependencies:
```bash
    pip install -r requirements.txt
```
If you're using Windows and encounter issues with `pqcrypto`, it's recommended to use WSL (Ubuntu) or a Linux VM.

The project uses:
- Python 3.10 or 3.11 (Not compatible with 3.12+ for `pqcrypto`)
- pqcrypto (for ML-DSA from PQClean)
- ecdsa, pandas, matplotlib, numpy, tqdm, IPython, jupyter

Running the Experiment
----------------------

Launch:

    jupyter notebook

and open Ethereum_PQC.ipynb. You can:
- Run all cells
- Inspect performance comparisons
- View tables and plots
- Export results

Outputs
-------

The notebook provides:
- Bar plots for:
  - Signing time
  - Verification time
  - Estimated gas cost
- Final summary table with:
  - Block time
  - Signing and verification time
  - Signature size (bytes)
  - Estimated calldata gas

All results are phase-separated and directly usable in thesis figures or tables.

Testing the Schemes
-------------------

Each signature scheme has a test block in its Python file (__main__) that:
- Generates a keypair
- Signs and verifies a message
- Validates that tampered messages fail verification

Run these as:

    python src/signature_schemes/ecdsa_scheme.py
    python src/signature_schemes/mldsa_scheme.py

Unit tests are also available in the `tests/` directory, which can be run using:

```bash
    python -m unittest discover -s tests
```
Contact
-------

For questions, feel free to reach out to the author or submit an issue in this repository.
