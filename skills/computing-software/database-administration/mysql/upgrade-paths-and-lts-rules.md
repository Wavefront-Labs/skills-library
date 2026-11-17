---
id: computing-software.database-administration.mysql.upgrade-paths-and-lts-rules
name: upgrade-paths-and-lts-rules
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-upgrade, upgrade-path-mysql, lts, innovation-release, version-planning]
level: practitioner
status: docs-checked
description: "Plan a supported MySQL upgrade path under the LTS and Innovation model: which jumps are allowed, why you cannot skip an LTS, and downgrade limits."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/upgrade-paths.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html
  - https://dev.mysql.com/doc/refman/8.4/en/downgrading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade paths and LTS rules

## Release model
- **LTS** series (8.4, then 9.7 LTS ...): only necessary fixes within the series, no removals; a series follows
  the Oracle Lifetime Support Policy (5 years premier plus 3 years extended). For production.
- **Innovation** releases: new features and behaviour changes; supported only until the next Innovation release.
- Monthly Rapid Updates and hot fixes count as releases for the path rules.

## Allowed paths (in-place, logical dump/load, or replication)
| From | To | Allowed |
|---|---|---|
| Within an LTS or bugfix series | later release of it (8.4.0 -> 8.4.4) | yes (MySQL Clone also works) |
| LTS or bugfix series (e.g. 8.0) | next LTS (8.4) | yes, directly |
| LTS | an Innovation release before the next LTS (8.4.0 -> 9.0.0) | yes |
| Innovation | next LTS (8.3.0 -> 8.4) | yes |
| Within an Innovation series | later one (8.1.0 -> 8.3.0) | yes |
| Innovation | an Innovation after the next LTS | **no**: go 8.3.0 -> 8.4 LTS -> 9.x |
| Any LTS | the LTS after next (skipping one) | **no** |
| 5.7 | 8.4 | **no**: 5.7 -> 8.0 -> 8.4 |
A replication topology is upgraded with the rolling scheme (replicas first, then switch over), using one
supported single-server method per server.

## Downgrade
- Within an LTS series: in-place, logical dump/load, MySQL Clone or replication.
- To the previous LTS or an earlier Innovation series: logical dump/load or replication only, and only for rollback
  (no new server functionality applied to the data). Downgrading to 5.7 or earlier is not supported.
- Therefore: take a full backup (and keep the old binaries) before upgrading; the realistic rollback is restore or
  failing back to a not-yet-upgraded replica.

## Planning checklist
1. Read the release notes and "Changes in MySQL 8.4" for removed variables and changed defaults.
2. Run MySQL Shell's Upgrade Checker, `util.checkForServerUpgrade()`, against the current server before upgrading.
3. Check connectors/ORMs support the target version.
4. Upgrade replicas first, run them on read traffic, then switch over and upgrade the old source.
5. Upgrade backup tools, monitoring and proxies in step.

## Verify
`SELECT @@version, @@version_comment;` on every node shows the target; the upgrade checker reports no errors before
starting, and replication between mixed versions stayed healthy during the rolling phase.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual pages Upgrade Paths (3.2), MySQL Releases: Innovation and LTS
(1.3) and Downgrading MySQL (chapter 4): path table, no LTS skipping, 5.7 via 8.0, 5.7 downgrade unsupported,
rollback-only downgrade methods, support-period wording. Removed as unconfirmed: end-of-life dates, release cadence,
the specific 8.4 changed defaults, and connector syntax claims.
Method: documentation only; no commands were run.
