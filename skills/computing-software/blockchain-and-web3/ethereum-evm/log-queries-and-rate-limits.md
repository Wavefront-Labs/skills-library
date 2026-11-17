---
id: computing-software.blockchain-and-web3.ethereum-evm.log-queries-and-rate-limits
name: log-queries-and-rate-limits
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [eth-getlogs-pagination, rpc-rate-limits, rpc-batching]
level: practitioner
status: draft
description: "Page through eth_getLogs under provider range limits, batch RPC requests and handle rate limiting."
sources:
  - https://ethereum.org/en/developers/docs/apis/json-rpc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reliable log queries
- Providers cap block span and result size. Loop in windows (for example a few thousand blocks) and halve the window on a limit error.
- Filter as narrowly as you can: address + topic0 + indexed topics.
- Batch: send a JSON array of requests in one HTTP call (supported by most providers) to save round trips.
- Retry on HTTP 429 and limit errors with exponential backoff and jitter.
- Handle reorgs: treat only `finalized` or N-confirmed blocks as final; honour `removed: true` in subscriptions.

## Verify
- [ ] Re-running a window gives identical logs; the total equals the sum of windows.
