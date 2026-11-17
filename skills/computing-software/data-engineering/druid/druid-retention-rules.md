---
id: computing-software.data-engineering.druid.druid-retention-rules
name: druid-retention-rules
category: computing-software
field: data-engineering
product: druid
tags: [retention-rules, load-rules, drop-rules, broadcast-rules, coordinator]
level: practitioner
status: docs-checked
description: "Set Druid load, drop and broadcast retention rules by forever, period or interval via the console or Coordinator API."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/rule-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Retention rules say which data to keep and which to drop. Each rule is a JSON object, selecting data by forever (all), period (offset from now) or interval (fixed range). Rules persist in the metadata store until changed. A default rule set applies to all datasources, and datasources can have their own rules.

## Setting rules

- Console: Datasources, open the datasource, Actions, Edit retention rules, +New rule, choose type and properties, Next, add a description, Save.
- Coordinator API: POST an array to `/druid/coordinator/v1/rules/_default` (defaults) or `/druid/coordinator/v1/rules/{datasourceName}`; GET `/druid/coordinator/v1/rules` lists all. Every POST overwrites the datasource's existing rules, so send the whole array in the desired order.
- Order matters: the Coordinator walks used segments and matches each to the first rule that applies; a segment matches only one rule. The console has up/down arrows to reorder.

## Load rules

Assign segments to Historical tiers with replica counts. A single tier is auto-named `_default`; a newly defined tier stays empty until a load rule targets it. Common properties: `tieredReplicants` (tier to replica count; each 0 or a positive integer) and `useDefaultTierForNull` (default true). When `tieredReplicants` is omitted or null, the default is `{"_default_tier": 2}` if `useDefaultTierForNull` is true, and `{}` (no replicas) if false.
- `loadForever`: all segments; this is the default rule Druid applies to datasources.
- `loadByPeriod`: `period` (ISO 8601) and `includeFuture` (default true; matches segments overlapping the rule interval or starting after it starts, so future-dated segments load).
- `loadByInterval`: `interval` as an ISO 8601 range.
- To keep segments off Historicals but queryable from deep storage, set `tieredReplicants` empty and `useDefaultTierForNull` false for those intervals or periods.

## Drop rules

Dropped data stays in deep storage until a kill task or automatic cleanup deletes it. To retain only a time window with a load rule, you must also add a drop rule, otherwise the default `loadForever` keeps everything else.
- `dropForever`: drops all remaining data; usually the last rule.
- `dropByPeriod`: matches when the period contains the segment interval; always drops recent data; has `period` and `includeFuture` (default true).
- `dropBeforeByPeriod`: drops segments before the period; `dropBeforeByPeriod` plus `loadForever` equals `loadByPeriod` (includeFuture true) plus `dropForever`.
- `dropByInterval`: `interval`; typically the oldest data, still queryable from deep storage.

## Broadcast rules

Used by extensions to load segments onto all Brokers. The docs say to apply them in a test environment, not production, and `druid.segmentCache.locations` must be set on both Brokers and Historicals. Types: `broadcastForever`, `broadcastByPeriod` (`period`, `includeFuture` default true), `broadcastByInterval` (`interval`).

## Deleting and reloading

Rule-dropped segments are always marked `unused`; submit a kill task to delete them permanently. A single rule cannot reload dropped data: lengthen the retention (for example one month to two), then mark all the datasource's segments `used`; the Coordinator reruns rules, loads the missing segments, and drops older versions.

## Checked

2026-11-08. Read the cited rule-configuration page in full. Expanded the draft with every rule type and property, defaults, ordering semantics and reload steps.

Method: documentation only; no commands were run.
