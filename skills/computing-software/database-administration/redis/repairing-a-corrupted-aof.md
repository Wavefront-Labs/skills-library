---
id: computing-software.database-administration.redis.repairing-a-corrupted-aof
name: repairing-a-corrupted-aof
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, aof, redis-check-aof, aof-load-truncated, multi-part-aof, crash-recovery]
level: practitioner
status: docs-checked
description: "Recover Redis when the AOF is truncated or corrupted: aof-load-truncated behaviour, redis-check-aof --fix on multi-part AOF, and what data you lose."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://redis.io/docs/latest/operate/oss_and_stack/management/config-file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repairing a truncated or corrupted AOF

## Truncated tail (common after power loss or a full disk)
The last command was partially written. With the default `aof-load-truncated yes`, Redis
loads everything up to the last complete command, logs a warning and starts:
```
* Reading RDB preamble from AOF file...
* Reading the remaining AOF tail...
# !!! Warning: short read while loading the AOF file !!!
# !!! Truncating the AOF at offset 439 !!!
# AOF loaded anyway because aof-load-truncated is enabled
```
You lose at most the incomplete command. If set to `no`, Redis refuses to start and you
fix the file manually.

## Corruption in the middle
Redis aborts startup:
```
# Bad file format reading the append only file: make a backup of your AOF file, then use ./redis-check-aof --fix <filename>
```
Procedure:
```bash
systemctl stop redis
cp -a /var/lib/redis/appendonlydir /var/lib/redis/appendonlydir.bak.$(date +%F-%H%M)
redis-check-aof /var/lib/redis/appendonlydir/appendonly.aof.manifest        # report only
redis-check-aof --fix /var/lib/redis/appendonlydir/appendonly.aof.manifest  # asks 'Continue? [y/N]', then truncates at the last valid offset
systemctl start redis
```
Since Redis 7.0 the AOF is **multi-part** (`appendonlydir/` with a base file `*.base.rdb` or
`.base.aof`, incremental `*.incr.aof` files, and a manifest): point the tool at the manifest.
`--fix` discards everything from the first invalid command **to the end of that file**, which
can be a lot of data. Inspect the reported offset first (`--truncate-to-timestamp <ts>` instead
truncates at the first `#TS:` annotation newer than the timestamp; the AOF must contain timestamp
annotations, which `aof-timestamp-enabled` records).

## Better options than losing data
- If a **replica** has a good copy, promote it or resync this node from it instead of repairing.
- Restore the most recent RDB snapshot / backup and accept loss since then.
- RDB base file corrupt: verify it with `redis-check-rdb`.

## Prevent
- Keep enough free disk: AOF rewrite needs space for the new base; a full disk can leave a
  truncated last command.
- `appendfsync everysec` (default): about one second of writes can be lost on a crash.
- Monitor `aof_last_write_status`, `aof_last_bgrewrite_status` in `INFO persistence`.
- Take regular backups of the RDB/AOF directory off the host.

## Verify
Redis starts, `INFO persistence` shows `aof_enabled:1` and `aof_last_write_status:ok`,
`DBSIZE` is in the expected range, and a sample of critical keys is present.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the persistence page: `aof-load-truncated` default yes loads the AOF minus the last malformed command and logs the quoted warning; the corruption message and advice to run redis-check-aof first without --fix; --fix may discard everything from the invalid part to the end of the file; Redis 7.0 multi-part AOF (base, incremental, manifest, `appenddirname`); everysec is the default and loses about one second. Confirmed from redis-check-aof.c: usage `[--fix|--truncate-to-timestamp $timestamp] <file.manifest|file.aof>`, --fix asks `Continue? [y/N]`, timestamp truncation uses `#TS:` annotations, only the last file of a multi-part AOF can be truncated. Removed unconfirmed: the exact log text with file names, the 7.0 label on --truncate-to-timestamp, the short-write log message, no-automatic-fix claim.
Method: documentation only; no commands were run.
