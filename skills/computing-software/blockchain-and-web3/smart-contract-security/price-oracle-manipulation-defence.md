---
id: computing-software.blockchain-and-web3.smart-contract-security.price-oracle-manipulation-defence
name: price-oracle-manipulation-defence
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [oracle-manipulation, twap-oracle, spot-price-risk, bc-sec-oracle]
level: advanced
status: draft
description: "Do not use a DEX pool's spot price for valuation; use manipulation-resistant sources and bounds."
sources:
  - https://docs.chain.link/data-feeds
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oracle manipulation (defence)
- A pool's instantaneous reserve ratio can be moved within one transaction using a flash loan; any contract valuing collateral from it can be misled.
- Prefer: decentralised oracle feeds (Chainlink data feeds), or a time-weighted average price (TWAP) over a long enough window with deep liquidity.
- Add circuit breakers: max deviation between sources, max change per block, pause on anomaly.
- Value only assets with sufficient liquidity; consider the cost to manipulate vs the value at risk.
- Test with a fork-based flash-loan simulation of price movement and assert the protocol's behaviour.

## Verify
- [ ] A fork test that moves the pool price in one transaction does not change protocol valuations.
