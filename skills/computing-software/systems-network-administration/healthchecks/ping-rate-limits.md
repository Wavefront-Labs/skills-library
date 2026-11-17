---
id: computing-software.systems-network-administration.healthchecks.ping-rate-limits
name: ping-rate-limits
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, rate-limit, ping-frequency, ip-block]
level: practitioner
status: docs-checked
description: "Avoid Healthchecks ping rate limiting: the more-than-5-pings-per-minute threshold per check, what happens when exceeded, and the separate API request limit."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/http_api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pinging API: clients should not ping a check more often than necessary. Pinging more than 5 times per minute may cause some requests to be rate limited and not recorded. In extreme cases the client's IP address may be blocked.

Management API (separate): avoid more than 100 API requests per minute. Exceeding it eventually returns HTTP 429 errors.

Self-hosted note: login rate limiting depends on the real client IP, so the reverse proxy must set `X-Forwarded-For`; otherwise clients can spoof IPs and bypass IP-based limits. The `prunetokenbucket` management command removes rate-limit records (`api_tokenbucket`) older than one day.

## Checked

2026-11-04: confirmed against the Pinging API page (more than 5 pings per minute, IP blocking in extreme cases), the Management API page (100 requests per minute, 429) and the project README (X-Forwarded-For, prunetokenbucket, records older than one day). Removed generic practical-guidance bullets the pages do not state.
Method: documentation only; no commands were run.
