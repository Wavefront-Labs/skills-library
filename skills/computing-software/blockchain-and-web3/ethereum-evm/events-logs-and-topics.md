---
id: computing-software.blockchain-and-web3.ethereum-evm.events-logs-and-topics
name: events-logs-and-topics
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [event-logs, indexed-topics, event-signature]
level: practitioner
status: docs-checked
description: "Decode event logs: topic0 as event signature hash, indexed arguments as topics, others in data."
sources:
  - https://docs.soliditylang.org/en/latest/abi-spec.html#events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Events and logs
- Topic 0 is the Keccak hash of the event signature (non-anonymous events).
- Up to 3 indexed arguments (4 for anonymous events) become additional topics; non-indexed arguments are ABI-encoded in the log data.
- Indexed values of at most 32 bytes are stored directly (padded or sign-extended to 32 bytes); for "complex" types such as strings and bytes the topic holds the Keccak hash of the value, so the original cannot be recovered from the topic.

## Verify
- [ ] Decoded values equal those from the contract's view function at that block.
## Checked
2026-11-02. Confirmed against the Solidity "Contract ABI Specification" (Events section). Removed: the ERC-20 Transfer topic prefix, `eth_getLogs` and provider limits, `cast logs`, and the claim that contracts cannot read logs (none stated on the page).
Method: documentation only; no commands were run.
