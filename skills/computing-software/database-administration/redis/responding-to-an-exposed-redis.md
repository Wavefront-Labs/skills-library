---
id: computing-software.database-administration.redis.responding-to-an-exposed-redis
name: responding-to-an-exposed-redis
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-security, exposed-redis, incident-response, config-set-dir, protected-mode, cryptominer]
level: advanced
status: docs-checked
description: "Respond when a Redis instance was reachable without auth: firewall it, check CONFIG dir/dbfilename abuse, assume the host may be compromised, then harden."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/
  - https://redis.io/docs/latest/commands/config-set/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to an exposed Redis instance

Redis is designed for trusted clients in trusted environments. Left reachable from the internet, a single `FLUSHALL` from an outsider deletes the whole dataset. Worse, `CONFIG SET` lets a client change the server's working directory (`dir`) and dump file name (`dbfilename`), so an attacker can write RDB files to arbitrary paths, which can compromise the system and run untrusted code as the Redis user. Assume the **host** may be compromised, not just the data.

## 1. Contain
- Firewall the Redis port so only the application hosts can reach it (loopback still works).

## 2. Inspect Redis state
```
CONFIG GET dir
CONFIG GET dbfilename
CONFIG GET *          # lists every parameter CONFIG SET can change
MODULE LIST           # unknown modules
ROLE                  # unexpected replication role or master
ACL LIST              # unknown users
```
An unexpected `dir` or `dbfilename`, or an RDB written outside the data directory, indicates the config-write abuse above. Treat the host as compromised and rebuild it from a clean image; rotate credentials stored on it.

## 3. Harden
```
bind 127.0.0.1                    # one or more private interfaces only
user default off                  # ACLs (Redis 6+) are the recommended auth; requirepass is legacy
tls-port 6380                     # TLS covers client, replication and cluster-bus traffic
```
- Protected mode (since 3.2.0) only protects a default config with all interfaces bound and no password; an administrator can disable it or bind all interfaces, so do not rely on it.
- If you need a password, make it very long: Redis answers many guesses per second. `AUTH` is sent unencrypted, so it does not stop an eavesdropper.
- Restrict dangerous commands with ACL rules. `rename-command CONFIG ""` still works but is deprecated and may be removed.
- Run Redis as an unprivileged `redis` user (no root needed).

## 4. Restore data
Prefer a known-good backup from before the exposure; do not trust the current dataset.

## Verify
An external scan shows the port closed, and an unauthenticated client cannot run commands.

## Checked

2026-11-09. Pages read in full against this skill:
- https://redis.io/docs/latest/operate/oss_and_stack/management/security/
- https://redis.io/docs/latest/commands/config-set/

Confirmed: exposure risk, CONFIG dir/dbfilename abuse, protected mode, ACL vs requirepass, rename-command deprecation, TLS scope, unprivileged user, CONFIG GET *.
Removed or reworded: the attack-technique list (SSH key, cron, rogue master, module load, ransom/miner), forensic host checks, systemd hardening, enable-protected-configs/enable-debug-command/enable-module-command settings, and CLIENT LIST/INFO inspection steps; none is stated on the cited pages. The earlier advice to use rename-command for older versions was reworded because the page marks it deprecated. The commands ROLE, MODULE LIST and ACL LIST appear only as command names in the page's related list; their output was not read.

Method: documentation only; no commands were run.
