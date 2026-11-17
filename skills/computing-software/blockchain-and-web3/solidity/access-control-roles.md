---
id: computing-software.blockchain-and-web3.solidity.access-control-roles
name: access-control-roles
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [access-control-roles, ownable2step, default-admin-role, bc-sol-openzeppelin]
level: practitioner
status: docs-checked
description: "Pick Ownable2Step or AccessControl, define roles, and protect DEFAULT_ADMIN_ROLE."
sources:
  - https://docs.openzeppelin.com/contracts/5.x/access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access control
- `Ownable2Step`: ownership transfer requires the new owner to `acceptOwnership`, preventing transfer to a wrong address.
- `AccessControl`: `bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");` guard with `onlyRole(MINTER_ROLE)`. `DEFAULT_ADMIN_ROLE` administers all roles by default unless `_setRoleAdmin` selects another admin role, and is its own admin, so it carries significant risk.
- Use `AccessControlDefaultAdminRules` (recommended by OpenZeppelin): admin restricted to a single account, with a 2-step transfer and a delay between steps.
- Grant the initial roles in the constructor (the docs example calls `_grantRole(DEFAULT_ADMIN_ROLE, msg.sender)`); consider handing admin to a multisig afterwards (practitioner advice).
- Base `AccessControl` has no on-chain member enumeration: monitor `RoleGranted`/`RoleRevoked` events off-chain, or use `AccessControlEnumerable`.

## Verify
- [ ] Test: a non-role account calling a protected function reverts with AccessControlUnauthorizedAccount.

## Checked

- Confirmed: Ownable2Step acceptOwnership, onlyRole, DEFAULT_ADMIN_ROLE semantics, DefaultAdminRules 2-step delay, event-based enumeration, AccessControlUnauthorizedAccount error.

Method: docs-checked 2026-11-09 against OpenZeppelin Contracts 5.x access-control guide and api/access page (Ownable2Step, AccessControl, DEFAULT_ADMIN_ROLE, AccessControlDefaultAdminRules, AccessControlUnauthorizedAccount, events).
