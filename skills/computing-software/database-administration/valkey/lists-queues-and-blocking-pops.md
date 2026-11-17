---
id: computing-software.database-administration.valkey.lists-queues-and-blocking-pops
name: lists-queues-and-blocking-pops
category: computing-software
field: database-administration
product: valkey
tags: [lists, lpush, rpush, lpop, lrange, ltrim, blpop, brpop, lmove, queues]
level: intro
status: docs-checked
description: "Valkey lists: LPUSH, RPUSH, LPOP, LRANGE, LTRIM capped lists, BLPOP/BRPOP/BLMOVE blocking queues, key auto-creation rules and O(n) middle access."
sources:
  - https://valkey.io/topics/lists/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lists are linked lists of strings, up to 2^32 - 1 elements. Push or pop at head or tail is O(1) regardless of length, but access by index (`LINDEX`, `LINSERT`, `LSET`) is O(n). Use sorted sets when middle access matters; consider Streams for event series.

Commands: `LPUSH`/`RPUSH` (variadic) add at head/tail; `LPOP`/`RPOP` remove (nil when empty); `LLEN`; `LRANGE key 0 9` with negative indexes counting from the end (-1 is last); `LMOVE` atomically pops from one list and pushes to another, for safer or rotating queues. Queue (page example): `LPUSH` then `RPOP`. Stack: `LPUSH` then `LPOP`.

Capped list: `LTRIM key start stop` keeps only that range. A push followed by a trim adds an element and discards the excess; the page example `LTRIM bikes:repairs 0 2` keeps the first three, and after `RPUSH`, `LTRIM key -3 -1` keeps the newest 3. Small `LRANGE` near either end is constant time.

Blocking: instead of polling `RPOP`, workers call `BRPOP key [key ...] timeout` or `BLPOP`. A timeout of 0 waits forever; on timeout the reply is nil. The reply is a two-element array (key name, value) because several lists can be watched. Blocked clients are served in the order they blocked. `BLMOVE` is the blocking `LMOVE`. Background-job libraries such as resque and sidekiq use lists this way.

Key lifecycle (all aggregate types): pushing to a missing key creates it; popping the last element deletes the key (Streams excepted); read or remove commands on a missing key behave as on an empty list, e.g. `LLEN` returns 0. A key of another type gives `WRONGTYPE`.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/lists/ (page text read in full): Linked lists, 2^32 - 1 elements, O(1) head/tail and O(n) LINDEX/LINSERT/LSET, LPUSH/RPUSH/LPOP/RPOP/LLEN/LMOVE/LTRIM, LRANGE negative indexes, LTRIM -3 -1, BRPOP timeout 0 and nil, two-element reply, FIFO service of blocked clients, BLMOVE, resque and sidekiq, the three key lifecycle rules, WRONGTYPE, Streams alternative.

Removed or changed: The invented `LTRIM key 0 99` newest-100 example and the RPUSH-then-LPOP queue recipe (the page queue example is LPUSH then RPOP).

Method: documentation only; no commands were run.
