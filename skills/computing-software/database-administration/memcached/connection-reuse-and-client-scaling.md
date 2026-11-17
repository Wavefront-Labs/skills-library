---
id: computing-software.database-administration.memcached.connection-reuse-and-client-scaling
name: connection-reuse-and-client-scaling
category: computing-software
field: database-administration
product: memcached
tags: [persistent-connections, client, connection-churn, time-wait, multiplexing]
level: advanced
status: docs-checked
description: "Scale clients: reuse persistent connections, avoid per-request server hash rebuilds, and tame connection churn and TIME_WAIT."
sources:
  - https://docs.memcached.org/serverguide/performance/
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Memcached uses an event-based architecture, so a high number of clients will not generally slow it down; users have hundreds of thousands of connected clients working fine. Hard limits:
- Each connected client uses some TCP memory, so you can only connect as many clients as you have spare RAM.
- There is only one thread to accept new client connections. If you cycle connections very quickly you can overwhelm it; use persistent connections or UDP in this case.
- High connection churn requires OS tuning: you will run out of local ports, TIME_WAIT buckets and similar, so research how to tune the TCP stack for your OS.

Client behaviours:
- Most clients calculate the server hash table once on startup and reuse it; calculating it on every request slows down as servers are added. Looking up a server to issue a request is simply a hash lookup.
- Establishing too many TCP sockets from the client wastes RAM.
- Disabling persistent connections means the client will likely connect to all servers on every request; the 3-way handshake adds latency and packets to each request.
- A well designed binary protocol client (the page uses spymemcached) can take many application threads and use a single TCP connection back to memcached, so with 50 threads or processes per application node this can vastly reduce overhead.

protocol.txt also encourages clients to cache their connections rather than reopen them each time; memcached is designed to work efficiently with a very large number of open connections.

## Checked

2026-11-04. Confirmed against the Performance and Efficiency page (max clients, nodes in a cluster, binary protocol client) and protocol.txt (intro paragraph on caching connections). Removed: the closing "Watch total_connections vs curr_connections" line, which neither page states.

Method: documentation only; no commands were run.
