---
id: computing-software.cybersecurity-defensive.threat-intelligence.stix-patterning
name: stix-patterning
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [threat-intel-platform, stix-patterning, stix-2-1, indicator-objects, pattern-validator, cyber-observables]
level: practitioner
status: docs-checked
description: "Write and read STIX 2.1 indicator patterns: object paths, comparison and observation operators, qualifiers like WITHIN and REPEATS, validation, and translation to SIEM queries."
sources: ["https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_e8slinrhxcc9", "https://github.com/oasis-open/cti-pattern-validator", "https://github.com/opencybersecurityalliance/stix-shifter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STIX patterning

STIX 2.1 Indicator objects carry detection logic in `pattern` (with `pattern_type: stix`).

## Basic patterns
```
[ipv4-addr:value = '203.0.113.50']
[domain-name:value = 'evil-update.example']
[file:hashes.'SHA-256' = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08']
[url:value = 'https://evil.example/login.php']
[email-message:from_ref.value = 'billing@evil.example']
```
Object path = `<object-type>:<property>`; nested refs (`from_ref.value`), hashes with quoted keys, lists
(`extensions.'windows-pebinary-ext'.sections[*].entropy > 7.5`).

## Comparison expressions (inside one observation, in brackets)
- Operators: `=`, `!=`, `>`, `<`, `IN ('a','b')`, `LIKE 'evil%'`, `MATCHES '^regex$'`, `ISSUBSET`/`ISSUPERSET`
  (CIDR for IPs: `[ipv4-addr:value ISSUBSET '198.51.100.0/24']`).
- `AND` within brackets = same observed object/event; `OR` alternatives.
```
[file:name = 'invoice.exe' AND file:size < 300000]
```

## Observation expressions (across observations)
- `[A] AND [B]`: both observed (any order); `[A] OR [B]`; `[A] FOLLOWEDBY [B]`: B after A.
- Qualifiers: `WITHIN 300 SECONDS`, `REPEATS 5 TIMES`, `START t'2026-10-01T00:00:00Z' STOP t'...'`.
```
([network-traffic:dst_ref.value = '203.0.113.50'] REPEATS 10 TIMES WITHIN 600 SECONDS)
```

## Full indicator object
```json
{"type":"indicator","spec_version":"2.1","id":"indicator--<uuid4>",
 "created":"2026-10-18T09:00:00Z","modified":"2026-10-18T09:00:00Z",
 "name":"C2 server","indicator_types":["malicious-activity"],
 "pattern":"[ipv4-addr:value = '203.0.113.50']","pattern_type":"stix",
 "valid_from":"2026-10-18T09:00:00Z","valid_until":"2026-12-18T09:00:00Z",
 "confidence":80,"object_marking_refs":["marking-definition--<TLP:AMBER id>"]}
```
Always set `valid_until` so consumers can expire it.

## Validate and translate
- `pip install stix2-patterns`; `validate-patterns` CLI checks syntax.
- STIX-shifter translates patterns into SIEM/EDR queries (see its README for supported data sources).
- Other pattern types (`sigma`, `yara`, `snort`, `suricata`) can be carried in indicators with `pattern_type`.

## Gotchas
- Single quotes and backslashes in values must be escaped (`\'`, `\\`).
- Many consumers only support simple single-observation equality patterns; complex observation expressions
  may be ignored silently. Keep patterns simple for broad sharing.

## Verify
Patterns pass `validate-patterns`, round-trip through your TIP export and import unchanged, and a translated
query for a test indicator returns the seeded event in the SIEM.

## Checked
2026-10-28. Confirmed in the STIX 2.1 specification: the comparison operators (`MATCHES`, `LIKE`, `ISSUBSET`, `ISSUPERSET`), `FOLLOWEDBY`, `WITHIN`, `REPEATS`, `START`/`STOP`, indicator properties (`indicator_types`, `pattern_type`, `valid_until`), `windows-pebinary-ext`, and the pattern types `pcre`, `sigma`, `snort`, `suricata`, `yara`. Confirmed in the cti-pattern-validator README: `pip install stix2-patterns` and `validate-patterns`. Removed: stix2 library and stix-shifter connector claims.
Method: documentation only; no commands were run.
