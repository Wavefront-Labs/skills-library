---
id: computing-software.database-administration.redis.protected-mode-bind-and-dangerous-commands
name: protected-mode-bind-and-dangerous-commands
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-security, protected-mode, rename-command, bind, enable-debug-command, config-set-attack, network-exposure, hardening]
level: practitioner
status: docs-checked
description: "Harden Redis network exposure: bind and protected-mode, firewalling, and disabling or ACL-restricting dangerous commands (CONFIG, DEBUG, MODULE, FLUSHALL, KEYS)."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/
  - https://raw.githubusercontent.com/redis/redis/7.2/redis.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network exposure and dangerous commands

**Goal:** Redis is reachable only by the hosts that need it, and a leaked app
credential cannot be turned into code execution on the server.

## Why it matters
An exposed Redis with no auth is a classic compromise path: `CONFIG` can change the working
directory and dump file name, so a client can write RDB files to arbitrary paths, which the
security page says may lead to running untrusted code as the Redis user.

## bind and protected-mode
```
bind 127.0.0.1 -::1 10.0.2.15        # only the interfaces you need (redis.conf default: 127.0.0.1 -::1)
protected-mode yes                   # default; with the default config (all interfaces) and no password, only loopback clients are served
port 6379
```
Protected mode is a safety net, not a control: once any password is set it no
longer blocks remote clients. Real controls: private network, security groups /
firewall allowing only app hosts, ACLs, TLS.

## Dangerous commands
Preferred (Redis 6+): remove them from app users with ACLs (`-@dangerous`,
`-@admin`), keeping them for an admin user only. Additional hardening in redis.conf:
```
enable-debug-command no              # 7.0+, default no; 'local' allows from loopback only
enable-module-command no             # 7.0+, block MODULE LOAD at runtime
enable-protected-configs no          # 7.0+, blocks CONFIG SET of security-sensitive settings (see redis.conf)
rename-command FLUSHALL ""           # legacy: disable entirely (affects replicas/AOF too, use with care)
rename-command CONFIG "CONFIG_8f3a2c"
```
`rename-command` is deprecated in favour of ACLs; redis.conf warns that renaming commands
that are logged to the AOF or sent to replicas may cause problems.

## Also
- Run as a non-root `redis` user with the data dir owned by it.
- Disable `KEYS` in app usage (use `SCAN`); it is not a security issue but an availability one.
- Containers: don't publish 6379 to 0.0.0.0 on the host.

## Verify
From an unauthorised host, `redis-cli -h <ip> PING` times out (firewall); from an
app host as the app user, `CONFIG GET dir` returns `NOPERM`; `CONFIG GET protected-mode`
and `CONFIG GET bind` show the intended values.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the security page and redis.conf (8.2 and 7.0): protected mode (since 3.2.0) applies with the default config and no password, only loopback is served; default `bind 127.0.0.1 -::1`; `enable-protected-configs`, `enable-debug-command`, `enable-module-command` exist in the 7.0 redis.conf with values no/yes/local; rename-command is deprecated in favour of ACLs; `+@all -@dangerous` category example and the @admin/@dangerous categories from the ACL page; CONFIG dir/dbfilename can write RDB files to arbitrary paths; run as an unprivileged redis user; KEYS is a latency risk. Removed unconfirmed: MODULE LOAD/replication attack description, the meaning of the leading dash in bind, specific protected settings, replica mismatch claim.
Method: documentation only; no commands were run.
