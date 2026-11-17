---
id: computing-software.blockchain-and-web3.ethereum-evm.eip1559-fee-fields
name: eip1559-fee-fields
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [eip1559-fees, max-priority-fee, base-fee, bc-eth-transactions]
level: practitioner
status: docs-checked
description: "Set maxFeePerGas and maxPriorityFeePerGas correctly and predict what a type-2 transaction actually pays."
sources:
  - https://eips.ethereum.org/EIPS/eip-1559
  - https://ethereum.org/en/developers/docs/gas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EIP-1559 fees
- Type-2 (`0x02`) transactions carry `max_priority_fee_per_gas` and `max_fee_per_gas` (JSON-RPC names `maxPriorityFeePerGas` and `maxFeePerGas`).
- The base fee per gas is burned. It rises when blocks are above the gas target and falls when below; the target is half the block gas limit.
- ethereum.org: the base fee changes by at most 12.5% per block.
- The gas fee you pay is split into the base fee and a priority fee (tip).
- The transaction states the maximum fee per gas it is willing to pay; set headroom above the current base fee as the limit, not the price actually paid.

## Verify
- [ ] The receipt shows what the transaction paid; compare with the block's base fee plus your tip.

## Checked

2026-11-02. Confirmed against EIP-1559 (type 0x02 fields, burned base fee, gas target = limit / elasticity 2, base-fee direction) and ethereum.org gas page (12.5% per block, base fee plus priority fee). Removed as not stated on those pages: the min() effective-price formula, the 2 x baseFee + tip rule of thumb, refund of unused headroom, eth_feeHistory, eth_maxPriorityFeePerGas, cast base-fee, effectiveGasPrice, legacy gasPrice behaviour.
Method: documentation only; no commands were run.
