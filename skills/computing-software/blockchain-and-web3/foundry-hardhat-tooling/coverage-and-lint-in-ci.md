---
id: computing-software.blockchain-and-web3.foundry-hardhat-tooling.coverage-and-lint-in-ci
name: coverage-and-lint-in-ci
category: computing-software
field: blockchain-and-web3
product: foundry-hardhat-tooling
tags: [forge-coverage, forge-fmt, solhint-linting]
level: practitioner
status: draft
description: "Measure coverage with forge coverage, enforce forge fmt and solhint, and wire them into CI."
sources:
  - https://book.getfoundry.sh/reference/forge/forge-coverage
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coverage and lint
- `forge coverage` prints line/branch/function coverage; `--report lcov` for tooling. Coverage runs with the optimizer off, so numbers can differ from production behaviour.
- `forge fmt --check` in CI; `forge build --sizes`; `solhint 'src/**/*.sol'`.
- Aim for branch coverage of access control, error paths and edge values, not a vanity percentage.
- Pipeline: build, fmt check, test, snapshot check, slither, coverage upload.

## Verify
- [ ] CI is red when a test is removed that covered a revert branch.
