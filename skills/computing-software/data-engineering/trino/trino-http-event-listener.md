---
id: computing-software.data-engineering.trino.trino-http-event-listener
name: trino-http-event-listener
category: computing-software
field: data-engineering
product: trino
tags: [event-listener, http-event-listener, query-events, ingest-uri, custom-headers]
level: practitioner
status: docs-checked
description: "Stream Trino query created and completed events as JSON to an HTTP service, with retry, backoff, excluded fields and custom headers."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/event-listeners-http.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino http event listener

The HTTP event listener POSTs query events, encoded as JSON, to an external service. It is a first step to understanding datalake usage: events carry CPU and memory metrics, which data (down to column level) was accessed, and query-processing metadata. Running the capture system outside Trino reduces performance impact and lets you change it without client-facing downtime.

Requirements: an HTTP/S service accepting POST with a JSON body, and `http-event-listener.connect-ingest-uri` pointing at it.

Create `etc/http-event-listener.properties`:

```properties
event-listener.name=http
http-event-listener.log-created=true
http-event-listener.connect-ingest-uri=<your ingest URI>
```

Then list it in `config.properties`: `event-listener.config-files=etc/http-event-listener.properties,...`.

Key properties and defaults:
- `log-created` and `log-completed` (both `false`) enable `QueryCreatedEvent` and `QueryCompletedEvent` logging.
- `excluded-fields`: comma-separated names to omit, such as `payload,user`; a name matches at any nesting level.
- `connect-http-method`: `POST` (default) or `PUT`.
- `connect-retry-count` (`0`): retries on responses of 500 or higher; `connect-retry-delay` (`1s`); `connect-backoff-base` (`2`, delay = retryDelay * base^attempt, set 1 or empty for constant delay); `connect-max-delay` (`1m`).
- `connect-http-headers`: `key:value` pairs separated by commas; escape commas or colons with a backslash. Headers are static and cannot carry event data.
- Any other `http-event-listener.*` property is passed to the HTTP client.

## Checked

2026-11-04. Read against the Trino docs page `admin/event-listeners-http.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
