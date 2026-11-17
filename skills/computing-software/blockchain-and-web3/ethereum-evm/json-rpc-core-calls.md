---
id: computing-software.blockchain-and-web3.ethereum-evm.json-rpc-core-calls
name: json-rpc-core-calls
category: computing-software
field: blockchain-and-web3
product: ethereum-evm
tags: [json-rpc-methods, block-tags, eth-call, bc-eth-jsonrpc]
level: practitioner
status: draft
description: "Use eth_call, eth_getBalance, eth_blockNumber and block tags (latest, safe, finalized) correctly with curl or cast."
sources:
  - https://ethereum.org/en/developers/docs/apis/json-rpc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Core JSON-RPC
```
curl -s -X POST "$RPC_URL" -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}'
```
- Quantities are hex without leading zeros (`0x1`, not `0x01`).
- Block tags: `latest`, `earliest`, `pending`, `safe`, `finalized`. Use `finalized` when a read must not be reorged away.
- `eth_call` runs without a transaction; state overrides go in an optional third param on supporting clients.
- Equivalents: `cast call`, `cast balance`, `cast block-number`.
- Gotcha: never commit an API-keyed URL; read it from an environment variable.

## Verify
- [ ] The response `id` matches the request and `result` (not `error`) is returned.
