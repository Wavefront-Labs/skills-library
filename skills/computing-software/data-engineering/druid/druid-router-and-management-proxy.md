---
id: computing-software.data-engineering.druid.druid-router-and-management-proxy
name: druid-router-and-management-proxy
category: computing-software
field: data-engineering
product: druid
tags: [router, management-proxy, web-console, load-balancer, query-routing]
level: practitioner
status: docs-checked
description: "Use the Router for query routing across Broker groups and as a management proxy for Coordinator and Overlord."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/router.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Router distributes queries between different Brokers. By default the Broker routes by preconfigured data retention rules; for example, if one month of recent data is in a hot cluster, queries within that month can go to a dedicated set of Brokers and older queries to another set. For query routing purposes you should only need a Router if your cluster is well into the terabyte range.

The Router also hosts the web console, the UI for loading data, managing datasources and tasks, and viewing server status and segment information.

Management proxy: the Router can forward requests to the active Coordinator or Overlord. This helps with high availability where the HTTP redirect from an inactive to the active Coordinator or Overlord does not work, such as behind a load balancer or when the redirect hostname resolves only internally. Enable it in the Router runtime.properties:

```
druid.router.managementProxy.enabled=true
```

The proxy supports implicit and explicit routes. Implicit routes follow API path conventions: `/druid/coordinator/*` goes to the Coordinator and `/druid/indexer/*` to the Overlord, with the path unchanged, so only the target host changes. Explicit routes use a prefix, `/proxy/coordinator/*` or `/proxy/overlord/*`, which is stripped before forwarding; use them for calls with an ambiguous destination such as `/status`, which every service has.

Router strategies choose the Broker and are evaluated in order, with the Broker chosen as soon as one matches: `timeBoundary` (sends all timeBoundary queries to the highest priority Broker), `priority` (queries with priority below `minPriority` go to the lowest priority Broker and above `maxPriority` to the highest; defaults 0 and 1), `manual` (reads `brokerService` from the query context, falling back to `defaultManualBrokerService`, valid only if present in `druid.router.tierToBrokerMap`; works for native and SQL queries) and `javascript` (an arbitrary function, disabled unless JavaScript is enabled).

SQL queries use strategies only when `druid.router.sql.enable` is `true` (default `false`); otherwise, or if no strategy resolves one, the Router uses `defaultBrokerServiceName`. Native queries always use strategies, then load rules, then the default.

Avatica JDBC requests are routed by connection ID, because Brokers do not share connection state. `druid.router.avatica.balancer.type` is `rendezvousHash` (the default) or `consistentHash` (non-default, experimental). With several Routers, give all the same balancer configuration.

Start the service with `org.apache.druid.cli.Main server router`.

## Checked

2026-11-08. Read design/router.md in full; skipped the sample production JVM and runtime configuration. Added management proxy routes, strategies, SQL routing and Avatica balancers.

Method: documentation only; no commands were run.
