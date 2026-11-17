---
id: computing-software.blockchain-and-web3.smart-contract-security.griefing-and-forced-ether
name: griefing-and-forced-ether
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [forced-ether, balance-invariant, griefing]
level: practitioner
status: draft
description: "Never use address(this).balance for strict invariants; handle forced ETH and donation attacks."
sources:
  - https://consensys.github.io/smart-contract-best-practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forced ETH and donations
- ETH can be forced into a contract (`selfdestruct` beneficiary, coinbase rewards), bypassing `receive`. Likewise tokens can be sent directly.
- Equality checks like `require(address(this).balance == total)` can be broken permanently by a 1 wei donation.
- Track internal accounting variables; treat extra balance as surplus.
- For vaults, donation to inflate share price is the first-depositor attack; see ERC-4626 mitigations.

## Verify
- [ ] Test donates ETH/tokens directly and asserts core invariants still hold.
