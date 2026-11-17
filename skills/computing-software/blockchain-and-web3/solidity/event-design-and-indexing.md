---
id: computing-software.blockchain-and-web3.solidity.event-design-and-indexing
name: event-design-and-indexing
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [event-design, indexed-parameters, anonymous-events, bc-sol-events]
level: practitioner
status: docs-checked
description: "Emit events that indexers and front-ends can rely on: what to index, naming, and what to log."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event design
- Emit an event for every state change a UI or indexer cares about: ownership, parameters, deposits, withdrawals.
- `indexed` parameters go into log topics, which can be filtered; at most three per event (four if the event is `anonymous`). Index fields you filter by, such as user or id.
- A topic holds one 32-byte word, so an indexed reference type (string, bytes, array) is stored as its Keccak-256 hash and the original value cannot be read back from the log. Leave such values unindexed if consumers need them.
- Non-indexed parameters are ABI-encoded into the data part of the log.
- Include old and new values for config changes.
- The event signature hash is the first topic unless the event is `anonymous`; anonymous events cannot be filtered by name, only by contract address, and an anonymous event can fake another event's signature. `event.selector` gives the signature hash for non-anonymous events.
- Logs are not accessible from within contracts, not even the one that emitted them, so do not use them as an on-chain data source.
- Logs only store the data, not its types: consumers need the ABI to know which parameters are indexed and whether the event is anonymous.

## Verify
- [ ] A test asserts the expected event (name, topics and data) for every state-changing function.

## Checked

Confirmed against Solidity docs contracts/events.rst: indexed limit of three (four for anonymous), hashing of indexed reference types, topic and data layout, anonymous event behaviour, `event.selector`, and logs being inaccessible to contracts. Removed: the per-topic and per-byte gas figures (no page read states them), the "emit after state change" rationale, and the Foundry `vm.expectEmit` reference.

Method: docs-checked 2026-11-09 against Solidity docs contracts/events.rst (raw rst on GitHub).
