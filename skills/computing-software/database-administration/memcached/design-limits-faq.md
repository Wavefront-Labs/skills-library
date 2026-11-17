---
id: computing-software.database-administration.memcached.design-limits-faq
name: design-limits-faq
category: computing-software
field: database-administration
product: memcached
tags: [faq, sessions, replication, failover, not-a-database]
level: intro
status: docs-checked
description: "Design limits from the memcached FAQ: keys are not for listing, RAM-first, O(1) atomic ops, not for sessions or as a database, no replication."
sources:
  - https://docs.memcached.org/userguide/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

- Listing keys: the interface is deliberately limited; applications must not rely on reading all keys back. The LRU crawler can examine all keys for analysis.
- All commands are internally atomic (aside from bugs); concurrent sets: the last one in is the one that sticks.
- All operations should run in O(1) time and be atomic; complex operations need careful thought, and many can be emulated on top of basic functionality.
- RAM only for latency and speed; the extstore feature allows splitting items between RAM and disk (flash) storage.
- Sessions: not recommended. If a session disappears the user is often logged out, whereas losing part of a cache from a crash or a software upgrade should not cause noticeable pain.
- Not a database: it is an ephemeral data store, so if the server goes down (crash, reboot) the data is gone.
- Replication: it does not do it. Adding replication halves your effective cache size.
- Failover: you usually do not handle it; some clients have a failover option that tries the next server.
- Persistence between restarts: yes in some situations; see warm restart.
- Authentication: limited password based authentication in the basic protocol, or TLS with certificate verification.
- MySQL query cache: uses many global locks and caches per table, so it falls over once tables change with any frequency.
- Clients and servers do not all need to talk to each other.
- Memcached can make an application slower, for example a loop of single gets; use pipelined gets instead.

## Checked

2026-11-04. Confirmed against the FAQ page. Fixed: the description's "no key listing" (the FAQ describes the LRU crawler), persistence ("only clean restarts" was not stated), and the loop-of-gets remedy wording. Removed: the closing advice line.

Method: documentation only; no commands were run.
