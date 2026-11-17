---
id: computing-software.cloud-infrastructure-engineering.netdata.backup-restore-agent
name: backup-restore-agent
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, backup, restore, var-cache-netdata]
level: practitioner
status: docs-checked
description: "Back up and restore a Netdata Agent: config, metrics database and identity directories, with the stop-before-database-copy order and the empty-cache warning."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/backup-and-restore-an-agent.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Data locations (verify first; they vary by install method, OS, Docker or Kubernetes):
- Configuration: `/etc/netdata/`
- Metrics database: `/var/cache/netdata`
- Identity (claim token, API key): `/var/lib/netdata`

Backup (as root or the `netdata` user), ideally with the Agent stopped:

```
sudo tar -cvpzf netdata_backup.tar.gz /etc/netdata/ /var/cache/netdata /var/lib/netdata
```

To minimise downtime: back up config and identity, stop the service, back up the database files, restart the Agent.

Restore:
1. Install the Agent without starting it:

```
wget -O /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh && sh /tmp/netdata-kickstart.sh --dont-start-it
```

2. Empty the metrics directory before restoring database files: `sudo rm -Rf /var/cache/netdata`
3. Extract:

```
sudo tar -xvpzf /path/to/netdata_backup.tar.gz -C /
```

4. Start the Agent.

Gotcha: the Agent must be stopped during restore.

## Checked

2026-11-04: data locations, path variations, the tar backup and restore commands, the stop recommendation, the minimised-downtime sequence, `--dont-start-it` and the empty-metrics-directory warning confirmed against the Netdata backup and restore page.

Method: documentation only; no commands were run.
