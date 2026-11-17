---
id: computing-software.database-administration.couchdb.network-batching-and-connections
name: network-batching-and-connections
category: computing-software
field: database-administration
product: couchdb
tags: [performance, batching, nodelay, socket-options, connection-limit]
level: advanced
status: docs-checked
description: "Tune CouchDB network behaviour: batch requests, use concurrency, set socket_options nodelay, and raise the chttpd server_options max connections."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/performance.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each request/response has latency overhead, so batch where you can (lists of documents or keys in the request body, for example the bulk load and store APIs). Large batches cost client time encoding and decoding JSON, so benchmark with your own data; the sweet spot is likely between one and ten thousand documents. On fast I/O, add concurrency.

**Small-write latency.** The page says the MochiWeb HTTP library shipped from CouchDB 1.1.0 sets TCP `SO_NODELAY` to false by default, so small replies may be buffered. Disable that:

```ini
[httpd]
socket_options = [{nodelay, true}]
```

**Connection limit.** The default maximum is 65535. Change it with `server_options`, where `max` is the maximum connections:

```ini
[chttpd]
server_options = [{backlog, 128}, {acceptor_pool_size, 32}, {max, 262144}]
```

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/performance page (Network, Connection limit): batching advice and the one to ten thousand document range, concurrency, SO_NODELAY and the [httpd] socket_options fix, default maximum of 65535 connections, server_options example. Rephrased the NODELAY sentence to match the page's 1.1.0 attribution. Nothing else removed.

Method: documentation only; no commands were run.
