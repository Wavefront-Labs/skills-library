---
id: computing-software.cybersecurity-defensive.splunk.splunk-config-and-kvstore-backup
name: splunk-config-and-kvstore-backup
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, kvstore-backup, kv-store, backup-and-restore, splunk-platform-admin, search-head-clustering, disaster-recovery]
level: practitioner
status: draft
description: "Back up Splunk configuration and the KV store (kvstore backup/restore commands, etc/ snapshots, ES collections) and rehearse restores on search heads and clusters."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Admin/BackupKVstore", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Backupconfigurations", "https://docs.splunk.com/Documentation/Splunk/latest/DistSearch/BackuprestoreSHC"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Backing up Splunk configuration and KV store

What you lose without backups: ES notable status/ownership, investigations, asset/identity merged
lookups, threat intel collections, user knowledge objects and app configs. Index data is protected
by replication, not by this.

## Configuration
- Back up `$SPLUNK_HOME/etc` (apps, users, system/local, auth secrets incl. `splunk.secret`,
  `passwd`) from search heads, deployer, cluster manager and deployment server.
- Better: keep apps in git and deploy from it; still snapshot `etc/users` and `etc/apps/*/local`
  daily since users and UI edits write there.
- Without the matching `splunk.secret`, encrypted passwords in configs cannot be decrypted on restore.

## KV store
```
splunk backup kvstore -archiveName kv-$(date +%F) [-appName SplunkEnterpriseSecuritySuite -collectionName incident_review]
splunk show kvstore-backup-status   # (or check $SPLUNK_HOME/var/lib/splunk/kvstorebackup)
splunk restore kvstore -archiveName kv-2026-10-18.tar.gz [-appName ... -collectionName ...]
```
- Run online on one SHC member; backup is consistent per collection. Archives land in
  `var/lib/splunk/kvstorebackup`; copy them off-host.
- Point-in-time restore overwrites the collection; restore one collection to recover a single
  lookup without rolling back everything.
- Splunk 9.x: KV store server version upgrades (MongoDB) require a backup first.

## Search head cluster
- Back up from one member; restoring KV store on one member replicates.
- For a total loss: rebuild members, restore `etc` from the deployer bundle, then restore KV store.

## Gotchas
- Large ES collections make backups slow; schedule off-peak and monitor disk.
- `kvstore` status `failed`/`starting` before backup means a corrupt or out-of-sync member; resync
  (`splunk resync kvstore`) first.

## Verify
Quarterly restore test on a lab search head: restore etc and KV store, open Incident Review,
confirm notable history and asset counts match production.
