---
id: computing-software.blockchain-and-web3.smart-contract-security.access-control-audit-checklist
name: access-control-audit-checklist
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [access-control-audit, missing-modifier, tx-origin-misuse, bc-sec-access]
level: practitioner
status: draft
description: "Audit every state-changing function for authorisation, initialisers and tx.origin misuse."
sources:
  - https://swcregistry.io/
  - https://consensys.github.io/smart-contract-best-practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Access control audit
- Enumerate all external/public non-view functions (`forge inspect C methods`). For each: who may call, and is that enforced?
- Red flags: missing modifier on mint/burn/setX/withdraw; `initialize` callable by anyone or twice; `tx.origin` used for authorisation (SWC-115: phishable via an intermediary contract; use `msg.sender`); unprotected `selfdestruct`/`delegatecall`.
- Check role administration: who can grant roles, can the last admin renounce into a lock-out.
- Verify two-step ownership transfer and that deployer privileges are revoked after deploy.
- Write a negative test per privileged function (non-owner reverts).

## Verify
- [ ] Table of function -> allowed caller -> test name has no empty cells.
