---
id: computing-software.digital-forensics-incident-response.log-analysis.running-hunts-with-the-peak-framework
name: running-hunts-with-the-peak-framework
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [peak-framework, threat-hunting, hypothesis-driven-hunting, baseline-hunting, model-assisted-hunting, hunt-documentation, dfir]
level: practitioner
status: draft
description: "Plan, execute and close threat hunts with the PEAK framework (Prepare, Execute, Act with Knowledge): hypothesis, baseline and model-assisted hunt types."
sources: ["https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html", "https://www.splunk.com/en_us/form/the-peak-threat-hunting-framework.html", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running hunts with the PEAK framework

**Goal:** run threat hunts as a repeatable process with documented outcomes, not ad hoc
searching.

## PEAK structure
**Prepare -> Execute -> Act**, with **Knowledge** carried through every phase. Three hunt types:
- **Hypothesis-driven:** a testable statement from threat intel or ATT&CK
  ("An adversary is using scheduled tasks created remotely via atsvc to persist on servers").
- **Baseline (exploratory data analysis):** characterise normal for a data source, then
  investigate outliers (stacking, first-seen).
- **Model-Assisted Threat Hunts (M-ATH):** use ML/statistical models (clustering,
  classification, anomaly scoring) to surface candidates for human review.

## Prepare
- Pick the topic (intel report, recent incident, ATT&CK gap, crown-jewel asset).
- Research the technique: how it appears in your telemetry, known benign look-alikes.
- Write the hypothesis or baseline goal, scope (systems, time range), data sources required, and
  confirm data availability and retention. Use the ABLE checklist: **A**ctor, **B**ehaviour,
  **L**ocation, **E**vidence.

## Execute
- Gather and pre-process data; run queries; iterate (refine filters, pivot on findings).
- Analyse candidates, document each reviewed item and its disposition.
- If you find an active intrusion, **stop hunting and escalate** to incident response.

## Act
- Preserve the hunt: queries, data sources, timeline, findings, decisions.
- Turn results into durable value: new or tuned detections (Sigma/SIEM rules), logging
  improvements for gaps found, playbook updates, asset/owner data fixes.
- Communicate findings to stakeholders, including "no evidence found" with the limits of the data.

## Knowledge
Feed lessons back: what data was missing, which queries worked, new baselines, and the
hunt backlog. Track metrics: hunts completed, detections created, gaps closed, incidents found.

## Hunt record template
```
Hunt ID / title / type (hypothesis | baseline | M-ATH)
Hypothesis or goal; ATT&CK technique(s)
Scope: systems, period; data sources and retention verified
Queries (with links/versions)
Findings: items reviewed, dispositions, incidents opened
Outputs: detections, logging changes, follow-up hunts
```

## Self-check
The hunt has a written hypothesis/goal, documented queries and dispositions, and at least one
concrete output (detection, gap ticket, or documented negative result with data limits).
