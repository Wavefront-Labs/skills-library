---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-parsers-stages-and-grok
name: crowdsec-parsers-stages-and-grok
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [parsers, stages, grok, onsuccess, s00-raw, s01-parse, s02-enrich, nodes]
level: advanced
status: docs-checked
description: "How CrowdSec parser files are structured: stages, filter, grok, statics, sub-nodes and onsuccess."
sources: ["https://docs.crowdsec.net/docs/log_processor/parsers/format", "https://docs.crowdsec.net/docs/log_processor/parsers/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Parsers turn a raw line into structured fields. They are processed in the order of their **stage** (alphabetical: `s00-raw`, `s01-parse`, `s02-enrich`) and then file order. Hub-style layout is `parsers/s01-parse/<author>/<name>.yaml`; the extension must be `.yaml`, and following that layout lets editors validate against the published YAML schema.

## Directives

- `name` (mandatory; a node without a name is skipped at runtime)
- `filter`: an expr expression evaluated on the event. If true or absent the node runs; false or non-boolean skips it. Example: `evt.Parsed.program == 'kernel'`.
- `grok`: a RE2 pattern with capture groups plus `apply_on` (field of `evt.Parsed` to match, such as `message`) or `expression` returning the string to match. Captured fields merge into `Parsed`.
- `statics`: assign values to `Meta`, `Parsed` and similar fields.
- `onsuccess: next_stage`: on success move the event to the next stage.
- `nodes`: sub-nodes for branching. If any sub-node succeeds the whole node succeeds. A parent captures common data, leaves apply different patterns, as the nginx parser does for access and error logs.
- `debug: true`: logs node-level processing (statics, grok results, filter evaluation).
- `format`: parser version; versions from 2.0 raise the minimum crowdsec version (conditional features need 2.0 for crowdsec 1.5.0).

## Developing

The docs suggest creating the functional test first with `cscli hubtest create myservice-logs --type syslog`, filling the sample log and the `parser.assert` file, then writing the parser. A static with `method: GeoIpCity` populates fields in the `Enriched` map.

## Checked

2026-11-03. Confirmed against the parsers format and 'Creating parsers' pages: stage order, directives (name, filter, grok with apply_on/expression, statics, onsuccess, nodes, debug, format 2.0 / crowdsec 1.5.0), the hubtest create command and the schema/directory-layout note. Removed: the GeoIpASN, IpToRange and geoip-enrich enricher details, which the fetched pages do not state.

Method: documentation only; no commands were run.
