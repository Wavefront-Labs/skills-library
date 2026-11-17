---
id: computing-software.cybersecurity-defensive.threat-intelligence.intelligence-feedback-and-evaluation
name: intelligence-feedback-and-evaluation
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [intel-feedback, intelligence-lifecycle, cti-metrics, source-evaluation, priority-intelligence-requirements, threat-intelligence]
level: practitioner
status: draft
description: "Close the CTI loop: collecting consumer feedback, measuring intelligence usefulness, evaluating sources and products, and adjusting requirements and collection."
sources: ["https://www.sans.org/white-papers/", "https://www.first.org/global/sigs/cti/curriculum/", "https://csrc.nist.gov/pubs/sp/800/150/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Intelligence feedback and evaluation

The feedback phase of the intelligence lifecycle is the most neglected and the one that makes CTI useful.

## Collect feedback
- Every product carries a short feedback mechanism: was it relevant (1-5), timely, actionable, what
  action did you take, what do you need next.
- Structured check-ins with consumers per quarter (SOC, IR, VM, risk, executives) against their PIRs.
- Telemetry: IOC hit rates in detections, detections created from intel, hunts launched, patches
  prioritised due to intel.

## Measure
- **Requirement coverage**: % of PIRs with intelligence delivered this quarter.
- **Actionability**: % of products leading to a recorded action.
- **Timeliness**: time from public reporting/observation to product delivery.
- **Source performance**: unique contributions, false-positive rate, timeliness per feed/vendor
  (rate sources with Admiralty reliability over time).
- **Outcome stories**: incidents prevented or detected earlier thanks to intel (qualitative but powerful).

## Adjust
- Retire products nobody uses; change format (e.g. dashboard instead of PDF) where engagement is low.
- Re-prioritise collection: drop low-value feeds, add sources for uncovered PIRs.
- Update PIRs annually or after major business/threat changes.

## Gotchas
- Counting reports produced or IOCs ingested measures activity, not value.
- Feedback fatigue: keep forms to 2-3 questions and act visibly on feedback.

## Verify
Quarterly CTI review pack: PIR coverage, consumer feedback summary, source scorecard, and changes made.
