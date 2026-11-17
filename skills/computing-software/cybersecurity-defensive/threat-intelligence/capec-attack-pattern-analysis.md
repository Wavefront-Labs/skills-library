---
id: computing-software.cybersecurity-defensive.threat-intelligence.capec-attack-pattern-analysis
name: capec-attack-pattern-analysis
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [capec, attack-mapping, attack-patterns, cwe, mitre-attack, threat-modelling, application-security]
level: practitioner
status: docs-checked
description: "Use MITRE CAPEC attack patterns in defensive work: navigating CAPEC, linking CWE weaknesses to attack patterns and ATT&CK, and using them in threat modelling and testing."
sources: ["https://capec.mitre.org/", "https://capec.mitre.org/data/definitions/1000.html", "https://cwe.mitre.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CAPEC

CAPEC (Common Attack Pattern Enumeration and Classification) catalogues how attackers exploit
weaknesses, mostly at the application/software level. ATT&CK describes adversary behaviour in
enterprise intrusions; CAPEC describes attack patterns against software; CWE describes weaknesses.

## Structure
- Views include Mechanisms of Attack (CAPEC-1000).
- Entry fields: description, likelihood, typical severity, prerequisites, skills required,
  execution flow (explore/experiment/exploit), consequences, mitigations, related CWEs, related ATT&CK
  techniques (taxonomy mappings).
- Abstraction: meta, standard, detailed patterns.

## Defensive uses
- **Threat modelling**: for each component/data flow, list relevant CAPEC patterns (via STRIDE
  category or domain), check prerequisites against your design, record mitigations.
- **CWE -> CAPEC**: a SAST finding (a CWE) maps to related CAPEC attack patterns, which inform test cases
  and severity justification.
- **Security testing**: execution flow sections give test steps for pentest/DAST scenarios.
- **ATT&CK bridging**: CAPEC entries reference ATT&CK techniques so
  application-level threats link into enterprise detection coverage.

## Data
Use the machine-readable downloads offered on capec.mitre.org.
Parse to build lookup tables CWE <-> CAPEC <-> ATT&CK.

## Gotchas
- CAPEC is broad and some entries are thin; use it as a checklist generator, not an authority on
  likelihood.
- Mappings are incomplete; absence of a mapping doesn't mean no relationship.

## Verify
Threat model for an application cites CAPEC IDs per identified threat with mitigations; test plan
includes cases derived from the execution flows.

## Checked
2026-10-28. Confirmed on capec.mitre.org: the Mechanisms of Attack view is CAPEC-1000. Removed: CAPEC-3000 domain list, example CAPEC IDs and the CWE-89 mapping, the T1566 mapping, the mitre/cti `capec/2.1/` path and the XML/CSV format claim (none confirmed on the fetched pages).
Method: documentation only; no commands were run.
