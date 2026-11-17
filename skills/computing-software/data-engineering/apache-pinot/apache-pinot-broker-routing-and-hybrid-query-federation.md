---
id: computing-software.data-engineering.apache-pinot.apache-pinot-broker-routing-and-hybrid-query-federation
name: apache-pinot-broker-routing-and-hybrid-query-federation
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, broker, routing-table, segment-pruning, hybrid-table, federation, startbroker, scatter-gather]
level: intro
status: docs-checked
description: "What a Pinot broker does with a query: scatter-gather, segment pruning, merge, and splitting hybrid-table queries on the time boundary."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/broker.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broker routing and hybrid query federation

Brokers take query requests from clients, scatter them to the applicable servers, gather the results and return them. The controller shares cluster metadata with the brokers, so they can plan execution using a minimal subset of servers that hold the source data and, when required, other servers to shuffle and consolidate results. More brokers means more concurrent queries and lower latency.

Brokers are Helix **spectators**: they learn the location of each segment of a table (and each replica) through Helix and route requests to the servers hosting those segments.

The broker ensures every row of the table is queried exactly once. It may **prune segments** as long as accuracy is not sacrificed.

Hybrid tables (OFFLINE and REALTIME sharing one name): the broker performs offline and real-time federation so the overlap is queried exactly once. It splits the query on the time boundary into one sub-query for the offline table and one for the real-time table, and merges the results before returning them. See the time-boundary skill and the Pinot time-boundary page for how the boundary is derived and exactly which side gets `<=` or `>`.

Start a broker with the launcher script:
```
bin/pinot-admin.sh StartBroker -zkAddress localhost:2181 -clusterName PinotCluster -brokerPort 7000
```
Docker: run the Pinot image with `StartBroker -zkAddress <zookeeper-host>:2181`.

## Checked

2026-11-08. Read the whole pinot-docs broker page. Confirmed the scatter-gather role, Helix spectator model, exactly-once guarantee, pruning, hybrid federation and the StartBroker command. Removed the claims the page does not make: routing table built from the external view with ONLINE or CONSUMING replicas, broker tenant tags, and the pruning-versus-hardware gotcha. The page's own example uses a different boundary comparison from the time-boundary page, so the skill no longer states one.

Method: documentation only; no commands were run.
