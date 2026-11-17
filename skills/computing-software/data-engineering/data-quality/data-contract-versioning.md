---
id: computing-software.data-engineering.data-quality.data-contract-versioning
name: data-contract-versioning
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, data-contracts, contract-versioning, breaking-changes, semantic-versioning, deprecation, odcs, datacontract-cli]
level: advanced
status: verified
description: "Version data contracts: classify breaking vs non-breaking changes, semantic versioning, detecting breaks in CI with datacontract-cli, parallel versions and deprecation windows."
sources:
  - https://bitol-io.github.io/open-data-contract-standard/latest/
  - https://cli.datacontract.com/
  - https://semver.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data contract versioning

**Goal:** producers can evolve datasets while consumers get advance notice and a migration path for anything that would break them.

## Classify changes
| Change | Type |
|---|---|
| Add optional column | non-breaking (minor) |
| Add enum value | potentially breaking (consumers with exhaustive mapping) -> treat as minor with notice |
| Loosen constraint (nullable, wider type) | usually non-breaking for readers; breaking for consumers relying on not-null |
| Remove/rename column, change type, tighten constraint, change grain/primary key, change semantics (units, definition) | **breaking (major)** |
| Change SLA (freshness, availability) for worse | breaking for SLA-dependent consumers |
| Docs/description fixes | patch |

Semantic changes without schema changes (revenue now net of tax) are the most dangerous; they must bump major even though no tool detects them.

## SemVer in the contract
```yaml
# ODCS-style contract excerpt
apiVersion: v3.0.2
kind: DataContract
id: sales-orders
version: 2.1.0
status: active
schema:
  - name: orders
    physicalName: sales.orders_v2
    properties:
      - {name: order_id, logicalType: string, required: true, primaryKey: true}
      - {name: amount_net, logicalType: number, required: true, description: "Net of tax, EUR"}
```
Major version usually maps to a new physical object (`orders_v2` table/view, `orders.v2` topic) so v1 and v2 can coexist.

## Detect breaking changes in CI
```bash
git show origin/main:contracts/orders.yaml > /tmp/orders-main.yaml          # the CLI takes file paths or URLs, not `file@ref` (tested: file does not exist)
datacontract changelog /tmp/orders-main.yaml contracts/orders.yaml            # list changes
datacontract breaking /tmp/orders-main.yaml contracts/orders.yaml             # exit code 1 on breaking changes
datacontract test contracts/orders.yaml                                      # verify the live dataset matches
```
Tested with datacontract-cli 1.2.7: removing a property while changing `version` 2.1.0 to 1.1.0 still returned exit code 1 and the changelog listed the version change as INFO, so the tool does not itself compare version bumps. Gate merges with a script: if `breaking` fails and the major number in `version` did not increase, fail the PR.

## Rolling out a major version
1. Publish v2 alongside v1 (new table/view/topic), both maintained.
2. Notify consumers (from the contract's consumer list / lineage), with migration notes and deadline.
3. Track adoption via access logs/lineage.
4. Mark v1 `status: deprecated` with a sunset date; after the date and zero usage, retire it.

## Gotchas
- Views over a single physical table can serve v1 (compat projection) and v2 simultaneously, cheaply.
- Consumers outside the catalog (ad hoc exports) are invisible; access logs catch them.
- Dropping v1 early erodes trust in contracts more than any outage.

## Verify
- [ ] CI fails a PR that removes a column without bumping the major version.
- [ ] Each deprecated version has a sunset date and a usage query showing remaining consumers.
