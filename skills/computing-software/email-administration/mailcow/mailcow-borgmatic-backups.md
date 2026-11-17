---
id: computing-software.email-administration.mailcow.mailcow-borgmatic-backups
name: mailcow-borgmatic-backups
category: computing-software
field: email-administration
product: mailcow
tags: [borgmatic, borg-passphrase, deduplicated-backup, retention-policy, mariadb-dump, storage-box]
level: advanced
status: docs-checked
description: "Run continuous encrypted, deduplicated mailcow backups with the borgmatic container, a compose override and a config.yaml with retention and MariaDB dumps."
sources: ["https://docs.mailcow.email/third_party/borgmatic/third_party-borgmatic/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backing up mailcow with borgmatic

borgmatic runs as an extra container (`ghcr.io/borgmatic-collective/borgmatic`) defined in `docker-compose.override.yml` as `borgmatic-mailcow`. It mounts the vmail, crypt, redis, rspamd and postfix volumes read-only under `/mnt/source/`, the MySQL socket volume, Borg config and cache volumes, and `data/conf/borgmatic/etc` and `ssh`. Environment: `TZ`, `BORG_PASSPHRASE` (append a strong value to `mailcow.conf`), `DBNAME`, `DBUSER`, `DBPASS`. The read-only mount must be removed before restoring.

`data/conf/borgmatic/etc/config.yaml` lists `source_directories`, `repositories` (for example an ssh:// path on a storage box), `exclude_patterns` for sockets, retention such as `keep_hourly: 24`, `keep_daily: 7`, `keep_weekly: 4`, `keep_monthly: 6`, and `mariadb_databases` using `${DBNAME}`, `${DBUSER}`, `${DBPASS}`. Version notes: borgmatic 1.8.0 changed the config syntax; since 1.9.4 the MariaDB tools force encrypted connections, so add `--skip-ssl` to `options`, `list_options` and `restore_options` and use `mariadb_databases` rather than `mysql_databases`.

Schedule with `data/conf/borgmatic/etc/crontab.txt`, for example `14 * * * * PATH=$PATH:/usr/local/bin /usr/local/bin/borgmatic --stats -v 0 2>&1`. Put the SSH key in `data/conf/borgmatic/ssh` with mode 600. Bring the container up, initialise the repository (confirm the host key; `repokey` modes store the key in the repository, a `keyfile` must be exported and backed up separately), then restart the container. For a local destination mount it at the container's `/mnt/borg-repository` volume.

## Checked

2026-11-04. Confirmed on the Borgmatic page: the image, the compose override services and read-only mounts, BORG_PASSPHRASE in mailcow.conf, config.yaml keys and retention values, the 1.8.0 and 1.9.4 version notes with --skip-ssl and mariadb_databases, crontab.txt example, SSH key mode 600, init with repokey, keyfile export warning, and /mnt/borg-repository. No changes needed.

Method: documentation only; no commands were run.
