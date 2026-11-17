---
id: computing-software.database-administration.mongodb.upgrades-and-feature-compatibility-version
name: upgrades-and-feature-compatibility-version
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-production-notes, mongodb-administration, feature-compatibility-version, setfeaturecompatibilityversion, rolling-upgrade, mongodb-upgrade, downgrade-path]
level: advanced
status: docs-checked
description: "Upgrade a MongoDB replica set or sharded cluster one major version at a time with rolling binary swaps, then raise featureCompatibilityVersion only after it has soaked."
sources:
  - https://www.mongodb.com/docs/manual/release-notes/8.0-upgrade-replica-set/
  - https://www.mongodb.com/docs/manual/reference/command/setFeatureCompatibilityVersion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrades and featureCompatibilityVersion

**Goal:** a major-version upgrade with no downtime and a working downgrade path
until you deliberately give it up.

## Rules
- Check MongoDB Versions and Upgrade Paths for the supported path before each step.
- Feature compatibility version (FCV) gates features that persist data incompatible with the older version; enabling them complicates downgrade, because persisted incompatible features must be removed first.
- Check driver compatibility with the target server version first.

## Replica set
```javascript
db.adminCommand({ getParameter: 1, featureCompatibilityVersion: 1 })   // current FCV
```
1. Upgrade secondaries one at a time: stop mongod, install new binaries, start,
   wait until `rs.status()` shows SECONDARY and caught up.
2. `rs.stepDown()` the primary, wait until another member is PRIMARY, upgrade the stepped-down primary the same way.
3. Soak: app tests, performance, error logs.
4. Raise FCV:
   ```javascript
   db.adminCommand({ setFeatureCompatibilityVersion: "8.0", confirm: true })   // confirm: true is required
   ```

## Sharded cluster
Follow the sharded cluster upgrade tutorial for your target version; it documents the order.
## Downgrade
Keep FCV at the old value for a burn-in period and raise it only when a downgrade is unlikely. To go back after raising it, set FCV back to the older version (after removing persisted incompatible features), as the setFeatureCompatibilityVersion page describes; plan this, and backups, explicitly.

## Gotchas
- Read the compatibility changes page for each version.

## Verify
`db.version()` on every member equals the target; `featureCompatibilityVersion`
shows the target after the final step; `rs.status()` all healthy.

## Checked

2026-10-28. Confirmed against MongoDB manual 8.0 replica set upgrade tutorial and setFeatureCompatibilityVersion page: upgrade secondaries one at a time, step down the primary and upgrade it once another member is PRIMARY, setFeatureCompatibilityVersion 8.0 with confirm: true, FCV 7.0 supported on 7.0 and 8.0 deployments, backwards-incompatible features must be removed before downgrade, burn-in advice, getParameter for FCV. Removed unconfirmed: the one-major-at-a-time chain, sharded upgrade order and balancer step, the 7.0+ confirm tag, since-7.0 downgrade claim, arbiter/hidden/Atlas notes.

Method: documentation only; no commands were run.
