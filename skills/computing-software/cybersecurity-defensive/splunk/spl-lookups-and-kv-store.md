---
id: computing-software.cybersecurity-defensive.splunk.spl-lookups-and-kv-store
name: spl-lookups-and-kv-store
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, lookup-tables, kv-store, inputlookup, outputlookup, automatic-lookups, collections-conf, enrichment]
level: practitioner
status: draft
description: "Enrich SPL searches with CSV lookups and KV store collections: definitions, automatic lookups, updating with outputlookup, and when KV store beats CSV."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/ConfigureKVstorelookups", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Outputlookup"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lookup tables and KV store

**Goal:** add context (asset owner, VIP users, known-good hashes, threat lists) to events
and maintain that context from searches.

## CSV lookups
1. Upload `vip_users.csv` (Settings > Lookups > Lookup table files) into an app.
2. Create a definition `vip_users` (Settings > Lookups > Lookup definitions); set
   `case_sensitive_match = false` and match type (`WILDCARD(user)` or `CIDR(subnet)`) in
   transforms.conf if needed:
   ```
   [network_zones]
   filename = network_zones.csv
   match_type = CIDR(subnet)
   max_matches = 1
   ```
3. Use it:
   ```
   index=auth | lookup vip_users user OUTPUT title department
   | lookup network_zones subnet as src_ip OUTPUT zone
   ```
4. Automatic lookup (props.conf `LOOKUP-zone = network_zones subnet AS src_ip OUTPUT zone`)
   applies at search time to a sourcetype, so analysts get the field without typing it.

## Maintaining lookups from searches
```
| tstats count where index=proxy by dest_host | eval first_seen=now()
| inputlookup append=t seen_domains.csv
| stats min(first_seen) as first_seen by dest_host
| outputlookup seen_domains.csv
```
Schedule this as a baseline builder; detections then flag `first_seen` within the last day.

## KV store collections
Use KV store when the table is large (hundreds of thousands of rows), updated row by row,
or needs per-row keys:
```
# collections.conf
[asset_owner]
field.ip = string
field.owner = string
accelerated_fields.ip_idx = {"ip": 1}

# transforms.conf
[asset_owner_lookup]
external_type = kvstore
collection = asset_owner
fields_list = _key, ip, owner
```
Update a single row: `| makeresults | eval ip="10.1.2.3", owner="netops" | outputlookup append=t asset_owner_lookup`.
`outputlookup key_field=_key` updates in place instead of appending.

## Gotchas
- CSV lookups over about 10 MB get indexed on disk and replicated in every knowledge bundle;
  large ones slow every search in the cluster. Move them to KV store or exclude from the
  bundle with `replicate = false` (then use `local=true`).
- `outputlookup` without `append=t` overwrites the whole file.
- Lookup permissions follow app sharing; a detection running as nobody needs the lookup
  shared globally or in the same app.
- KV store runs on search heads only (replicated in SHC); check status with
  `splunk show kvstore-status`.

## Verify
`| inputlookup asset_owner_lookup | stats count` returns the expected row count, and a test
search shows the enrichment fields populated on real events.
