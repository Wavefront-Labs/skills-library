---
id: computing-software.systems-network-administration.coredns.coredns-trace-plugin
name: coredns-trace-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, trace, zipkin, datadog, opentracing]
level: practitioner
status: docs-checked
description: "Trace DNS requests through the plugin chain to Zipkin or Datadog with sampling, service name and Zipkin batching options."
sources:
  - https://coredns.io/plugins/trace/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see where time goes inside the chain.

Syntax:

```
trace [ENDPOINT-TYPE] [ENDPOINT] {
    every AMOUNT
    service NAME
    client_server
    datadog_analytics_rate RATE
    zipkin_max_backlog_size SIZE
    zipkin_max_batch_size SIZE
    zipkin_max_batch_interval DURATION
}
```

- ENDPOINT-TYPE is `zipkin` (default) or `datadog`. ENDPOINT defaults to `localhost:9411`. For Zipkin, an ENDPOINT not starting with http becomes `http://ENDPOINT/api/v2/spans`.
- With no options, every query is traced.
- `every AMOUNT` traces one query in every AMOUNT; default 1.
- `service NAME` is the reported service name; default `coredns`.
- `client_server` enables the ClientServerSameSpan OpenTracing feature.
- `datadog_analytics_rate` (0 to 1) is a Datadog-only option.
- Zipkin reporter limits: backlog default 1000, batch size default 100 traces, batch interval default 1 second. When the backlog threshold is reached, spans from the start of the batch are disposed.

Enable the debug plugin to get logs from trace. A local Zipkin can be started with `docker run -d -p 9411:9411 openzipkin/zipkin`.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/trace/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the unsourced operational-notes paragraph.

Method: documentation only; no commands were run.
