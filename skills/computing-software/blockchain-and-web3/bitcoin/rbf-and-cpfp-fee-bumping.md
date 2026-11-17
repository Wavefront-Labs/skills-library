---
id: computing-software.blockchain-and-web3.bitcoin.rbf-and-cpfp-fee-bumping
name: rbf-and-cpfp-fee-bumping
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [replace-by-fee, cpfp, bumpfee]
level: practitioner
status: gated
description: "Bump a stuck transaction with RBF (BIP 125) or CPFP."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki
  - https://developer.bitcoin.org/reference/rpc/bumpfee.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fee bumping
- RBF (BIP 125, opt-in): a transaction signals replaceability; the replacement must pay an absolute fee of at least the sum paid by the transactions it replaces, and must also pay for its own bandwidth at or above the node's minimum relay fee rate.
- `bitcoin-cli bumpfee "txid"` bumps the fee of an opt-in-RBF transaction by replacing it with a new transaction that includes all the original inputs; it fails if the wallet or mempool holds a transaction spending one of the original's outputs. Its `fee_rate` option is in sat/vB since 0.21.
- CPFP: the recipient (or sender, via change) spends an unconfirmed output with a high-fee child so miners take both. Package feerate = (fee1 + fee2) / (vsize1 + vsize2). (gated: unconfirmed, source is paywalled or blocked)
- Cancelling: replace with a transaction paying yourself.
- Do not accept payments on 0-conf from untrusted senders.

## Verify
- [ ] The original txid disappears from the mempool and the replacement appears with the higher fee.
## Checked
2026-11-02. Confirmed against BIP 125 (replacement fee rules) and the `bumpfee` RPC reference. Gated: the CPFP definition and package feerate formula, which neither page states (no CPFP page was read). Removed: the claim about newer Core versions' default replaceability.
Method: documentation only; no commands were run.
