---
id: computing-software.cybersecurity-defensive.threat-intelligence.mitre-car-analytics
name: mitre-car-analytics
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [mitre-car, attack-mapping, detection-engineering, analytics, mitre-attack, sigma, siem-queries]
level: practitioner
status: docs-checked
description: "Use MITRE Cyber Analytics Repository (CAR) analytics: navigating analytics by ATT&CK technique, pseudocode to SIEM queries, data model mapping and unit tests."
sources: ["https://car.mitre.org/", "https://car.mitre.org/analytics/", "https://github.com/mitre-attack/car"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MITRE CAR analytics

CAR (Cyber Analytics Repository) is a MITRE-curated set of detection analytics, each mapped to
ATT&CK techniques and written against the CAR data model, with pseudocode and often Splunk, EQL,
Sigma or LogPoint implementations.

## Navigating
- Analytics list or the ATT&CK Navigator layer of CAR coverage; each analytic (e.g. `CAR-2013-05-004`
  Execution with AT, `CAR-2019-04-004` Credential Dumping via Mimikatz) shows hypothesis, ATT&CK
  mapping, data model references, pseudocode, implementations,
  unit tests (how to generate a true positive).

## Turning CAR into detections
1. Map the analytic's data model objects to your telemetry (CAR is moving to the OSSEM Common Data Model, so check
   which model each analytic uses).
2. Translate pseudocode to your query language; prefer provided Sigma when present.
3. Run the unit test to confirm the detection fires.
4. Tune for environment; add metadata referencing the CAR ID.

## Using CAR in coverage work
Compare your detection inventory against CAR analytics per technique; gaps where CAR has analytics are
quick wins. CAR's sensor mappings and data model show which data you need.

## Gotchas
- CAR is not actively expanded at the pace of ATT&CK; some analytics are old and noisy; validate before
  production.
- Pseudocode assumes fields available in CAR's model; your logs may lack them (e.g. parent command line).

## Verify
Each CAR-derived detection has a passing unit test and references the CAR ID in metadata.

## Checked
2026-10-28. Confirmed on car.mitre.org and the CAR README: analytics mapped to ATT&CK with pseudocode, a unit test per analytic, Splunk, EQL, Logpoint and Sigma implementations, the ATT&CK Navigator coverage layer, the OSSEM data model move, CAR-2013-05-004 (Execution with AT) and CAR-2019-04-004 (Credential Dumping via Mimikatz). Removed: CAR data model object names, event ID mappings, Atomic Red Team remark.
Method: documentation only; no commands were run.
