---
id: computing-software.database-administration.couchdb.replicator-connect-to-and-sockets
name: replicator-connect-to-and-sockets
category: computing-software
field: database-administration
product: couchdb
tags: [replication, connect-to, socket-options, proxy, port-rewriting]
level: sme
status: docs-checked
description: "Route CouchDB replicator requests with connect_to host:port rewrites, and set replicator socket_options within the valid_socket_options allowlist."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**connect_to.** Comma-delimited `host:port:target_host:target_port` mappings for replicator requests, similar to curl's `--connect-to`. Useful behind a transparent proxy or when ports must be rewritten.

- `host`: exact hostname (`foo.bar.com`) or a leading wildcard such as `*.example.test` (wildcards only at the start).
- `port`: port in the source URL (for example 443 for HTTPS).
- `target_host`: IPv4 address, hostname, or a bracketed IPv6 address (brackets avoid ambiguity with `:`).
- `target_port`: port to connect to.

```ini
[replicator]
connect_to = foo.bar.com:443:127.0.0.1:9443
```

**Sockets.** `socket_options` takes Erlang `inet` options that may boost performance: `nodelay`, `sndbuf`, `recbuf`, `priority`:

```ini
socket_options = [{keepalive, true}, {nodelay, false}]
```

`valid_socket_options` (3.3) is an allowlist; others are ignored (`buffer,keepalive,nodelay,priority,recbuf,sndbuf`). Many are low level and can cause unpredictable behaviour.

## Checked

2026-11-04. Confirmed against the CouchDB config/replicator page ([replicator] connect_to, socket_options, valid_socket_options): the four mapping parts, wildcard rule, IPv6 brackets, the example, listed socket options, the 3.3 allowlist and its default value. Nothing removed.

Method: documentation only; no commands were run.
