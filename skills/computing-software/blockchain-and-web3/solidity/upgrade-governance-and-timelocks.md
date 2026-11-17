---
id: computing-software.blockchain-and-web3.solidity.upgrade-governance-and-timelocks
name: upgrade-governance-and-timelocks
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [upgrade-governance, timelock-controller, multisig-admin]
level: practitioner
status: docs-checked
description: "Put upgrade rights behind a multisig and timelock so users get notice, and document the trust model."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/governance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade governance
- A single externally owned account holding upgrade rights is the main trust risk. Put the admin behind a multisig and/or a `TimelockController`, so queued changes are visible for a delay and users can exit if they disagree before execution.
- With a timelock, the timelock executes operations, so it is the timelock that should hold funds, ownership and access-control roles (for example a proxy admin's ownership).
- `TimelockController` roles: Proposer queues operations (normally only the Governor or the multisig); Executor runs operations that are ready (the zero address lets anyone execute); Canceller cancels queued operations (a Governor must hold it for cancellations to work, and a proposer receives it automatically at deployment); Admin grants and revokes the others.
- The Admin role is very sensitive. It goes to the timelock itself; an optional second account used for setup should promptly renounce it.
- Extra proposers or cancellers beyond the Governor are risky: they can execute operations as the timelock, bypassing governance, or cancel approved proposals.
- Publish the admin addresses, the delay and any emergency path, and monitor upgrade events.

## Verify
- [ ] The owner or admin of each proxy admin is the timelock or multisig, not a personal account.

## Checked
Method: docs-checked 2026-11-09 against the OpenZeppelin Contracts 5.x Governance guide, Timelock section read in full. Dropped the Safe-specific advice, the separate-canceller advice (the page says the Governor should hold the Canceller role), the renounce-upgradeability advice and the cast call command as not confirmed there.
