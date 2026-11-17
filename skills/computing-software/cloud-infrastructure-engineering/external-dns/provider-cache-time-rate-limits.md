---
id: computing-software.cloud-infrastructure-engineering.external-dns.provider-cache-time-rate-limits
name: provider-cache-time-rate-limits
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, provider-cache-time, rate-limits, cache-trade-off, provider-cache-metrics]
level: practitioner
status: docs-checked
description: "Avoid DNS provider API throttling with --provider-cache-time: why full-zone refreshes hit limits, the deletion-recovery trade-off, and the cache metrics to watch."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/rate-limits.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider cache and rate limits

ExternalDNS refreshes all records of a zone through API calls, periodically and, with `--events`, on object changes. Large zones hit provider limits: the docs report that a Route 53 zone with 200k records needs around 70 API calls per refresh.

**Fix:** an optional in-memory cache, invalidated whenever records change in the cluster (new or deleted domains, changed targets).

```sh
--provider-cache-time=15m   # enable
--provider-cache-time=0m    # disable
```

**Trade-off:** records are cached in memory, so if someone deletes or edits a record at the provider, ExternalDNS does not notice until the cache expires. Higher values cut API use but slow recovery. Choose a value that matches how long you can tolerate a deleted record staying missing.

Restarting the controller (for example a rolling update) invalidates the cache at once.

**Monitor**
- `external_dns_provider_cache_records_calls`: label `from_cache=true` means served from memory, `from_cache=false` means the provider was called.
- `external_dns_provider_cache_apply_changes_calls`: every ApplyChanges invalidates the cache.

This option works for all providers and combines with `--txt-cache-interval` and provider-specific batch flags (the page lists per-provider batch flags). Registries other than `txt`, such as `dynamodb`, keep the registry outside the hosted zone and also help.

## Checked

2026-11-04. Confirmed against the ExternalDNS DNS provider API rate limits page: the 200k-record Route 53 figure, cache behaviour and trade-off, enable and disable values, metrics and related options. Nothing removed.
Method: documentation only; no commands were run.
