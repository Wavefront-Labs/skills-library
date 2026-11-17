---
id: computing-software.cybersecurity-defensive.suricata.datasets-keyword
name: datasets-keyword
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [datasets, datarep, dataset-types, blocklists]
level: advanced
status: docs-checked
description: "Match large lists with dataset and datarep: types string, md5, sha256, ipv4, ip, formats, load, state, save, memcap and hashsize."
sources: ["https://docs.suricata.io/en/latest/rules/datasets.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# dataset and datarep

`dataset:<cmd>,<name>,<options>;` with cmd `set`, `unset`, `isset`, `isnotset`. Works on any sticky buffer, and transforms apply first (for example `to_md5` on a DNS query).

- `type` is mandatory: `string` (base64 in files), `md5` and `sha256` (hex), `ipv4`, `ip` (IPv4 or IPv6).
- `load` (file at start), `state` (load and save), `save` (write on exit). `load` and `save` cannot combine with `state`.
- `memcap`, `hashsize` (keep near the entry count).
- `format`: `csv` (default), `json`, `ndjson`, with `context_key`, `value_key`, `array_key`, `remove_key`.
- `match subdomain`: with `isset`/`isnotset` on type string; best with `dotprefix`.

`datarep:<name>,<operator>,<value>`: matches when data is listed and its reputation satisfies the comparison; each file line is data plus a reputation field.

Datasets can also be defined in suricata.yaml with defaults for memcap and hashsize.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/datasets) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
