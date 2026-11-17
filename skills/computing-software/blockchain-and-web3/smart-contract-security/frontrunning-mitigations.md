---
id: computing-software.blockchain-and-web3.smart-contract-security.frontrunning-mitigations
name: frontrunning-mitigations
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [front-running-mitigation, commit-reveal, slippage-protection, bc-sec-mev]
level: practitioner
status: draft
description: "Reduce transaction-ordering dependence with slippage limits, deadlines and commit-reveal."
sources:
  - https://swcregistry.io/
  - https://ethereum.org/en/developers/docs/mev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Front-running mitigations
- Anything in the public mempool can be seen and reordered. Design assuming adversarial ordering.
- Swaps: require `minAmountOut` and `deadline` from the caller; never compute them on chain from the same pool.
- Auctions/claims: commit-reveal (commit hash, later reveal with salt).
- Approvals and first-depositor flows: avoid actions where a first mover profits from a later user's transaction.
- Users can submit through private relays to avoid public mempool exposure.

## Verify
- [ ] A test that sandwiches a swap hits the user's min-out check and reverts.
