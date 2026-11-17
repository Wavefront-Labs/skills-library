---
id: computing-software.cybersecurity-defensive.cloud-security.amazon-detective
name: amazon-detective
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [amazon-detective, guardduty-investigation, behavior-graph, entity-profiles, aws-investigation, cloud-logging]
level: practitioner
status: docs-checked
description: "Investigate AWS findings with Amazon Detective: behavior graph and Organizations admin setup, entity profiles, finding groups, Detective Investigation, VPC flow pivots."
sources: ["https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html", "https://docs.aws.amazon.com/detective/latest/userguide/detective-investigation-about.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon Detective

Detective automatically extracts time-based events (login attempts, API calls, network traffic) from AWS
CloudTrail and Amazon VPC Flow Logs and ingests GuardDuty findings, then builds a **behavior graph**. It gives
access to up to a year of historical event data.

## Setup
- An account that enables Detective becomes the administrator account of a behavior graph and invites member accounts.
- With AWS Organizations, the organization management account designates a Detective administrator account, which enables organization accounts as members.
- Detective is regional: work with it in each Region where you need it.
- Detective integrates with Amazon Security Lake to query raw CloudTrail management events, VPC Flow Logs and EKS audit logs (EKS audit log version 2.0).
- First enablement starts a 30-day free trial; Detective shows estimated usage costs. Pricing is per GB of data; see the Detective pricing page rather than relying on figures here.

## Investigation workflow
Phases per the User Guide: triage (true or false positive), scoping (what was compromised, where it started, how long, related activity), response.
1. Start from a GuardDuty or Security Hub CSPM finding and pivot into the Detective console, or start from an entity such as an IP address or AWS user.
2. **Finding groups** show multiple related activities for a potential security event, useful for root cause of high-severity GuardDuty findings; triage the group rather than each finding.
3. **Entity profiles** hold visualizations from the behavior graph; each visualization has guidance with questions and next steps. Pivot from a profile to related entity and finding profiles.
4. **Detective Investigation** examines IAM users and IAM roles for indicators of compromise; it can be started from the console, the `StartInvestigation` API operation, or the `start-investigation` AWS CLI command.
5. VPC flow volume views show traffic for EC2 instances and Kubernetes pods.
6. Take action: archive false-positive GuardDuty findings (possible from Detective) or fix the resource configuration.

## Limits
- Detective shows aggregated and summarised views; for evidence, confirm in the underlying logs (Security Lake integration exposes raw logs).

## Verify
- [ ] Member accounts are enabled in every Region in use.
- [ ] Runbook for high-severity GuardDuty findings includes Detective pivots.

## Checked
2026-11-01. Confirmed against the Detective User Guide pages "What is Amazon Detective?" and "How Detective is used for investigation". Removed: the finding-groups and Organizations-accounts deep links (returned empty stubs), ATT&CK mapping, entity-type list, EKS/Security Hub data-source package claims, no-backfill and not-a-SIEM statements, and per-GB pricing.
Method: documentation only; no commands were run.
