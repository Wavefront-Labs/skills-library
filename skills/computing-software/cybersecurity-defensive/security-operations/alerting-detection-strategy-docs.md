---
id: computing-software.cybersecurity-defensive.security-operations.alerting-detection-strategy-docs
name: alerting-detection-strategy-docs
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, alerting-detection-strategy, ads-framework, detection-documentation, triage-guide, palantir-ads]
level: practitioner
status: draft
description: "Document detections with the Alerting and Detection Strategy (ADS) framework: goal, ATT&CK category, technical context, blind spots, false positives, validation and response."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://blog.palantir.com/alerting-and-detection-strategy-framework-52dc33722df2", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alerting and Detection Strategy documentation

**Goal:** every production detection has a document that lets an engineer review it and an
analyst triage it without reverse-engineering the query (Palantir ADS framework).

## ADS sections
1. **Goal:** one sentence of the behaviour detected ("Detect creation of a new service
   from a remote host via the Service Control Manager").
2. **Categorization:** ATT&CK tactic/technique (T1569.002 System Services: Service Execution).
3. **Strategy abstract:** how the detection works at a high level: data source, logic,
   thresholds, enrichment.
4. **Technical context:** what an analyst needs to understand the behaviour: how the OS
   feature works, normal uses, event IDs and fields involved (7045, 4697), examples of
   attacker tooling.
5. **Blind spots and assumptions:** what it will not catch and what must be true (Sysmon
   deployed on servers; attacker using WMI instead bypasses it; log source X is complete).
6. **False positives:** known benign causes and how they are filtered (software deployment
   tools creating services, with the allowlist location).
7. **Validation:** how to produce a true positive on demand (Atomic Red Team T1569.002 test
   number, or a command line), so anyone can test it.
8. **Priority:** severity and why (asset classes may raise it).
9. **Response:** triage steps: what to check, what makes it benign or malicious, containment
   steps and escalation path. Link the runbook.
10. **Additional resources:** references, blog posts, prior incidents.

## Workflow
- Write the ADS **before** the rule goes to production; the review checks the doc and the
  query together. Draft status can begin with goal, strategy and validation.
- Store alongside the rule in the detection repo (same slug) and link from the alert
  (Splunk `action.notable.param.drilldown` / next steps, Sentinel description, Elastic
  investigation guide).
- Update the ADS whenever tuning changes logic or blind spots.

## Gotchas
- Blind spots left blank: every detection has them; writing them guides future detections.
- Response sections that say "investigate" are useless; give concrete pivots and queries.
- ADS docs nobody can find; surface them in the alert itself.

## Verify
An analyst new to the detection triages a test alert using only the ADS, and a reviewer can
reproduce a true positive from the Validation section.
