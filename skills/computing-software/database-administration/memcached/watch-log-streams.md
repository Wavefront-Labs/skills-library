---
id: computing-software.database-administration.memcached.watch-log-streams
name: watch-log-streams
category: computing-software
field: database-administration
product: memcached
tags: [watch, watchers, fetchers, mutations, connevents]
level: advanced
status: docs-checked
description: "Stream live memcached internals with the watch command: fetchers, mutations, evictions, connevents, deletions and proxy logs."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`watch <arg> <arg> ...` turns the connection into a log watcher until it disconnects. Reply `OK` or `ERROR`.

Arguments:
- `fetchers`: every internal item fetch (a set also logs a get, as it checks first).
- `mutations`: stores and most store errors.
- `evictions`: items as they are evicted; shows whether evicted items were used and which keys.
- `connevents`: connections opening and closing, with remote address and close reason; TLS protocol errors when TLS is on.
- `deletions`: successful `delete` or `md`; misses are not logged.
- `proxyreqs`, `proxyevents`, `proxyuser`: proxy timing, internal errors and Lua log output.

Output lines are `key=value`, prefixed with `ts=` and `gid=`; logs may arrive out of order, so sort by gid. Values are URI encoded (`n%2Cfoo`).

Example: `printf 'watch evictions
' | nc localhost 11211`.

Slow watchers are skipped: see `log_watcher_skipped` and `log_watchers` in `stats`.

## Checked

Confirmed 2026-11-09: the watch argument list and each argument's description, `OK` or `ERROR` reply, key=value lines with ts and gid, out-of-order logs and URI-encoded values, and the stats `log_watcher_skipped` and `log_watchers` (protocol.txt Watchers and Statistics sections). Nothing removed.

Method: docs-checked 2026-11-09 against memcached doc/protocol.txt
