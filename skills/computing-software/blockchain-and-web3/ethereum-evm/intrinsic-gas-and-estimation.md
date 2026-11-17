---
id: computing-software.blockchain-and-web3.ethereum-evm.intrinsic-gas-and-estimation
name: intrinsic-gas-and-estimation
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [intrinsic-gas, eth-estimategas, gas-limit, bc-eth-gas]
level: practitioner
status: draft
description: "Estimate gas with eth_estimateGas, know the 21000 base cost and calldata costs, and avoid out-of-gas failures from tight limits."
sources:
  - https://ethereum.org/en/developers/docs/gas/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intrinsic gas and estimation
- Every transaction pays 21000 base gas; contract creation adds 32000; calldata costs 4 gas per zero byte and 16 per non-zero byte (verify against the Yellow Paper for your fork).
- `eth_estimateGas` simulates and returns gas needed; add a buffer (about 10-20%) because state may change before inclusion.
- Gas limit is a ceiling, only gas used is charged. The block gas limit caps the sum of transactions.
- Gotcha: the 63/64 rule: a call forwards at most 63/64 of remaining gas, so sub-calls can fail when the outer limit is tight.
- Gotcha: an estimate can succeed on a node but fail on-chain if behaviour depends on `block.timestamp` or earlier transactions.

## Verify
- [ ] `cast estimate` result is below the limit you set, and a dry run on a fork matches.
