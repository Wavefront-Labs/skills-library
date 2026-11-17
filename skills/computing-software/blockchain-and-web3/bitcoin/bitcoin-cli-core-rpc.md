---
id: computing-software.blockchain-and-web3.bitcoin.bitcoin-cli-core-rpc
name: bitcoin-cli-core-rpc
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [bitcoin-cli, getblockchaininfo, getrawtransaction, bc-btc-rpc]
level: practitioner
status: draft
description: "Query chain, mempool and transactions with bitcoin-cli and understand verbosity levels."
sources:
  - https://developer.bitcoin.org/reference/rpc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# bitcoin-cli
- Chain: `getblockchaininfo` (sync progress, pruned, chain), `getblockcount`, `getblockhash <h>`, `getblock <hash> 2`.
- Tx: `getrawtransaction <txid> true` (requires `-txindex=1` for non-wallet, non-mempool txs), `decoderawtransaction`, `testmempoolaccept`.
- Mempool: `getmempoolinfo`, `getrawmempool`, `getmempoolentry`.
- Network: `getnetworkinfo`, `getpeerinfo`.
- Use `-rpcwallet=<name>` with multiple wallets; `-regtest` / `-testnet4`-style flags select networks (check the flag for your version).
- RPC credentials: prefer cookie auth or `rpcauth` over plaintext `rpcpassword`.

## Verify
- [ ] `getblockchaininfo.verificationprogress` is near 1 before trusting queries.
