---
id: computing-software.digital-forensics-incident-response.log-analysis.documenting-detections-with-the-ads-framework
name: documenting-detections-with-the-ads-framework
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [ads-framework, alerting-detection-strategy, detection-engineering, detection-documentation, dfir]
level: practitioner
status: draft
description: "Document detections with Palantir's Alerting and Detection Strategy (ADS) framework: goal, categorisation, strategy abstract, technical context, blind spots, validation and response."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://blog.palantir.com/alerting-and-detection-strategy-framework-52dc33722df2", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Documenting detections with the ADS framework

Palantir's ADS framework (2017) requires every alert to ship with a structured document before it goes live. It forces the engineer to think through false positives, blind spots and response, and it gives the 03:00 analyst what they need.

## The sections
| Section | Content |
|---|---|
| **Goal** | One or two sentences: what behaviour this detects and why it matters |
| **Categorization** | ATT&CK tactic and technique IDs (e.g. Credential Access / T1003.001) |
| **Strategy Abstract** | High-level how: data source, logic, thresholds, enrichment |
| **Technical Context** | Background the analyst needs: how the technique works, normal vs malicious, relevant OS internals |
| **Blind Spots and Assumptions** | What it will miss (renamed binaries, logging gaps, alternative tooling) and what it assumes (Sysmon deployed, field X populated) |
| **False Positives** | Known benign triggers and how to recognise them |
| **Validation** | Exact steps to generate a true positive (e.g. an Atomic Red Team test ID or command) |
| **Priority** | Severity levels and the criteria for each |
| **Response** | Triage steps when it fires: what to check, how to escalate, containment options |
| **Additional Resources** | References, blog posts, prior incidents |

## Writing well
- Blind spots are the most valuable section: be specific (e.g. "LSASS access via `MiniDumpWriteDump` from a signed driver is not visible to Sysmon 10").
- Validation must be runnable by someone else; include expected alert fields.
- Response steps should match the IR playbook; link instead of duplicating long procedures.
- Store ADS docs next to the rule (same repo, same pull request) so they change together.

## Process
1. Draft ADS before writing the query; it clarifies the hypothesis.
2. Peer review covers both logic and ADS; rule does not deploy without it.
3. Run the validation; record the date and result in the doc.
4. Revisit after each true positive or false-positive tuning; update blind spots.

## Gotchas
- ADS docs that just restate the query add nothing; focus on context and response.
- A rule with an empty blind spots section has not been thought through.

## Verify
For a sample of production rules, each has an ADS document with a validation section that was executed within the review period and matches current rule logic.
