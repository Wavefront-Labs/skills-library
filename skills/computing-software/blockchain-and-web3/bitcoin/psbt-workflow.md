---
id: computing-software.blockchain-and-web3.bitcoin.psbt-workflow
name: psbt-workflow
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [psbt-workflow, walletcreatefundedpsbt, finalizepsbt]
level: advanced
status: gated
description: "Create, sign (possibly on an air-gapped signer), combine and broadcast transactions with PSBT (BIP 174)."
sources:
  - https://developer.bitcoin.org/reference/rpc/walletcreatefundedpsbt.html
  - https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSBT
1. Create: RPC `walletcreatefundedpsbt` returns the transaction as a base64-encoded PSBT (`psbt`); its `includeWatching` option defaults to true for watch-only wallets.
2. BIP-174 defines the roles: Creator, Updater, Signer, Combiner, Input Finalizer, Transaction Extractor. Signers must use the sighash type an input specifies.
3. The RPC names for the other steps (`decodepsbt`, `analyzepsbt`, `walletprocesspsbt`, `combinepsbt`, `finalizepsbt`, `testmempoolaccept`, `sendrawtransaction`) and their arguments: not confirmed on the pages read (gated: unconfirmed, source is paywalled or blocked). Check the Bitcoin Core RPC reference.
- Always verify destination and amounts on the signing device's screen.

## Verify
- [ ] Test acceptance (for example with the node's mempool test) before broadcasting.

## Checked

2026-11-02. Confirmed against the walletcreatefundedpsbt RPC page (base64 psbt, includeWatching) and BIP-174 (roles, sighash rule). Gated: the other RPC names and example arguments; the source was not read (only the one RPC page was fetched), not unreadable.
Method: documentation only; no commands were run.
