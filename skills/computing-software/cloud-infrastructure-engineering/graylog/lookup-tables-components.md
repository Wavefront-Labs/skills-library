---
id: computing-software.cloud-infrastructure-engineering.graylog.lookup-tables-components
name: lookup-tables-components
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [lookup-tables, data-adapters, lookup-cache, enrichment, geoip]
level: practitioner
status: docs-checked
description: "Lookup tables combine a data adapter, a cache and a lookup table to enrich messages; caches protect slow sources."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/lookup_tables.html
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/data_adapters.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# lookup tables components

Four components:
- **Data adapters** perform the real lookup against an external source, for example a CSV file, a database or an HTTP request. Types are pluggable; the sidebar lets some adapters run a test lookup.
- **Caches** store lookup results to speed lookups and avoid overloading databases and APIs. A cache is a separate entity so one implementation can serve several adapters. Also pluggable.
- **Lookup tables** tie an adapter to a cache.
- **Lookup results** are the values returned.

Use lookup tables from pipeline rules to enrich messages. A slow adapter without a cache can drive high CPU in pipelines.

Documented adapter types include CSV file, DNS lookup, GeoIP, HTTP JSONPath, MongoDB, Active Directory user lookup and several threat intelligence feeds.

## Checked

2026-11-04. Confirmed against the Lookup Tables and Data Adapters pages. Nothing removed.

Method: documentation only; no commands were run.
