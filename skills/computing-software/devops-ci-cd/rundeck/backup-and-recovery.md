---
id: computing-software.devops-ci-cd.rundeck.backup-and-recovery
name: backup-and-recovery
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, backup-restore, rd-jobs-list, data-directory, execution-logs]
level: practitioner
status: docs-checked
description: "Back up and restore a file-datastore Rundeck server: export jobs with rd, stop the server, copy data and log directories, and reload jobs."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backup (assumes the file datastore). Data files must only be copied with the server down.

1. Export jobs per project, if they are not in source control:
```bash
rd jobs list -f /path/to/backup/dir/project1/jobs.xml -p project1
```
2. Stop the server: `rundeckd stop`.
3. Copy the data directory: RPM install `/var/lib/rundeck/data`, launcher install `$RDECK_BASE/server/data`.
4. Copy the execution log directory: RPM `/var/lib/rundeck/logs`, launcher `$RDECK_BASE/var/logs`.
5. `rundeckd start`.

Other files worth saving: ACL policies in `$RDECK_BASE/etc`, server config in `$RDECK_BASE/server/config`, Key Storage in `$RDECK_BASE/var/storage`.

Recovery (server stopped):
1. `rundeckd stop`.
2. Copy the backed-up `logs` and `data` back to the paths above.
3. `rundeckd start`.
4. Reload jobs per project:
```bash
rd jobs load -f /path/to/backup/dir/project1/jobs.xml -p project1
```

Verify by checking jobs and past executions appear in the UI.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Backup and Recovery: rd jobs list/load commands, rundeckd stop/start, server must be down for data backup, RPM and launcher data and log paths, and the other files to save (etc, server/config, var/storage). Nothing removed.

Method: documentation only; no commands were run.
