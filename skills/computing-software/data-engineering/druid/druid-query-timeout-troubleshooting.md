---
id: computing-software.data-engineering.druid.druid-query-timeout-troubleshooting
name: druid-query-timeout-troubleshooting
category: computing-software
field: data-engineering
product: druid
tags: [troubleshooting, jetty-timeout, channel-disconnected, broker-backpressure, idle-timeout]
level: advanced
status: docs-checked
description: "Diagnose queries failing with a Channel disconnected error."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calls from the Broker to data servers are synchronous, so Jetty on the data server can time out in two cases: the data server pushes no results before the maximum idle time, or it starts pushing and then pauses longer than the idle time, for example because of Broker backpressure.

On timeout the server drops the Broker connection and the query fails with an error like "Unknown exception ... Channel disconnected (through reference chain ...)", with `errorClass` `com.fasterxml.jackson.databind.JsonMappingException` and the data server `host`.

Channel disconnection has several causes, so first confirm it is a web server timeout: the `host` field in the error names the Historical, so search that Historical's logs for the failing query ID and look for an exception containing `Idle timeout expired`.

Mitigations:
- Raise `druid.server.http.maxIdleTime` in the Historical `runtime.properties`; this needs a cluster restart.
- If the data servers pushed nothing before the timeout, optimize them. Slowdowns can come from groupBy queries spilling too much data to disk, large `IN` filters, or an under-scaled cluster; use the query metrics to find the bottleneck.
- If Broker backpressure caused the pause, optimize the Broker and check the connection between the Broker and deep storage.

## Checked

2026-11-08. Read querying/troubleshooting.md in full. Added the verification step and the three mitigations including druid.server.http.maxIdleTime.

Method: documentation only; no commands were run.
