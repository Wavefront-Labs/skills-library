---
id: computing-software.email-administration.mailcow.mailcow-cold-standby-script
name: mailcow-cold-standby-script
category: computing-software
field: email-administration
product: mailcow
tags: [cold-standby, create-cold-standby, mariabackup, rsync-remote, ssh-key, disaster-recovery]
level: advanced
status: docs-checked
description: "Keep a consistent remote copy of a running mailcow with create_cold_standby.sh, which uses mariabackup and rsync over SSH without downtime."
sources: ["https://docs.mailcow.email/backup_restore/b_n_r-coldstandby/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow cold-standby copy

`create_cold_standby.sh` in the mailcow base directory makes a consistent copy of a running installation on a remote host without downtime. It reads each project volume with `docker inspect`, uses `mariabackup` for a consistent SQL copy, rsyncs with `--delete` so the destination is an exact copy, then runs `docker compose pull` and removes old image tags there. The source is never changed.

Setup: edit the exported `REMOTE_SSH_KEY`, `REMOTE_SSH_PORT` and `REMOTE_SSH_HOST` variables in the script. The key must be passwordless, and owned and readable by root only. Both ends need rsync 3.1.0 or newer; the destination needs Docker and Docker Compose v2, and should use the same `/etc/docker/daemon.json`. Test with an ssh login first.

Run `bash create_cold_standby.sh`; the same command refreshes the standby. Cron example: `0 3 * * * bash /opt/mailcow-dockerized/create_cold_standby.sh 2> /var/log/mailcow-coldstandby-sync.log`.

Limits: it targets default installs and may break with unsupported volume overrides; local bind mounts may or may not work. Versioning is not included, so rely on snapshots at the destination, and do not snapshot the target while the script runs. When switching between x86 and ARM64 the script detects the difference and omits the Rspamd volume, which regenerates its cache on the new platform.

## Checked

2026-11-04. Confirmed on the Cold-standby page: docker inspect volume discovery, mariabackup, rsync --delete, docker compose pull afterwards, REMOTE_SSH_* variables, passwordless root-only key, rsync 3.1.0 and Docker Compose v2 requirements, daemon.json advice, cron example, unsupported volume overrides, no versioning, no snapshots during a run, and the x86/ARM64 Rspamd volume omission. No changes needed.

Method: documentation only; no commands were run.
