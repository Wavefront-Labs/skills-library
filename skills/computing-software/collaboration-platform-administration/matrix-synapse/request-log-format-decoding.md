---
id: computing-software.collaboration-platform-administration.matrix-synapse.request-log-format-decoding
name: request-log-format-decoding
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, logging, request-log, access-log, processed-request, db-time, 499, troubleshooting]
level: practitioner
status: docs-checked
description: "Decode the Synapse Processed request log line: request tags, requester field, total versus send time, CPU and DB timings, the status code ! suffix and 499, and grepping by tag."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/request_log.html
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse logs a line containing `Processed request:` when each HTTP request finishes, written to a logger named `synapse.access.(http|https).<tag>`, where the tag comes from the listener config and is normally the port. Fields, in order:

- Timestamp the request was logged (not received), logger name, code line number and log level.
- Request identifier such as `GET-37` or `PUT-1000`, shared by all related log lines. The prefix is the HTTP method (`GET-`, `PUT-`, `POST-`, `OPTIONS-`, `DELETE-`).
- Source IP, or `X-Forwarded-For` if enabled, then the server port.
- The federated server or local user making the request, blank if unauthenticated. A value like `@aaa:example.com|@bbb:example.com` means the first user is authenticated but controlled by the second.
- Total time to process the request, then time to send the response over the network (can be negative if the socket closed before the response was generated).
- Userland CPU and system CPU time (`ru=(...)`).
- `db=(...)`: total time waiting for a free DB connection from the pool, total time waiting for DB query responses, and the count of DB transactions. The first two can exceed the total time when slow queries run in parallel.
- Response size, status code, the request line and the user agent. A trailing events-fetched figure counts events loaded from the database, not those served from cache.

A status suffixed with `!`, such as `!200`, means the socket closed before the response was generated. A `499!` means Synapse also cancelled processing after the socket closed.

Several identical requests can arrive together; only the first reports CPU and DB figures, while the rest wait on it and show very small times.

To follow a single request, grep the log for its identifier, for example `grep 'GET-37' homeserver.log`, and wrap pasted output in triple backticks when sharing. For leaked file handles, compare `Received request` with `Processed request` lines and look for ones taking several seconds.

## Checked

2026-11-04. Confirmed against the Synapse Request log format page (field table and notes) and the Admin FAQ page (request tag grep, Received and Processed line comparison). Nothing removed.
Method: documentation only; no commands were run.
