---
id: computing-software.cybersecurity-defensive.splunk.detection-metadata-schema
name: detection-metadata-schema
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [detection-metadata, detection-as-code, json-schema, attack-mapping, detection-engineering, detection-lifecycle]
level: practitioner
status: draft
description: "Define a detection metadata schema (YAML) with ownership, ATT&CK mapping, data sources, severity, status, tests and triage notes, enforced by JSON Schema in CI."
sources: ["https://github.com/splunk/security_content/blob/develop/spec/detections.spec.json", "https://github.com/SigmaHQ/sigma-specification", "https://www.elastic.co/guide/en/security/current/rules-api-create.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Detection metadata schema

Metadata turns a query into a maintainable detection: who owns it, why it exists, how to triage it,
and whether it is tested.

## Fields worth requiring
```yaml
id: 3f2c9b1e-...            # UUID, never reused
name: Suspicious LSASS Access
status: production          # experimental | production | deprecated
owner: detection-team
author: <name>
created: 2026-05-01
modified: 2026-10-01
description: Detects non-allowlisted processes opening LSASS with read access.
mitre_attack: [T1003.001]
data_sources: [Sysmon EventID 10]
platforms: [windows]
severity: high
risk_score: 73
confidence: medium
query_language: spl
search: detections/lsass_access.spl
false_positives: [AV scanners, backup agents]
triage: |
  Check SourceImage signer; check GrantedAccess 0x1010 vs 0x1fffff...
response_playbook: playbooks/credential-dumping.md
tests: [tests/lsass_access_mimikatz.log]
references: [https://attack.mitre.org/techniques/T1003/001/]
```

## Enforce
- JSON Schema (`schemas/detection.schema.json`) with required fields and enums; validate in CI
  (`check-jsonschema --schemafile schemas/detection.schema.json detections/*.yml`).
- Custom checks: technique IDs exist in current ATT&CK (STIX bundle), referenced test files exist,
  `modified` updated when `search` changes.
- Generate coverage: ATT&CK Navigator layer from `mitre_attack`, data source dependency report from
  `data_sources`.

## Gotchas
- Free-text data sources prevent coverage analysis; use a controlled vocabulary (ATT&CK data
  components or your onboarding names).
- Don't duplicate fields the platform stores (rule ID in SIEM); keep the repo as source of truth
  and push to SIEM.

## Verify
CI rejects a detection missing `owner` or with an invalid technique ID; the generated Navigator
layer matches the count of production detections.
