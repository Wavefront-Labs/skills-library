---
id: computing-software.email-administration.mail-server-administration.destination-concurrency-limits
name: destination-concurrency-limits
category: computing-software
field: email-administration
product: mail-server-administration
tags: [destination-concurrency-limits, default-destination-concurrency-limit, destination-rate-delay, transport-maps]
level: advanced
status: docs-checked
description: "Throttle outbound delivery per destination with default_destination_concurrency_limit, rate delay and per-transport settings."
sources:
  - https://www.postfix.org/postconf.5.html
  - https://www.postfix.org/transport.5.html
  - https://www.postfix.org/TUNING_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destination concurrency limits

**Goal:** be a polite sender so remote sites do not throttle you.
## Steps
1. `default_destination_concurrency_limit = 20` (check `postconf -d`).
2. For a strict domain: map it to a transport in `transport_maps`: `slow.example  slow:`, define `slow unix - - n - - smtp` in master.cf and set `slow_destination_rate_delay = 1s`, `slow_destination_concurrency_limit = 2` (the `transport_destination_rate_delay` and `transport_destination_concurrency_limit` families, where `transport` is the master.cf name; the rate delay is enforced by the queue manager and does not survive `postfix reload`).
3. `postmap` then `postfix reload`.
## Failure modes
- Deferrals from the remote site in the log are the signal to slow down (see TUNING_README).
## Verify
- Log shows fewer simultaneous connections to that domain; deferrals stop.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5), transport(5), TUNING_README.
Confirmed: `default_destination_concurrency_limit` default 20, per-transport `transport_destination_rate_delay` and concurrency overrides, `transport_maps`.
Corrected or removed: the specific 421/450 claim.
Method: documentation only; no commands were run.
