---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.bundle-etag-caching-and-long-polling
name: bundle-etag-caching-and-long-polling
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [etag, if-none-match, long-polling, bundle-polling, superseded-etag]
level: advanced
status: docs-checked
description: "Make OPA bundle downloads efficient with Etag and 304 responses, superseded_etag_ttl_seconds for replicated servers, and HTTP long polling timeouts."
sources:
  - https://www.openpolicyagent.org/docs/management-bundles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: low-latency bundle updates without hammering the bundle server.

Etag caching: the service should set an `Etag` header on bundle responses. OPA sends it back in `If-None-Match`, and the service replies `304 Not Modified` when unchanged.

Replicated servers: if replicas update at different times, a lagging replica can serve an older bundle that OPA would then activate. Set `bundles[_].polling.superseded_etag_ttl_seconds` and OPA sends, within that window, the Etags of bundles it replaced as well as the current one, as a comma-separated `If-None-Match` list. A server following RFC 9110 answers `304` if any entry matches, so the old bundle is not served.

Requirements and cost:
- The service must support multiple values in `If-None-Match`. One that compares against a single Etag never replies `304` and OPA downloads on every poll.
- A rollback to a bundle replaced less than `superseded_etag_ttl_seconds` ago is not served until the time has passed.

Short polling sends regular requests and gets `304` when nothing changed; low latency needs a high frequency, which loads the server. HTTP long polling defers the server response until an update exists or a timeout passes (then `304`):

```yaml
bundles:
  authz:
    service: acmecorp
    resource: somedir/bundle.tar.gz
    polling:
      long_polling_timeout_seconds: 10
```

A supporting server sets `Content-Type: application/vnd.openpolicyagent.bundles`. If it does not, OPA falls back to periodic polling.

Check: watch server logs; unchanged polls should log `304`, and a published bundle should reach OPA within the timeout.

## Checked

2026-11-04. Confirmed against the Bundles page sections Caching and HTTP Long Polling: Etag and If-None-Match with 304, polling.superseded_etag_ttl_seconds and the comma-separated list, the multiple-value warning, the rollback note, long_polling_timeout_seconds and the application/vnd.openpolicyagent.bundles content type with fallback to periodic polling. Nothing removed.

Method: documentation only; no commands were run.
