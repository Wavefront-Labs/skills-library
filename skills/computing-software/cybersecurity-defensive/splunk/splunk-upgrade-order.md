---
id: computing-software.cybersecurity-defensive.splunk.splunk-upgrade-order
name: splunk-upgrade-order
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, splunk-upgrade, rolling-upgrade, indexer-clustering, search-head-clustering, compatibility-matrix, maintenance-mode]
level: advanced
status: draft
description: "Upgrade a distributed Splunk deployment in the right order: compatibility checks, cluster manager first, rolling indexer and SHC upgrades, forwarders last, and rollback."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Installation/HowtoupgradeSplunk", "https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Upgradeacluster", "https://docs.splunk.com/Documentation/Splunk/latest/DistSearch/UpgradeaSHC"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upgrading a distributed Splunk deployment

## Before
- Read the release notes "Known issues" and "Deprecated features" for the target version.
- Check app compatibility (Splunkbase version support; ES and its supporting add-ons have their
  own minimum Splunk versions). Run the Upgrade Readiness App for Python/jQuery issues.
- Forwarder compatibility: older UFs usually send to newer indexers fine; check the
  forwarder-indexer compatibility matrix.
- Back up `$SPLUNK_HOME/etc` everywhere and the KV store (`splunk backup kvstore`).
- Upgrade KV store engine/version first if the release requires it (`splunk show kvstore-status`).

## Order
1. **License manager**, **Monitoring Console**, **deployment server** (management components).
2. **Cluster manager**: upgrade, start, it stays in maintenance mode.
3. **Search heads / SHC**: either before or after peers per the docs for your version; for SHC
   use the rolling upgrade (`splunk upgrade-init shcluster-members`, then each member:
   `splunk upgrade-init shcluster-member`, stop, install, start, `splunk upgrade-finalize shcluster-member`).
   Upgrade the deployer as part of this step.
4. **Indexer peers**: searchable rolling upgrade
   ```
   splunk upgrade-init cluster-peers        # on manager
   splunk offline                           # on each peer in turn
   <install new version>; splunk start
   splunk upgrade-finalize cluster-peers    # on manager when all done
   ```
   Wait for all data searchable / RF+SF met between peers.
5. **Heavy forwarders**, then **universal forwarders** in waves via your software deployment tool.

## Rollback
Splunk has no in-place downgrade. Rollback = restore the previous version binaries plus the
`etc` backup; indexes created by the newer version may not be readable by older versions.
Hence: snapshot VMs or volumes before upgrading cluster managers and search heads.

## Gotchas
- Mixed versions across peers are supported only during the rolling window.
- First start after upgrade migrates configs and prompts for licence acceptance: use
  `--accept-license --answer-yes --no-prompt` in automation.
- ES upgrades are separate (install the new ES package via the setup page), after core Splunk.
- Python 2 code in custom apps breaks on Python 3-only releases.

## Verify
- `splunk version` on every node; Monitoring Console > Instances shows one version.
- Cluster manager dashboard: all peers up, SF/RF met, no fixup backlog.
- Scheduler skip ratio and searches/notables per hour back to the baseline.
