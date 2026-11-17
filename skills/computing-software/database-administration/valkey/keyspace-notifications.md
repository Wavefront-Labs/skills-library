---
id: computing-software.database-administration.valkey.keyspace-notifications
name: keyspace-notifications
category: computing-software
field: database-administration
product: valkey
tags: [keyspace-notifications, notify-keyspace-events, keyevent, expired-events, keyspace, pubsub]
level: advanced
status: docs-checked
description: "Valkey keyspace notifications: notify-keyspace-events flags (K E g l s h z t x e m n A), keyspace vs keyevent channels, event names and expiry timing caveats."
sources:
  - https://valkey.io/topics/notifications/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keyspace notifications publish events about dataset changes on Pub/Sub channels. They are fire and forget: a disconnected subscriber misses events. Disabled by default (some CPU cost); set `notify-keyspace-events` in config or via `CONFIG SET`; empty string disables.

A `DEL mykey` in db 0 emits two messages: `PUBLISH __keyspace@0__:mykey del` (channel is key, message is event name) and `PUBLISH __keyevent@0__:del mykey` (channel is event, message is key).

Flags: `K` keyspace channel, `E` keyevent channel (at least one required), `g` generic (DEL, EXPIRE, RENAME), `$` strings, `l` lists, `s` sets, `h` hashes, `z` sorted sets, `t` streams, `d` module types, `x` expired, `e` evicted, `m` key miss, `n` new key (not in `A`), `A` alias for `g$lshztxed`. `Kl` gives keyspace events for lists; `KEA` enables most.

Event examples: `RENAME` gives `rename_from` and `rename_to`; `SET` gives `set`, `SETEX` also `expire`; `LPUSH` one `lpush` even variadic; `RPOP` gives `rpop` plus `del` if the list empties; `HSET` gives `hset`; `HEXPIRE` gives `hexpire` (past time gives `hexpired`); `HPERSIST` gives `hpersist`; `XADD` gives `xadd`, maybe `xtrim`; expiry gives `expired`; eviction `evicted`. Events fire only if the key really changes.

Timing: `expired` fires when Valkey actually deletes the key (on access or by the incremental background scan), not when the TTL hits zero, so delay can be large; likewise `hexpired`.

Cluster: events are node-specific and not broadcast, so subscribe on every node.

Debug: `valkey-cli config set notify-keyspace-events KEA`, then `valkey-cli --csv psubscribe '__key*__:*'`.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/notifications/ (page text read in full): Fire-and-forget delivery, __keyspace@0__ and __keyevent@0__ publishes, disabled by default, empty string disables, flag table including A alias and n, K/E requirement, Kl and KEA, the per-command event names listed, only-on-real-change rule, expired/hexpired timing, node-specific cluster events, the valkey-cli debug recipe.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
