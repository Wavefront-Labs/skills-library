---
id: computing-software.database-administration.mysql.streaming-binlog-backups
name: streaming-binlog-backups
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqlbinlog-raw-backup, binlog-streaming, mysqlbinlog, point-in-time-recovery, read-from-remote-server, binlog-backup]
level: practitioner
status: docs-checked
description: "Continuously copy MySQL binary logs off the server with mysqlbinlog --read-from-remote-server --raw --stop-never so PITR survives losing the host."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog-backup.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog.html
  - https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming binary log backups

Full backups every night + binlogs only on the server = losing the server loses up to a day. Streaming binlogs to a backup host as they are written cuts that to seconds.

## Account
```sql
CREATE USER 'binlog_stream'@'10.0.5.%' IDENTIFIED BY '<PASSWORD>' REQUIRE SSL;
GRANT REPLICATION SLAVE ON *.* TO 'binlog_stream'@'10.0.5.%';    -- REPLICATION REPLICA alias in 8.0.26+
```

## Stream
```bash
cd /backup/binlogs/db1
mysqlbinlog --read-from-remote-server --host=db1 --user=binlog_stream --password=... \
  --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem \
  --raw --stop-never --verify-binlog-checksum \
  --connection-server-id=9901 \
  binlog.000123          # first file to fetch; must still exist on the server
```
- `--raw` writes binary files with the server's names (`binlog.000123` ...), identical to the originals.
- `--stop-never` keeps the connection open and waits for new events like a replica; `--connection-server-id` must be unique among replicas.
- Credentials: use `--login-path` (mysql_config_editor) instead of a password on the command line.

## Keep it running
systemd unit with `Restart=always`. On restart, resume from the **last file in the directory** (re-fetch it entirely: the last file may be partial):
```bash
LAST=$(ls -1 binlog.[0-9]* | tail -1)
exec mysqlbinlog --read-from-remote-server ... --raw --stop-never "$LAST"
```

## Monitor
- Newest local file name/size vs `SHOW BINARY LOG STATUS` on the source; alert if more than one file behind or the process is down.
- Source-side retention (`binlog_expire_logs_seconds`) must exceed the longest streaming outage you tolerate; once a file is purged on the source before being streamed, there is a PITR gap.

## Using them for PITR
Restore the last full backup, then:
```bash
mysqlbinlog --start-position=<pos-from-backup> binlog.000123 binlog.000124 ... --stop-datetime="2026-10-18 10:41:00" | mysql -u root -p
# with GTIDs: --exclude-gtids / --include-gtids, or --skip-gtids when replaying into a server with different GTID history
```
Replay all files in one mysqlbinlog invocation so temporary tables and session state carry across files.

## Gotchas
- Encrypted binlogs (`binlog_encryption=ON`) are sent decrypted over the replication protocol; protect the stream with TLS and the files at rest.
- Timestamps in `--stop-datetime` are server local time of the events; use positions or GTIDs for exactness.

## Checked

2026-10-31: confirmed on dev.mysql.com 8.4 mysqlbinlog pages: --read-from-remote-server (requires the REPLICATION SLAVE privilege), --raw (one binary output file per log file, same names as the originals), --stop-never (live backup; implies --to-last-log), --connection-server-id (default reported ID 1 with --stop-never), --verify-binlog-checksum, --login-path with mysql_config_editor, no automatic reconnect after connection loss (restart mysqlbinlog to resume), copies of encrypted binary logs stored unencrypted, --stop-datetime, --include-gtids/--exclude-gtids/--skip-gtids, and replaying all files in a single mysqlbinlog invocation for point-in-time recovery.
Method: documentation only; no commands were run.
