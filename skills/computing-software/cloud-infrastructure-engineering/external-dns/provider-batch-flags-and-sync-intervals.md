---
id: computing-software.cloud-infrastructure-engineering.external-dns.provider-batch-flags-and-sync-intervals
name: provider-batch-flags-and-sync-intervals
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aws-batch-change-size, google-batch-change-size, min-event-sync-interval, events-flag, sync-interval]
level: practitioner
status: docs-checked
description: "Tune ExternalDNS API volume with batch size flags for AWS, Google, Cloudflare and OVH, zone cache duration, --interval, --events and --min-event-sync-interval."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/rate-limits.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch flags and sync intervals

**Provider flags (defaults as documented)**
- Google: `--google-batch-change-interval=1s`, `--google-batch-change-size=1000`.
- AWS: `--aws-batch-change-interval=1s`, `--aws-batch-change-size=1000`, `--aws-batch-change-size-bytes=32000`, `--aws-batch-change-size-values=1000`, `--aws-zones-cache-duration=0s` (zones list cache TTL, `0s` disables), `--[no-]aws-zone-match-parent`.
- Cloudflare: `--cloudflare-dns-records-per-page=100` (maximum 5,000).
- OVH: `--ovh-api-rate-limit=20` (operations per second).

**Global flags**
- `--interval=1m0s`: time between consecutive synchronisations.
- `--[no-]events`: also reconcile when supported sources change (default disabled).
- `--min-event-sync-interval=5s`: minimum gap between event-triggered syncs.
- `--txt-cache-interval=0s`: registry cache sync interval (disabled by default).
- `--registry=txt|noop|dynamodb|aws-sd`.

**Recommendation from the docs:** enable `--events` and keep `--min-event-sync-interval` low so new resources reach DNS quickly; that gap is the acceptable propagation time between creating a Kubernetes resource and the record registering.

**Gotcha:** each refresh reads the zone through provider API calls (periodically and, with `--events`, on changes), and caching reduces that pressure. A failed batch typically falls back to individual per-record calls for that cycle, so one bad record does not block the zone; individual calls grow linearly with changes while batches grow with batch count.

**Check:** confirm defaults for your release in `docs/flags.md`.

## Checked

2026-11-04. Read the rate-limits page (Related options flag list with defaults, recommendation on --events and --min-event-sync-interval) and the operational best practices page (Batch API). Confirmed every flag name and default for Google, AWS, Cloudflare, OVH and the global flags, the registry options, the recommendation and the batch fallback and linear-growth remarks. Reworded the unsupported interval-tuning gotcha to what the pages state and added the operational page to sources.

Method: documentation only; no commands were run.
