# Set up phase parameters
NUM_BLOCKS = 1000
ECDSA_RATIO_CASES = {
    "Phase 1 (100% ECDSA - 0% ML-DSA )": 1.0,
    "Phase 2 (75% ECDSA - 25% ML-DSA)": 0.75,
    "Phase 3 (25% ECDSA - 75% ML-DSA)": 0.25,
    "Phase 4 (0% ECDSA - 100% ML-DSA)": 0.0
}

for label, ratio in ECDSA_RATIO_CASES.items():
    chain = Blockchain(validators, ecdsa_ratio=ratio)
    times = []

    for i in tqdm(range(NUM_BLOCKS), desc=f"Running {label} block time measurements", bar_format='{desc}: {bar:30} {percentage:3.0f}%'):
        txs = [Transaction("A", "B", i)]
        start = time.perf_counter()
        chain.add_block(txs)
        times.append(time.perf_counter() - start)