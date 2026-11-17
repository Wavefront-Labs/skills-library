---
id: computing-software.data-engineering.druid.druid-request-logging
name: druid-request-logging
category: computing-software
field: data-engineering
product: druid
tags: [request-logging, query-logs, slf4j, emitter, filtered, composing]
level: practitioner
status: docs-checked
description: "Enable query request logs and choose a request logger type."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/request-logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Druid service that serves queries can log the requests it processes. The logs include query metrics such as execution time and memory usage, useful for finding bottlenecks and slow queries. Request logging is disabled by default.

Pick a logger type, then set its specific properties. Types:
- `noop`: disables logging; the default.
- `file`: writes logs to disk.
- `emitter`: sends requests to an external location configured through an emitter.
- `slf4j`: logs through the SLF4J Java logging API.
- `filtered`: filters by query type or execution time, then passes matching queries to a delegate request logger.
- `composing`: logs all requests to multiple request loggers.
- `switching`: logs native queries and SQL queries to separate request loggers.

Set the type in `druid.request.logging.type` and the type-specific properties (see the request logging configuration reference) in `common.runtime.properties`; restart Druid for changes to take effect. Results go to the Broker logs unless the type is `emitter`, which also requires metrics emission to be configured.

For emitter logging set `druid.request.logging.feed` and define the emitter type in `druid.emitter`. Emitters are `noop` (default), `logging` (Log4j 2), `http` (POSTs JSON to a user-defined endpoint), `parametrized` (like `http` but adjusts the recipient URL by feed), `composing` and `graphite`. Example, posting to a placeholder endpoint:

```
druid.request.logging.type=emitter
druid.request.logging.feed=myRequestLogFeed
druid.emitter=http
druid.emitter.http.recipientBaseUrl=http://example.com:8080/path
# Only if the endpoint needs authentication
druid.emitter.http.basicAuthentication=username:password
```

The emitted events include the feed name, service, host, the query or SQL text, `queryStats` such as `sqlQuery/time`, `sqlQuery/planningTimeMs` and `sqlQuery/bytes`, and the query context.

## Checked

2026-11-08. Read operations/request-logging.md in full. Corrected the switching logger description (native versus SQL), added the config property, restart, emitter list and an example.

Method: documentation only; no commands were run.
