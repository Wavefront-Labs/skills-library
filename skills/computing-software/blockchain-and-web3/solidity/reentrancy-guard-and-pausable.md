---
id: computing-software.blockchain-and-web3.solidity.reentrancy-guard-and-pausable
name: reentrancy-guard-and-pausable
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [reentrancy-guard, pausable-contract, emergency-stop]
level: practitioner
status: docs-checked
description: "Apply nonReentrant and a pause switch sensibly without creating new lock-in risk."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/api/utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReentrancyGuard and Pausable
- `ReentrancyGuard` `nonReentrant` blocks nested entry into guarded functions; because there is a single guard, `nonReentrant` functions cannot call one another (work around with an external `nonReentrant` entry point calling a `private` function). Use `ReentrancyGuardTransient` where EIP-1153 transient storage is available. `nonReentrantView` blocks view functions. Cross-contract reentrancy still needs design (practitioner note).
- Put `nonReentrant` first among modifiers (practitioner convention).
- `Pausable` provides `whenNotPaused`/`whenPaused` modifiers that only take effect where you apply them, and an authorized account triggers the pause. Use `whenNotPaused` on user flows; keep withdrawals possible when paused unless funds are at risk, so a pause cannot trap users forever.
- Pausing power is a trust assumption; give it to a multisig, and keep `unpause` rules documented.

## Verify
- [ ] Reentrant attacker test fails with ReentrancyGuardReentrantCall.

## Checked

- Confirmed: nonReentrant single-guard limitation, ReentrancyGuardTransient/EIP-1153, ReentrancyGuardReentrantCall error, Pausable modifiers. Modifier order and multisig advice are practitioner guidance.

Method: docs-checked 2026-11-09 against OpenZeppelin Contracts 5.x api/utils page (ReentrancyGuard, ReentrancyGuardTransient, Pausable).
