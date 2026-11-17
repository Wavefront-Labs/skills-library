---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.slither-static-analysis
name: slither-static-analysis
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [slither-analysis, slither-detectors, slither-printers, bc-tool-static]
level: practitioner
status: draft
description: "Run Slither, triage detector output, and use printers to understand a code base."
sources:
  - https://github.com/crytic/slither
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slither
- Install: `pip install slither-analyzer` (needs solc via `solc-select`).
- Run: `slither .` (Foundry/Hardhat projects autodetected); `--exclude-dependencies`, `--filter-paths lib`.
- Triage by impact/confidence; suppress justified findings with `// slither-disable-next-line <detector>`.
- Printers: `--print contract-summary`, `function-summary`, `inheritance-graph`, `human-summary`.
- Output SARIF/JSON for CI: `--sarif out.sarif`.
- Static analysis finds patterns, not logic bugs; it supplements tests and review.

## Verify
- [ ] CI step fails on new high-severity findings and passes with an approved baseline.
