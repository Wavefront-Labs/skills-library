---
id: computing-software.blockchain-and-web3.smart-contract-security.chainlink-feed-consumption-checks
name: chainlink-feed-consumption-checks
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [chainlink-staleness, latestrounddata, sequencer-uptime-feed]
level: practitioner
status: draft
description: "Read Chainlink price feeds with staleness, positive-answer, decimals and L2 sequencer checks."
sources:
  - https://docs.chain.link/data-feeds/using-data-feeds
  - https://docs.chain.link/data-feeds/l2-sequencer-feeds
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe feed consumption
```solidity
(, int256 answer,, uint256 updatedAt,) = feed.latestRoundData();
require(answer > 0, "bad price");
require(block.timestamp - updatedAt <= MAX_AGE, "stale");
uint8 d = feed.decimals();   // normalise, do not hard-code 8
```
- Set `MAX_AGE` slightly above the feed's heartbeat (see the feed's page).
- Different feeds have different decimals (ETH/USD 8, some ETH-denominated feeds 18).
- On L2s, also check the sequencer uptime feed and a grace period after it comes back.
- Plan for feed deprecation: make the feed address updatable under governance with a delay.

## Verify
- [ ] Tests with mock feeds returning stale, zero and negative values revert.
