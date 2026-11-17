---
id: computing-software.cybersecurity-defensive.threat-intelligence.misp-feeds
name: misp-feeds
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [misp-feeds, misp, threat-intel-feeds, feed-overlap, threat-intelligence-platform, ioc-handling]
level: practitioner
status: docs-checked
description: "Configure MISP feeds: enabling default and commercial feeds, caching vs pulling into events, feed overlap analysis, filtering rules, and producing your own feeds."
sources: ["https://www.circl.lu/doc/misp/managing-feeds/", "https://www.misp-project.org/feeds/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MISP feeds

## Feed types
- **MISP feed format** (manifest.json + event JSON files), **freetext** (lists of IOCs), **CSV** with column mapping.
  Local feeds point at the `manifest.json`.

## Configure
Sync Actions > Feeds:
- Enabled, caching enabled (stores feed content in Redis for correlation without creating events), and the
  distribution set on events created from the feed.
- Pulling a feed into events: the Delta Merge option keeps only attributes from the most recent fetch and
  soft-deletes the old ones.
- Schedule via scheduled tasks or cron with the API (`/feeds/fetchFromAllFeeds`, `/feeds/cacheFeeds/all`).

## Caching vs importing
- Cache everything you want correlation against ("is this IP in any feed?") without bloating the DB.
- Import only feeds you will act on and export (IDS), with warninglists enforced.

## Overlap analysis
The Feed overlap analysis matrix (Feeds side menu, built from cached feed data) shows shared values between feeds: drop feeds that add
nothing unique, keep those with unique, timely hits.

## Producing feeds
Share selected events as a MISP-format feed (manifest.json plus event files), filtered by tags/TLP; see the
managing-feeds guide for local feeds.

## Gotchas
- Freetext feeds have no context; tag them with source and confidence on import.
- Large feeds fill the database; use Delta Merge so stale values are removed.
- Feed URLs change; monitor fetch failures.

## Verify
Feeds list shows recent fetch times without errors; overlap matrix reviewed quarterly; exported IDS
lists exclude warninglisted values.

## Checked
2026-10-28. Confirmed in the CIRCL managing-feeds guide and the automation guide: MISP, CSV and freetext feed formats, Redis caching without events, Sync Actions > Feeds, Enabled, Distribution, Delta Merge, the feed overlap analysis matrix, manifest.json for local feeds, `/feeds/fetchFromAllFeeds` and `/feeds/cacheFeeds/all`. Removed: named default and commercial feeds, pull-rule wording, Administration > Jobs, the misp-feed repo link (404), decay/expiry claim.
Method: documentation only; no commands were run.
