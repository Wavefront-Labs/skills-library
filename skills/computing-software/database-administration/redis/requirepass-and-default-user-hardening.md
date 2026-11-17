---
id: computing-software.database-administration.redis.requirepass-and-default-user-hardening
name: requirepass-and-default-user-hardening
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, redis-security, requirepass, masterauth, default-user, password-rotation, sentinel-auth, auth-command]
level: practitioner
status: docs-checked
description: "Set and rotate Redis passwords safely: requirepass vs ACL default user, masterauth for replicas, Sentinel auth, and multi-password rotation without downtime."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#the-default-user
  - https://redis.io/docs/latest/commands/auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# requirepass and the default user

**Goal:** every connection authenticates, replicas and Sentinels keep working,
and the password can be rotated with no outage.

## What requirepass really is
In Redis 6+, `requirepass <pw>` just sets a password on the ACL `default` user.
Clients sending one-argument `AUTH <pw>` authenticate as `default`.
```
requirepass "long-random-64-chars"
masterauth  "same-or-replication-user-password"     # on replicas (and on primaries that may become replicas)
masteruser  replicator                               # 6.0+, if replication uses a dedicated ACL user
```
Generate: `openssl rand -base64 48`. Redis checks passwords very fast, so short
passwords are brute-forceable at high rates.

## Rotation without downtime (ACL multi-password)
A user can have several valid passwords at once:
```
ACL SETUSER default >NEW-PASSWORD             # add new (old still valid)
-- roll new password to every client, replica masterauth (CONFIG SET masterauth ...), Sentinel config
ACL SETUSER default <OLD-PASSWORD             # remove old
CONFIG REWRITE   (or ACL SAVE when using aclfile)
```
With plain `CONFIG SET requirepass NEW` the default user's password is replaced, so the old
one stops working at once: a hard cutover.

## Sentinel
Sentinels authenticate to Redis with `sentinel auth-pass <master-name> <pw>`
(or `sentinel auth-user`), and Sentinels themselves can require a password
(`requirepass` in sentinel.conf) which clients must send when asking for the master address.

## Better: no shared default
Prefer named ACL users per application and `ACL SETUSER default off`, so there is
no single shared password (new connections then start unauthenticated and must `AUTH` or
`HELLO`). Keep requirepass only for legacy clients.

## Gotchas
- `CONFIG REWRITE` writes the password into redis.conf in plaintext; protect file permissions (0640, redis user).
- Replicas without `masterauth` after enabling auth cannot sync: `INFO replication` will not show the link as up.
- Health checks / exporters (redis_exporter) also need the new password.

## Verify
`redis-cli PING` without auth returns `NOAUTH Authentication required`; `INFO replication`
on replicas shows `master_link_status:up`; `ACL LIST` shows the default user's state as intended.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the ACL and security pages: `requirepass` sets the default user's password; the legacy password is used by all clients and Redis refuses queries from unauthenticated clients; a user can have several passwords (`>password` adds, `<password` removes); a default user flagged off makes new connections start unauthenticated; CONFIG REWRITE does not trigger ACL SAVE and handles only users stored in redis.conf; the password sits in clear text in redis.conf; Redis checks passwords very fast. Confirmed from the replication and Sentinel pages: `masterauth` on replicas, Sentinel `auth-user`/`auth-pass`, `requirepass` on Sentinels. `masteruser` is present in the 6.0 redis.conf. Removed unconfirmed: the -NOAUTH log claim and the new-connections-only wording.
Method: documentation only; no commands were run.
