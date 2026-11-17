---
id: computing-software.blockchain-and-web3.solidity.storage-and-calldata-gas-patterns
name: storage-and-calldata-gas-patterns
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [gas-optimization-patterns, cache-storage-reads, unchecked-loop]
level: practitioner
status: docs-checked
description: "Apply proven gas patterns: cache storage reads, pack, calldata params, unchecked counters; measure each change."
sources:
  - https://github.com/foundry-rs/book/blob/master/src/pages/guides/gas-optimization.mdx
  - https://github.com/foundry-rs/book/blob/master/src/pages/forge/gas-tracking.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gas patterns
- Storage is the most expensive operation: minimise writes. Pack struct fields into shared slots (for example `uint128`, `uint64`, `uint64`) instead of a full `uint256` each.
- Read a storage variable once into a local, work on the local, and write back once after the loop.
- Use `calldata` instead of `memory` for read-only array parameters of external functions; memory copies the whole array.
- Use `unchecked { ++i; }` for counters and sums where overflow is impossible (document why).
- Prefer custom errors with `revert` over `require` strings.
- Order conditions so the cheap check runs first and short-circuits the expensive one.
- Do not trade readability for sub-percent wins in non-hot paths. Measure each change with `forge snapshot --diff` and `forge test --gas-report`, and guard with `forge snapshot --check` in CI.

## Verify
- [ ] `forge snapshot --diff` shows the gain and no regression elsewhere.

## Checked
Method: docs-checked 2026-11-09 against the Foundry book sources (raw MDX in the foundry-rs/book repository) for the gas optimization guide (storage, caching, unchecked, calldata, short-circuit and custom error sections) and the gas tracking page. The original book.getfoundry.sh URL is not fetchable. Dropped the immutable/constant advice and the "external" advice as not stated on those pages.
