---
id: computing-software.cybersecurity-defensive.zeek.zeromq-cluster-backend
name: zeromq-cluster-backend
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, zeromq, cluster-backend, xpub-xsub, cluster-publish]
level: advanced
status: docs-checked
description: "Switch a static Zeek cluster to the ZeroMQ backend: @load line, XPUB/XSUB central broker, PUSH/PULL log pipeline, and Cluster::publish replacing Broker::publish."
sources: ["https://docs.zeek.org/en/current/advanced/devel/cluster/backend/zeromq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# zeromq cluster backend

Marked as added in version 7.1. For a static cluster layout add to `local.zeek`:

```
@load frameworks/cluster/backend/zeromq
```

Then `Broker::publish` is non-functional and warns; use `Cluster::publish`. The default configuration uses hard-coded endpoints and layout; more options are in the module `cluster/backend/zeromq/main.zeek`.

**Events**: a central XPUB/XSUB broker distributes events published via `Cluster::publish`. Each node connects to it twice (one XPUB, one XSUB socket), so every node sees all messages and needs no topology awareness. Subscriptions raise the `Cluster::Backend::ZeroMQ::subscription` event on other nodes, which is used to discover nodes via `Cluster::nodeid_topic`. By default the manager runs the broker in a separate thread, though a standalone long-running broker is possible. Serialisation is chosen by `Cluster::event_serializer`.

**Logging**: log writes go directly to loggers using ZeroMQ's pipeline pattern. Loggers (including the manager if `Cluster::manager_is_logger`) open PULL sockets; other nodes connect PUSH sockets to all of them. ZeroMQ balances load, so a node cannot choose the target logger. Messages carry batches; `Log::flush_interval` and `Log::write_buffer_size` control batch frequency and size, and `Cluster::log_serializer` the format.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
