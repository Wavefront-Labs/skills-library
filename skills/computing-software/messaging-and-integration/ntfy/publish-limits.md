---
id: computing-software.messaging-and-integration.ntfy.publish-limits
name: publish-limits
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, limits, rate-limit, quota, attachments]
level: practitioner
status: docs-checked
description: "Know ntfy's default per-visitor limits for requests, email, subscriptions, attachments, bandwidth and message size, and ntfy.sh differences."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default limits

Self-hosted defaults (ntfy.sh values differ where noted).

| Limit | Value |
|---|---|
| Message length | 4,096 bytes; longer becomes an attachment |
| Requests | 60 per visitor at once, refill one per 5 seconds |
| Daily messages | governed by request limits (ntfy.sh 250/day) |
| E-mails | 16 at once, refill one per hour (ntfy.sh 5/day) |
| Subscriptions | 30 connections per visitor |
| Attachment size | 15 MB per file, 100 MB per visitor, 5 GB total |
| Attachment expiry | 3 hours |
| Title / tags | 1 KB / 512 bytes combined; exceeding returns HTTP 400 |
| Daily bandwidth | 500 MB per visitor per 24 h (ntfy.sh 200 MB) |
| Total topics | 15,000 |

Limits can be changed per user with tiers. Heavy abuse may get an IP temporarily banned.

## Gotchas

- Behind a proxy without `behind-proxy: true`, every visitor shares one IP and one set of limits.
- ntfy.sh attachment limits are lower (2 MB per file, 20 MB per visitor) than self-hosted defaults.
- Tune with the server keys in the rate-limit-config skill.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Limitations table, ntfy.sh values, tiers) and config page (behind-proxy counts all visitors as one, 429 on limit). Removed: the Verify burst test.
Method: documentation only; no commands were run.
