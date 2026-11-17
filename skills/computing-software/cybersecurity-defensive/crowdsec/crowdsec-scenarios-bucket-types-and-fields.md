---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-scenarios-bucket-types-and-fields
name: crowdsec-scenarios-bucket-types-and-fields
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [scenarios, leaky-bucket, trigger, counter, conditional, bayesian, groupby, capacity, leakspeed, blackhole]
level: advanced
status: docs-checked
description: "Write CrowdSec scenarios: the five bucket types and the main directives (filter, groupby, distinct, capacity, leakspeed, blackhole)."
sources: ["https://docs.crowdsec.net/docs/log_processor/scenarios/format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A scenario defines a bucket that events are poured into; when it overflows an alert is raised.

## Types

`type: leaky|trigger|counter|conditional|bayesian`

- **leaky**: leaks one item every `leakspeed` and holds up to `capacity` before overflowing.
- **trigger**: overflows immediately on a matching event.
- **counter**: overflows after `duration` since the first event.
- **conditional**: overflows when a condition is true (for example a successful login after five failures).
- **bayesian**: updates a prior `P(Evil)` per condition and overflows when the posterior exceeds `bayesian_threshold`; `guillotine` stops re-evaluating a costly condition once it was true.

## Directives

- `name` (unique, `author/name`) and `description` are mandatory; `references` optional.
- `filter`: expr deciding whether an event is poured into the bucket.
- `groupby`: expression returning a string that partitions buckets, for example `evt.Meta.source_ip` or a combination of IP and target user.
- `distinct`: pour an event only if its string is not already in the bucket, for example `evt.Meta.http_path` for unique 404s.
- `capacity` (leaky), `leakspeed` (leaky and conditional), `duration` (counter only).
- `blackhole: 10m`: silence the bucket for that long after an overflow.
- `cache_size`: how many events the bucket keeps in memory (defaults to capacity).
- `cancel_on`: expression run per event that cancels the bucket.
- `overflow_filter`: expression run at overflow; can drop it.
- `reprocess: true` feeds the overflow back into the pipeline (default false).
- `scope`: change what the decision targets, for instance `type: Range` with an expression.
- `labels`: metadata such as `service`, `confidence`, `spoofable`, `remediation`.
- `data`: files downloaded for use by expressions.

Example filter: `evt.Meta.service == 'http' && evt.Meta.http_status in ['404', '403', '400']` with `groupby: evt.Meta.source_ip` and `distinct: evt.Meta.http_path`.

## Checked
2026-11-08. Confirmed against the whole Scenarios file-format page: the five types, every directive listed, the 404-scanner example, cache_size default, blackhole, scope, data. Removed the Scenarios create page from sources (not used).
Method: documentation only; no commands were run.
