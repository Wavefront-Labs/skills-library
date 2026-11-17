---
id: computing-software.blockchain-and-web3.bitcoin.vbytes-weight-and-fee-estimation
name: vbytes-weight-and-fee-estimation
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [virtual-size, weight-units, estimatesmartfee, bc-btc-fees]
level: practitioner
status: gated
description: "Compute fees from virtual size, use estimatesmartfee and set a sensible feerate."
sources:
  - https://developer.bitcoin.org/reference/rpc/estimatesmartfee.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fees
- `estimatesmartfee conf_target` estimates the approximate fee per kilobyte needed for a transaction to begin confirmation within `conf_target` blocks, using virtual transaction size as defined in BIP 141.
- Weight units: non-witness bytes count 4, witness bytes count 1; vsize = weight / 4. Fee = feerate (sat/vB) x vsize. (gated: unconfirmed, source is paywalled or blocked)
- The `estimatesmartfee` result is per kilobyte: convert to sat/vB before comparing with other tools. (gated: unconfirmed, source is paywalled or blocked)
- The `bumpfee` `fee_rate` option is in sat/vB as of 0.21 (before 0.21 it was BTC/kvB).

## Verify
- [ ] The final transaction's `fee / vsize` matches the requested feerate.
## Checked
2026-11-02. Confirmed against the `estimatesmartfee` and `bumpfee` RPC references. Gated: the weight formula (BIP 141 not read) and the unit conversion. Removed: `getmempoolinfo` floors, `fundrawtransaction`/`walletcreatefundedpsbt` fee_rate units and the freshly-synced-node note.
Method: documentation only; no commands were run.
