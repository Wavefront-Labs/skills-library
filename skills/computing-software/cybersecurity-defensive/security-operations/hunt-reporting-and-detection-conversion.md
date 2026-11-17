---
id: computing-software.cybersecurity-defensive.security-operations.hunt-reporting-and-detection-conversion
name: hunt-reporting-and-detection-conversion
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, hunt-reporting, detection-engineering, hypothesis, hunt-documentation, peak-framework, metrics]
level: practitioner
status: draft
description: "Document threat hunts and convert findings into detections: hypothesis records, scope and data used, results including nulls, new detections, data gaps and hunt metrics."
sources: ["https://www.splunk.com/en_us/blog/security/peak-threat-hunting-framework.html", "https://www.sans.org/white-papers/the-who-what-where-when-why-and-how-of-effective-threat-hunting/", "https://github.com/palantir/alerting-detection-strategy-framework"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hunt documentation and conversion to detections

**Goal:** every hunt leaves something durable: a record others can repeat, detections or
analytics where possible, and documented data gaps, even when nothing malicious was found.

## Hunt record (one per hunt)
- **ID, title, hunter, dates.**
- **Hypothesis:** "Adversaries with initial access are using scheduled tasks created
  remotely to move laterally (T1053.005) in the server estate."
- **Trigger / rationale:** intel report, recent incident, new technique, gap in detection coverage.
- **Scope:** hosts/segments, time range, data sources and their completeness.
- **Queries/analytics used:** exact text, links to notebooks.
- **Results:** findings (malicious, suspicious, benign but notable), with evidence links;
  explicitly state "no evidence found" with what was checked.
- **Outputs:** detections created or improved, allowlists, data gaps logged, hygiene issues
  (misconfigurations found), incidents opened.
- **Lessons and follow-ups.**
The PEAK framework (Prepare, Execute, Act with Knowledge) structures the same flow.

## Converting to detections
Ask of each hunt query: can it run on a schedule with tolerable volume?
- Yes: write it as a detection with ADS documentation, backtest, tune (the hunt data is the
  backtest), deploy via the detection pipeline.
- Too noisy: convert to a risk-based signal or a scheduled hunting dashboard reviewed weekly.
- Not possible due to data: log the gap (missing log source, field not collected) with an
  owner; this is often the most valuable output.

## Metrics
Hunts completed, techniques covered (ATT&CK heatmap of hunts), detections created, data
gaps found and closed, incidents discovered by hunting. Avoid judging hunts only by
incidents found; a null result over a well-defined scope is information.

## Gotchas
- Hunts with no hypothesis turn into aimless querying; write it before starting.
- Findings in chat threads are lost; the record is the deliverable.
- Repeating a hunt later needs the exact queries and scope; save them.

## Verify
Quarterly review: each hunt has a record, and each "convertible" query has a matching
detection or a logged reason why not.
