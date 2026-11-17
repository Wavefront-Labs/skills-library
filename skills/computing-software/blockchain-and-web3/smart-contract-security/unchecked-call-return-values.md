---
id: computing-software.blockchain-and-web3.smart-contract-security.unchecked-call-return-values
name: unchecked-call-return-values
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [unchecked-call-return, swc-104, low-level-call-check, bc-sec-calls]
level: practitioner
status: draft
description: "Never ignore return values of low-level calls or non-reverting token functions."
sources:
  - https://swcregistry.io/
  - https://consensys.github.io/smart-contract-best-practices/development-recommendations/general/external-calls/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unchecked return values
- `call`, `send`, `delegatecall`, `staticcall` return false instead of reverting. Require the result.
- Token `transfer` may return false (non-standard tokens); use SafeERC20.
- Check that the target has code before low-level calls to addresses that might be EOAs (a call to an EOA "succeeds").
- Prefer typed interface calls that revert on failure.
- Static analysis (`slither --detect unchecked-lowlevel,unchecked-transfer`) finds most cases.

## Verify
- [ ] Slither reports no unchecked-call findings, or each is justified.
