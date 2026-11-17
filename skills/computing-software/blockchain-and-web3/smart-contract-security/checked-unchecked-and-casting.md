---
id: computing-software.blockchain-and-web3.smart-contract-security.checked-unchecked-and-casting
name: checked-unchecked-and-casting
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [checked-arithmetic, unchecked-block, truncating-cast, bc-sec-arith]
level: practitioner
status: draft
description: "Know where overflow protection stops: unchecked blocks, explicit casts, shifts and assembly."
sources:
  - https://docs.soliditylang.org/en/latest/control-structures.html#checked-or-unchecked-arithmetic
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checked arithmetic
- Solidity 0.8+ reverts on overflow/underflow outside `unchecked {}`.
- NOT protected: explicit narrowing casts (`uint8(x)` truncates), left shifts discarding bits, and any arithmetic in inline assembly.
- Review each `unchecked` block: write the invariant that makes overflow impossible next to it.
- Pre-0.8 code needs SafeMath; auditing old code means checking every `+ - *`.
- Intermediate overflow in `a * b / c`: use `Math.mulDiv`.

## Verify
- [ ] Fuzz tests with `type(uint256).max` boundaries pass on each arithmetic path.
