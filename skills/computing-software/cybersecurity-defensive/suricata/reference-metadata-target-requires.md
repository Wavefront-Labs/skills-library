---
id: computing-software.cybersecurity-defensive.suricata.reference-metadata-target-requires
name: reference-metadata-target-requires
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [reference, metadata, target, requires]
level: practitioner
status: docs-checked
description: "Use reference, metadata, target and requires keywords: syntax, multiplicity, eve output and version or feature gating of rules."
sources: ["https://docs.suricata.io/en/latest/rules/meta.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# reference, metadata, target, requires

- `reference:type,reference;` for example `reference:cve,CVE-2014-1234;`. Repeatable. Types are defined in reference.config.
- `metadata: key value, key value;` free-form, but key-value pairs are recommended because Suricata can include them in eve alerts.
- `target:[src_ip|dest_ip]`: marks which side is the victim and adds source and target information to the alert event.
- `requires: feature geoip, version >= 7.0.0, keyword foobar`: rules failing the requirement are skipped, not errors.
  - Repeat `feature` per feature: `feature geoip, feature lua`.
  - AND by juxtaposition: `version >= 7.0.4 < 8`; OR with `|`: `version >= 7.0.4 < 8 | >= 8.0.3`.
  - Missing minor or patch defaults to 0.
  - `version` may appear only once, otherwise the rule is not loaded.
  - Available since 7.0.3 and 8.0.0.

## Checked

2026-11-04. Every keyword form above confirmed against the Suricata Meta Keywords page.

Method: documentation only; no commands were run.
