---
id: computing-software.blockchain-and-web3.smart-contract-security.incident-response-for-contracts
name: incident-response-for-contracts
category: computing-software
field: blockchain-and-web3
product: smart-contract-security
tags: [contract-incident-response, pause-and-monitor, post-mortem-contracts]
level: advanced
status: draft
description: "Prepare monitoring, pause authority and communication so a suspected exploit can be contained, then write a post-mortem."
sources:
  - https://ethereum.org/en/developers/docs/smart-contracts/security/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident response (defensive)
- Before launch: alerts on large transfers, role changes, `Upgraded` events and invariant breaks (e.g. via monitoring services or your own scripts).
- Know who can pause and how fast; test the runbook; keep signers reachable.
- During: pause, preserve evidence (tx hashes, block numbers), avoid public speculation until understood, coordinate with affected partners.
- Afterwards: root cause, timeline, user impact, fixes, and new tests that fail on the old code.
- Consider a published security contact and bug bounty policy.

## Verify
- [ ] A tabletop exercise reaches "paused" within the target time.
