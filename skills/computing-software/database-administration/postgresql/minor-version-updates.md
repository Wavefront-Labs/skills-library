---
id: computing-software.database-administration.postgresql.minor-version-updates
name: minor-version-updates
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-upgrade, major-version-upgrade, minor-version-update, patch-release, release-notes, rolling-restart, out-of-cycle-release]
level: practitioner
status: docs-checked
description: "Apply PostgreSQL minor releases (e.g. 17.5 to 17.6) promptly: read release notes for post-update steps, restart replicas first, then switch over, with minimal downtime."
sources:
  - https://www.postgresql.org/support/versioning/
  - https://www.postgresql.org/docs/18/upgrading.html
  - https://www.postgresql.org/docs/18/warm-standby.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minor version updates

**Goal:** every cluster runs the latest minor release of its major within weeks
of release, with seconds of downtime.

## What minor releases are
Per the versioning policy, minor releases contain fixes for frequently-encountered bugs, low-risk fixes, security issues and data corruption problems, and are released at least once every three months (see the minor release roadmap), with out-of-cycle releases for critical problems. They never change the internal storage format and are compatible with earlier and later minors of the same major: replace the executables while the server is down and restart, with no pg_upgrade or dump. The project recommends always running the current minor release; each major version is supported for 5 years after its first release.

## Read the release notes first
The docs say minor upgrades might require additional steps, so always read the release notes first. When you skip several minors, read the notes of every one you skip.

## Procedure for a primary with streaming standbys
1. Update the standby servers first and restart them: the docs say a new minor release is more likely to be able to read WAL from a previous minor than the reverse, and it is likely that different minor levels on primary and standby work, but keeping them at the same level is safest.
2. Then update the primary (a planned switchover to an updated standby or a restart of the primary in a quiet moment).
3. Update and restart the old primary if it became a standby.
4. Run any post-update steps from the notes.
Single server: install the updated binaries and restart; downtime = restart time.

## Gotchas
- Check what your package manager does to a running server on upgrade (some restart it, some do not) to avoid an unplanned restart; see your package documentation.
- Managed services: set maintenance windows and auto-minor-upgrade policies; they still restart.

## Verify
```sql
SELECT version();
SHOW server_version;
```
on every node equals the target minor; monitoring has a check that alerts when a
cluster is more than one minor behind.

## Checked
2026-10-25. Against the PostgreSQL versioning policy page (pgweb source of postgresql.org/support/versioning) and PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): minor release cadence (at least every three months, out-of-cycle releases possible), what minor releases contain, 5-year support window, "always run the current minor", read the release notes first, and the upgrading chapter (minor releases never change the storage format; replace executables and restart) and hot standby/high availability chapter (update standbys first; running different minors on primary and standby is likely to work). Removed the February/May/August/November month list (it belongs to the roadmap page, which was not read), the example version numbers, the `CHECKPOINT` tip, Patroni and specific packaging remarks, which the documentation checked does not give.
Method: documentation only; no commands were run.
