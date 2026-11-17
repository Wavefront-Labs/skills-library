---
id: computing-software.database-administration.redis.acl-key-patterns-and-selectors
name: acl-key-patterns-and-selectors
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-security, redis-acl, acl-key-patterns, acl-selectors, channel-permissions, acl-dryrun]
level: practitioner
status: docs-checked
description: "Restrict Redis ACL users to key prefixes and pub/sub channels, use read/write key permissions (%R~ %W~) and selectors (7.0+), and test with ACL DRYRUN."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
  - https://redis.io/docs/latest/commands/acl-setuser/
  - https://redis.io/docs/latest/commands/acl-dryrun/
  - https://redis.io/docs/latest/commands/acl-log/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL key patterns, channel permissions and selectors

## Key patterns
```
ACL SETUSER orders_svc on >S3cret! ~orders:* ~{orders}:* +@read +@write -@dangerous
ACL SETUSER cache_ro   on >...     ~cache:*  +@read
```
- `~pattern` grants read **and** write on matching keys (glob syntax, like `KEYS`).
- 7.0+: `%R~pattern` read-only, `%W~pattern` write-only, `%RW~pattern` = `~pattern`.
  ```
  ACL SETUSER reporter on >... %R~orders:* %R~stats:* +@read
  ```
- `allkeys` is an alias for `~*`; `resetkeys` clears all key patterns.
- Key patterns only restrict commands that name keys as arguments. Commands that work on a whole
  database take no key arguments and are governed only by command and category rules. A user with
  `~tenant1:* +@all` can still run `FLUSHALL`, `FLUSHDB` and `SWAPDB`; remove them explicitly
  (`-flushall -flushdb -swapdb`) or subtract `-@dangerous`.
- Read permission covers returned or processed user data, not metadata: `STRLEN`, `TYPE` and
  `SISMEMBER` do not need it. `LPOP` needs read and write; `LPUSH` needs write only.

## Pub/Sub channels
```
ACL SETUSER notifier on >... resetchannels &notifications:* +publish +subscribe
```
`&pattern` is available from 6.2. Redis 6.2 gave new users `allchannels` by default, to stay
compatible with 6.0. From 7.0 the `acl-pubsub-default` default is `resetchannels`, so new users have
no channel access until granted `&pattern` (or `allchannels`). Upgrades from configs that relied on
the 6.2 default may break subscribers. `PSUBSCRIBE` needs a literal match with an allowed pattern,
not a glob match.

## Selectors (7.0+)
A user can have extra rule sets in parentheses, each with its own commands and keys. A command is
allowed if the root permissions **or any selector** match; selectors cannot be edited later, only
removed all at once with `clearselectors`:
```
ACL SETUSER app on >... +@read ~app:* (+set +get ~cache:*) (+xadd ~events:*)
```
Here the user can read `app:*`, run SET/GET on `cache:*`, and only XADD to `events:*`.

## Testing
```
ACL DRYRUN orders_svc SET orders:1 x          # "OK", or a bulk string saying why it would be refused (7.0+)
ACL DRYRUN orders_svc GET users:1
ACL GETUSER orders_svc
ACL LOG 10                                     # recent events; reason is command, key, channel or auth
```

## Gotchas
- `redis.acl_check_cmd` (7.0+) lets a script check whether the calling user may run a command.
- Persist ACLs with either `user` lines in redis.conf or an `aclfile`; the two cannot be mixed.
  With an `aclfile` use `ACL SAVE` and `ACL LOAD`; `CONFIG REWRITE` does not save ACLs.
- Prefix patterns depend on consistent key naming; document the convention.

## Verify
`ACL DRYRUN` returns OK for intended operations and an explanation for the others; after deployment
`ACL LOG` shows no unexpected `key` or `command` denials from the application.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): ACL page, ACL SETUSER,
ACL DRYRUN, ACL LOG, Lua API (`redis.acl_check_cmd`). Confirmed: `%R~`/`%W~`/`%RW~`, selectors and
`clearselectors` (7.0), `&pattern` (6.2), the `acl-pubsub-default` change in 7.0, DRYRUN since 7.0.0, ACL LOG
reasons, whole-keyspace commands not limited by key patterns, aclfile versus redis.conf exclusivity.
Removed unconfirmed claims: per-command script checks, transaction queue-time denial, per-node ACLs in cluster mode.
Method: documentation only; no commands were run.
