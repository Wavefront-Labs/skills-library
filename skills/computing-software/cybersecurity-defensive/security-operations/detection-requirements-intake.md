---
id: computing-software.cybersecurity-defensive.security-operations.detection-requirements-intake
name: detection-requirements-intake
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-requirements, detection-engineering, backlog, threat-informed-defense, attack-coverage, intake]
level: practitioner
status: draft
description: "Run detection requirements intake: request template, threat and data feasibility checks, prioritisation against ATT&CK and risk, and turning requests into detection backlog items."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://center-for-threat-informed-defense.github.io/", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Detection requirements intake

## Sources of requests
Threat intel (new actor TTPs), incident lessons learned, red/purple team gaps, audit/compliance
requirements, new technology onboarding, analyst ideas, vendor advisories.

## Request template
```
Title / requester / date
Threat or behaviour (ATT&CK technique, procedure example, source report)
Why it matters here (assets, actors targeting us, incident reference)
Expected data source(s) and whether we have them
Desired response (alert to SOC, risk score, auto-response)
Urgency and deadline driver
Known benign activity that looks similar
```

## Feasibility check
1. Data: is the telemetry collected, parsed, retained, with required fields? If not, raise a
   data onboarding dependency.
2. Existing coverage: search repo/ATT&CK layer; maybe tuning an existing detection suffices.
3. Testability: can we produce a positive sample (atomic test, attack range)?
4. Noise estimate: quick backtest of a draft query over 30 days.

## Prioritise
Score = threat relevance (actors targeting the sector, prevalence) x impact x coverage gap x
feasibility. Keep it simple and visible; review weekly with SOC leads and CTI.

## Backlog item
Accepted requests become tickets with acceptance criteria: detection merged with metadata, test
dataset, triage notes, deployed to production, requester informed. Rejected requests are closed with
reason (no data, prevented by control, low relevance) and logged as known gaps where applicable.

## Gotchas
- Requests phrased as tools ("detect Mimikatz") should be reframed as behaviours (LSASS access).
- Without data feasibility upfront, backlogs fill with impossible items.

## Verify
Every backlog item traces to a request with rationale; cycle time from request to production is
tracked and reported.
