---
id: computing-software.blockchain-and-web3.solidity.gas-snapshot-ci
name: gas-snapshot-ci
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [forge-snapshot, gas-regression, gas-report]
level: practitioner
status: docs-checked
description: "Track gas regressions with forge snapshot in CI."
sources:
  - https://github.com/foundry-rs/book/blob/master/src/pages/forge/gas-tracking.mdx
  - https://github.com/foundry-rs/book/blob/master/src/pages/reference/forge/snapshot.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gas snapshots
- `forge snapshot` writes `.gas-snapshot` (default; `--snap <FILE>` changes it) with the gas used by each test. Commit the file.
- Fuzz tests appear with runs, mean and median entries rather than a single number, for example `(runs: 256, μ: 31121, ~: 31277)`.
- `forge snapshot --diff` prints a difference against the existing snapshot (default `.gas-snapshot`).
- CI: `forge snapshot --check` compares against the existing snapshot and exits with code 1 if they do not match, printing a diff. `--tolerance <PERCENT>` tolerates deviations up to that percentage.
- When a gas change is intentional, rerun `forge snapshot` and commit the updated `.gas-snapshot`.
- Narrow the run with the usual test filters such as `--match-test`.
- `forge test --gas-report` prints min, avg, median, max and call counts per function; `gas_reports` and `gas_reports_ignore` in `foundry.toml` filter contracts.

## Verify
- [ ] CI fails on an intentional regression and passes on revert.

## Checked
Method: docs-checked 2026-11-09 against the Foundry book sources (raw MDX in the foundry-rs/book repository) for the gas tracking page and the forge snapshot reference page, both read; the original book.getfoundry.sh URLs are not fetchable. Dropped the advice to snapshot only deterministic tests, which the pages do not say.
