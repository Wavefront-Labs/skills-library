---
id: computing-software.devops-ci-cd.gitlab-ci.audit-events-and-compliance-center
name: audit-events-and-compliance-center
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, compliance-center, audit-events, audit-event-streaming, compliance-violations, chain-of-custody]
level: advanced
status: docs-checked
description: "Use GitLab audit events and the compliance center: query and stream audit events, read standards adherence and violations, and export chain-of-custody reports."
sources: ["https://docs.gitlab.com/user/compliance/audit_events/", "https://docs.gitlab.com/user/compliance/audit_event_streaming/", "https://docs.gitlab.com/user/compliance/compliance_center/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit events and the compliance center

## 1. Audit events
Group/project → Secure → **Audit events**: who did what in the group or project (see the audit events page for the event types).
```bash
curl -H "PRIVATE-TOKEN: $T" "$API/groups/$GID/audit_events?created_after=2026-10-01T00:00:00Z&per_page=100"
```
Group audit event queries with `created_after` and `created_before` are limited to a maximum 30 day difference between the dates.

## 2. Streaming (Ultimate) — the real control
Top-level group → Secure → Audit events → Add streaming destination: HTTP endpoint (each event carries the verification token in the `X-Gitlab-Event-Streaming-Token` header; up to 20 custom HTTP headers) or Google Cloud Logging. Check the streaming page for other destination types.

## 3. Compliance center
Group → Secure → Compliance center:
The compliance center (Premium and Ultimate) is the central place for standards adherence reporting, violations reporting and compliance frameworks for the group. See its docs page for what each report contains and which exports exist.

## 4. Evidence workflow for an audit
1. Pull the compliance center violations report for the period.
2. Record remediation notes against each violation.
3. Pull audit events for settings changes on protected branches and approval rules.
4. Show policy project MR history (who changed enforcement, when).

## Gotchas
- Audit events and their sub-features span Free, Premium and Ultimate tiers; check the tier badge on each docs section.
- Streaming destinations failing silently = gap in records; monitor the receiver.

## Verify
- [ ] A test change appears at the streaming destination.

## Checked

2026-10-28. Confirmed against the GitLab audit events, audit event streaming and compliance center pages: Secure > Audit events, group audit events API 30-day limit for created_after/created_before, streaming is Ultimate, HTTP and Google Cloud Logging destinations, X-Gitlab-Event-Streaming-Token header, up to 20 custom headers, compliance center is Premium/Ultimate with standards adherence, violations and frameworks reports. Removed: S3 and Splunk destinations, instance-wide path, chain-of-custody export and violation details, retention and near-real-time claims (not in the fetched pages).

Method: documentation only; no commands were run.
