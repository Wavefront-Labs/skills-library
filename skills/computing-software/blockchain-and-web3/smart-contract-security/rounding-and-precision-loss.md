---
id: computing-software.blockchain-and-web3.smart-contract-security.rounding-and-precision-loss
name: rounding-and-precision-loss
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [rounding-direction, precision-loss, division-before-multiplication]
level: advanced
status: draft
description: "Choose rounding directions that favour the protocol and avoid divide-before-multiply precision loss."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/api/utils#Math
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rounding and precision
- Solidity integer division rounds toward zero. Multiply first, divide last: `a * b / c`, not `a / c * b`.
- Rule: round against the user and for the protocol: shares minted round down, assets owed for shares round up, fees round up.
- Beware tiny balances: `amount * rate / 1e18` becomes 0 for small amounts; reject or accumulate.
- Fixed-point libraries (WAD/RAY, PRBMath, Solmate/Solady FixedPointMathLib) document their rounding.
- Test rounding with fuzzing and asserting that totals never exceed deposits.

## Verify
- [ ] An invariant test asserts no sequence of tiny deposits/withdrawals nets a profit.
