---
id: computing-software.search-and-information-retrieval.apache-solr.backup-restore-collections
name: backup-restore-collections
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [backup-restore, backup, restore, collection-backup, backup-repository, replication-handler-backup]
level: practitioner
status: docs-checked
description: "Back up and restore Solr: Collections API BACKUP, RESTORE, LISTBACKUP, DELETEBACKUP with location, name, repository and async, plus per-core replication backup and restore."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/backup-restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backup-restore-collections

Backups and snapshots capture hard-committed data only, and can be restored to the same number of shards and replicas.

SolrCloud: `action=BACKUP`, `RESTORE`, `LISTBACKUP` (backup points and metadata at a location), `DELETEBACKUP` (files or whole backups). Backup is asynchronous and reflects the latest commit point. A shared file system mounted at the same path on all nodes is required.

Common parameters: `name`, `collection`, `location` (backup directory), `repository` (a configured repository; the local file system repository is used if absent), `async`.

User-managed and per-core: the ReplicationHandler creates backups; restore with `http://localhost:8983/solr/gettingstarted/replication?command=restore&name=backup_name`. It restores the named snapshot into the current core, and searches reflect it when the restore completes. Optional `location` and `repository` parameters apply. Snapshot directories are named `snapshot.<name>`, or `snapshot.<timestamp>` when no name is given.

Cap retained backups with `maxNumberOfBackups` on the ReplicationHandler.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Backup and Restore page: hard-committed data only, the Collections API actions, asynchronous backup from the latest commit point, shared file system requirement, `repository` default, the replication `command=restore` URL, `snapshot.<name>` and timestamp directory naming, restore completion, and `maxNumberOfBackups`. Nothing removed.

Method: documentation only; no commands were run.
