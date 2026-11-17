---
id: computing-software.blockchain-and-web3.smart-contract-security.invariant-and-fuzz-testing-for-security
name: invariant-and-fuzz-testing-for-security
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [invariant-testing, stateful-fuzzing, echidna-fuzzing]
level: advanced
status: draft
description: "Express protocol invariants and test them with Foundry invariant tests or Echidna."
sources:
  - https://book.getfoundry.sh/forge/invariant-testing
  - https://github.com/crytic/echidna
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Invariants and fuzzing
- Examples: conservation (sum of balances = total supply), solvency (assets >= liabilities), monotonic nonces, access rules.
- Foundry: contracts named with `invariant_` functions; a handler contract constrains random call sequences (`targetContract`, `targetSelector`). Configure `[invariant] runs`, `depth`.
- Echidna: property functions returning bool, config in YAML.
- Use handler "ghost variables" to track expected totals.
- A failing run prints a call sequence; reproduce it as a unit test and fix.

## Verify
- [ ] Invariants run with depth >= 50 and 256+ runs in CI without failure.
