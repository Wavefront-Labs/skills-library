---
id: computing-software.cybersecurity-defensive.zeek.broker-framework
name: broker-framework
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, broker, cluster-topology, data-partitioning, hrw-partitioning]
level: advanced
status: docs-checked
description: "Broker, Zeek's legacy pub/sub layer: cluster topology rules, node role guidance, and HRW data partitioning across proxies via publish_hrw."
sources: ["https://docs.zeek.org/en/current/frameworks/broker.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# broker framework

Status: the page says the framework is deprecated as of Zeek 9.0, for removal during the Zeek 10 release cycle. Zeekctl clusters use the ZeroMQ backend by default since 8.1, and users are encouraged to switch.

Broker is a topic-based publish/subscribe layer built on CAF. Node types are in `Cluster::NodeType`: Manager, Logger, Worker, Proxy. There is a single Manager. Connectivity is static: every node connects to all loggers and the manager, and each worker connects to all proxies.

Role advice:

- Workers do the brunt of parsing and a first-pass analysis.
- Proxies hold partitioned data or take offloaded work; default scripts use them minimally, so start with one.
- The manager suits decisions needing a global view but is easy to overload.
- Loggers write logs; by default logs are distributed round-robin among loggers, giving failover.

Sharing state: the `&synchronized` attribute is no longer possible; the alternative is data partitioning with the pools API in `base/frameworks/cluster/pools.zeek`. For example, `Cluster::publish_hrw` uses Highest Random Weight hashing to spread keys across proxies; scale by adding a proxy. A node leaving the pool leaves a temporary gap in the data until workers rehash to a live proxy. `Cluster::PoolSpec` lets a script developer constrain pool size while users can still override it.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text. The earlier claim about distributed data stores was dropped because the page does not cover it.

Method: documentation only; no commands were run.
