---
id: computing-software.email-administration.mail-server-administration.ip-warmup
name: ip-warmup
category: computing-software
field: email-administration
product: mail-server-administration
tags: [ip-warmup, sender-reputation, warm-up, new-ip]
level: practitioner
status: draft
description: "Warm up a new sending IP or domain gradually and watch provider feedback to avoid early throttling."
sources:
  - https://www.m3aawg.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ip warmup

**Goal:** build reputation before sending volume.
## Steps
1. Start with your most engaged recipients and small daily volumes; increase gradually (a schedule is your choice, M3AAWG gives general guidance).
2. Keep authentication perfect: PTR, SPF, DKIM, DMARC.
3. Watch for `421`/`4.7.0` throttling and slow down when seen.
4. Keep Postfix concurrency low for the major providers during warmup (`slow_destination_concurrency_limit`).
## Failure modes
- Sending a full list on day one triggers spam folder placement.
## Verify
- Postmaster dashboards show no spam-rate spikes; deferral rate stays low.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
