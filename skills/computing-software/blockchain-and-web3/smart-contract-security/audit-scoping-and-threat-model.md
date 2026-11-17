---
id: computing-software.blockchain-and-web3.smart-contract-security.audit-scoping-and-threat-model
name: audit-scoping-and-threat-model
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [audit-scoping, threat-model-contracts, trust-assumptions, bc-sec-audit]
level: practitioner
status: draft
description: "Prepare a code base for review: scope, actors, trust assumptions, invariants and documentation."
sources:
  - https://github.com/crytic/building-secure-contracts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scoping and threat model
- Freeze a commit; list in-scope contracts and external dependencies (with versions).
- Document actors (users, admins, keepers, oracles) and what each is trusted to do.
- Write down invariants in plain language ("total shares x price = assets", "only governance can change fee").
- Describe expected token behaviours and unsupported ones (fee-on-transfer, rebasing).
- Provide specification, architecture diagram, test coverage report and known issues list.
- Plan reviews for each change after the audit; audits do not carry over to modified code.

## Verify
- [ ] A reviewer can state the top five risks from your document without reading code.
