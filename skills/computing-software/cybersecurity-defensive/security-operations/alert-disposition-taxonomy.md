---
id: computing-software.cybersecurity-defensive.security-operations.alert-disposition-taxonomy
name: alert-disposition-taxonomy
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [alert-triage, alert-disposition, true-positive, benign-true-positive, false-positive, closure-codes, detection-feedback, soc-metrics]
level: practitioner
status: draft
description: "Define and use alert closure dispositions (TP, benign TP, FP, duplicate, test) consistently so metrics and detection tuning are trustworthy, with mapping to SIEM fields."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/investigate-incidents#closing-an-incident", "https://docs.splunk.com/Documentation/ES/latest/User/Triagenotableevents", "https://www.elastic.co/guide/en/security/current/alerts-manage.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert disposition taxonomy

If analysts close alerts inconsistently, every downstream number (FP rate per rule, MTTR, coverage
claims) is wrong, and detection engineers tune the wrong rules.

## A workable set
| Disposition | Meaning | Feedback to detection |
|---|---|---|
| True positive - malicious | Real malicious or unauthorised activity | Keep; maybe raise severity |
| True positive - policy violation | Real activity, not malicious, breaks policy | Keep; route to owner |
| Benign true positive | Rule fired correctly on activity that is authorised (admin tool, pentest, scanner) | Tune with a scoped exclusion |
| False positive | Rule logic matched something it should not (parsing error, wrong logic) | Fix the rule |
| Duplicate | Same activity already tracked in another case | Improve grouping/throttling |
| Test / simulation | Purple team, atomic tests, phishing simulation | Exclude from metrics |
| Undetermined | Insufficient data to decide | Fix telemetry gap; track separately |

The benign TP vs FP split is the important one: benign TP means "detection works, environment
needs an exception"; FP means "detection is broken".

## Map to the SIEM
- Sentinel: Classification `TruePositive` (reason SuspiciousActivity), `BenignPositive`
  (SuspiciousButExpected), `FalsePositive` (IncorrectAlertLogic / InaccurateData), `Undetermined`.
- Splunk ES: configure Status values and add a custom "disposition" field in Incident Review
  settings (ES 7+ has a disposition field: True Positive, Benign Positive, False Positive, Other...).
- Elastic: close reason (False positive, Duplicate, True positive, Benign positive, Other) in 8.x cases/alerts.
Make the disposition mandatory at closure and require a short comment.

## Using the data
```
SecurityIncident
| summarize arg_max(TimeGenerated, *) by IncidentNumber
| where Status == "Closed"
| summarize total=count(), fp=countif(Classification=="FalsePositive"),
            btp=countif(Classification=="BenignPositive") by Title
| extend fp_rate = round(100.0*fp/total,1)
| order by fp desc
```
Review monthly: top FP rules get fixed; top benign TP rules get exclusions or are converted to
risk-based signals.

## Gotchas
- Analysts default to "False positive" for anything not malicious; train with examples.
- Closing duplicates as FP inflates FP rates.
- Undetermined should be rare; a high rate means missing logs or analyst skill gaps.

## Verify
Second-analyst QA sample: agreement rate on dispositions above ~90%; disagreements discussed in
team reviews and the definitions updated.
