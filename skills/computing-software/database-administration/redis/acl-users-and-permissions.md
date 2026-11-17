---
id: computing-software.database-administration.redis.acl-users-and-permissions
name: acl-users-and-permissions
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-security, redis-acl, acl-setuser, acl-categories, key-patterns, default-user, aclfile, acl-log]
level: practitioner
status: docs-checked
description: "Lock down Redis 6+/7 with ACL users: per-app command categories and key patterns, disabling the default user, aclfile persistence, and debugging denials with ACL LOG."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
  - https://redis.io/docs/latest/commands/acl-setuser/
  - https://redis.io/docs/latest/commands/acl-log/
  - https://redis.io/docs/latest/develop/tools/cli/
  - https://raw.githubusercontent.com/redis/redis/unstable/sentinel.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redis ACLs

**Goal:** each client can run only the commands and touch only the keys it needs;
nobody can run FLUSHALL or CONFIG from an app credential.

## Define users
```
ACL SETUSER app_cache on >S3cret-long-pass ~cache:* &notifications:* +@read +@write -@dangerous
ACL SETUSER worker    on >Other-pass ~jobs:* +@list +@stream +@connection
ACL SETUSER monitor   on >Mon-pass nocommands +info +ping +client|list +slowlog|get +latency|latest
ACL SETUSER admin     on >Admin-pass ~* &* +@all
ACL SETUSER default off                     # disable the passwordless default user
```
Rule syntax: `on`/`off`; `>pass` adds a password (`#<sha256-hex>` adds a hashed one); `~pattern`
key access (`%R~` read-only, `%W~` write-only, 7.0+); `&pattern` pub/sub channels (6.2+);
`+@category` / `-@category`; `+cmd|subcmd` and `-cmd|subcmd` (7.0+); `resetkeys`, `reset`.
A new user is created off, with no passwords, no commands, no keys. Repeated `ACL SETUSER` calls
add to the existing user; start with `reset` to define it from scratch.
List categories: `ACL CAT`, `ACL CAT dangerous`.

## Persist
Either as `user` lines in redis.conf or, better for many users, an external file (the two methods
are mutually exclusive):
```
aclfile /etc/redis/users.acl
```
Then `ACL SAVE` after changes and `ACL LOAD` to reload (`ACL LOAD` is all-or-nothing: on an error the
old ACLs stay). With an `aclfile`, `CONFIG REWRITE` does not save users.

## Clients
`AUTH app_cache <password>` (two-argument form, 6.0+), or `redis-cli --user app_cache --pass ...`
(prefer the `REDISCLI_AUTH` environment variable over `-a`/`--pass` on the command line), or
`redis-cli -u redis://app_cache:<pw>@host:6379` (`rediss://` for TLS). Old clients that only send
`AUTH <password>` authenticate as `default`.

## Debug denials
```
ACL LOG 10          # recent events: reason is command, key, channel or auth; includes username and client-info
ACL DRYRUN app_cache GET cache:1    # 7.0+
```

## Gotchas
- Replicas need `+psync +replconf +ping` on the primary; configure the replica side with
  `masteruser`/`masterauth`. For Sentinel use `sentinel auth-user <master-name> <username>` with
  `sentinel auth-pass`; the ACL page lists the commands the Sentinel user needs.
- `-@dangerous` removes commands such as `KEYS`, `FLUSHALL`, `CONFIG`, `DEBUG`, `INFO` and `CLIENT`;
  check the exact list with `ACL CAT dangerous` and confirm apps do not need them (they should not
  need `KEYS`). `MONITOR` is in `@admin`; exclude it too if needed.
- Key patterns do not limit whole-keyspace commands such as `FLUSHALL`, `FLUSHDB` and `SWAPDB`:
  subtract them with `-@dangerous` or `-flushall -flushdb -swapdb`.
- ACL passwords are stored as fast SHA-256 hashes, not a slow password hash: use long random
  secrets (`ACL GENPASS` makes one), TLS and network isolation. ACLs are not a substitute for a firewall.
- Managed services have their own access-control setup; check the provider's documentation.

## Verify
`ACL LIST` shows `user default off ...`; as `app_cache`, `FLUSHALL` returns
`NOPERM this user has no permissions to run the 'flushall' command` and `GET other:1` returns
`NOPERM this user has no permissions to access one of the keys used as arguments`.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): ACL page, ACL SETUSER,
ACL LOG, redis-cli reference, and sentinel.conf from the redis/redis repository. Confirmed: rule syntax and
versions, default state of a new user, `reset`, aclfile versus redis.conf, `ACL SAVE`/`ACL LOAD` behaviour,
two-argument AUTH, `REDISCLI_AUTH`, replica command set, `sentinel auth-user`, the NOPERM message texts,
`ACL GENPASS`. Fixed: the NOPERM key message in Verify (it ends "used as arguments"); `@dangerous` is a
category you inspect with `ACL CAT`, and MONITOR is listed under `@admin`. Removed: the claim about
ElastiCache and Memorystore user-group APIs.
Method: documentation only; no commands were run.
