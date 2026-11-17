---
id: computing-software.database-administration.elasticsearch.geoip-and-user-agent-enrichment
name: geoip-and-user-agent-enrichment
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, geoip-processor, user-agent-processor, ingest-pipelines, enrichment, elasticsearch-ingest]
level: practitioner
status: docs-checked
description: "Enrich Elasticsearch documents with location from IPs (geoip processor, database downloads) and browser/device from user agents, with mapping and update gotchas."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/ingest-processor/geoip-processor.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/ingest-processor/ip-location-processor.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/ingest-processor/user-agent-processor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GeoIP and user_agent enrichment

## Pipeline
```json
PUT _ingest/pipeline/web-enrich
{ "processors": [
  { "geoip": { "field": "source.ip", "target_field": "source.geo", "ignore_missing": true } },
  { "geoip": { "field": "source.ip", "target_field": "source.as", "database_file": "GeoLite2-ASN.mmdb",
               "properties": ["asn", "organization_name"], "ignore_missing": true } },
  { "user_agent": { "field": "user_agent.original", "target_field": "user_agent", "ignore_missing": true,
                    "extract_device_type": true } }
] }
```

## Mapping
`source.geo.location` must be mapped as `geo_point` for maps and geo queries; ECS templates do this. A dynamic mapping creates an object with `lat`/`lon` floats instead, which breaks map visualisations; fix the template and reindex.

## GeoIP database updates
- Elasticsearch downloads GeoLite2 City/Country/ASN databases automatically from the Elastic GeoIP endpoint and checks for updates every three days by default. Without direct access, set `ingest.geoip.downloader.endpoint` to a reverse proxy, or set `ingest.geoip.downloader.enabled` to `false` and put the database files in the `ingest-geoip` directory of each node's config directory.
- If Elasticsearch cannot reach the endpoint for 30 days the databases become invalid: enrichment stops and documents get `tags: ["_geoip_expired_database"]`.
- Check: `GET _ingest/geoip/stats`.
- The newer `ip_location` processor uses the same downloaded databases (tags `_ip_location_expired_database` when expired); you can also have Elasticsearch download databases with your own MaxMind licence key through the IP location database configuration API.

## user_agent
- Default properties are `name`, `os`, `device`, `original` and `version`. A custom `regex_file` goes in the `config/user-agent` directory (named `config/ingest-user-agent` before 9.4, still a deprecated fallback). `extract_device_type` is a beta option, default false.
- Results are cached: setting `user_agent.cache_size` (9.4+; `ingest.user_agent.cache_size` before, now deprecated), default 1000.

## Privacy
IP addresses and the locations derived from them can be personal data depending on your jurisdiction and use; check your obligations, and consider dropping or truncating `source.ip` after enrichment and limiting precision with the `properties` option (for example country only).

## Verify
`_simulate` with a public IP returns `source.geo.country_iso_code`; mapping check `GET logs-web/_mapping/field/source.geo.location` shows `geo_point`.

## Checked

Checked 2026-10-25 against elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: automatic GeoLite2 download and three-day check interval; 30-day expiry and `_geoip_expired_database` tag; `ingest.geoip.downloader.endpoint` and `enabled`; `ingest-geoip` config directory; `database_file` and `properties` options; user_agent defaults, `regex_file` directory rename in 9.4, `user_agent.cache_size` default 1000 and the deprecated old name. Removed the unconfirmed 8.x gating claim and the GDPR legal assertion. `_ingest/geoip/stats` and the geo_point mapping advice (documented in the geoip mappings note) were not re-read.

Method: documentation only; no commands were run.
