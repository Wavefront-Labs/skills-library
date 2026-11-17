---
id: computing-software.cloud-infrastructure-engineering.google-cloud.writing-operational-runbooks-and-playbooks
name: writing-operational-runbooks-and-playbooks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, toil-automation, runbook-authoring, playbooks, alert-documentation, on-call, sre]
level: practitioner
status: docs-checked
description: "Write runbooks an on-call engineer can follow at 3am: structure, linking from alert documentation, exact gcloud commands, verification and rollback, and keeping them tested."
sources: ["https://sre.google/sre-book/being-on-call/", "https://cloud.google.com/monitoring/alerts/doc-variables", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing operational runbooks and playbooks

## Structure (one alert or task per runbook)
```markdown
# <Alert name / task>
Severity & impact: what users see, which SLO burns.
Owner: team, escalation contact.
## Quick check (2 min)
- Dashboard link (pre-filtered). - Log query link. - Recent deploys: `gcloud deploy releases list --delivery-pipeline=web --region=europe-west2 --limit=3`
## Diagnose
Decision tree: if X then section A; if Y then section B.
## Mitigate
A. Roll back: `gcloud run services update-traffic web --to-revisions=web-00042-abc=100 --region=europe-west2`
B. Scale: `gcloud compute instance-groups managed resize web-mig --size=12 --region=europe-west2`
Expected result + how to verify (metric returns below threshold within 5 min).
## Escalate when
Conditions and who.
## Afterwards
Ticket/postmortem link, cleanup steps.
Last tested: 2026-09-12 by <name>
```

## Link from alerts
A Cloud Monitoring alerting policy's documentation has a subject (up to 255 characters), `content` (Markdown, with variables such as `${resource.type}` and `${resource.label.zone}` that Monitoring replaces when sending notifications) and `links` (API only; a Link has `displayName` and `url`, up to three links; the console has no links field, so put the link in the Documentation field):
```
Runbook: https://wiki.example.com/runbooks/web-5xx?type=${resource.type}
```
Pages without a runbook link should fail review.

## Quality bar
- Copy-pasteable commands with placeholders clearly marked; no "check the usual places".
- Each mitigation has a verify step and a rollback.
- Safe by default: read-only diagnostics first.
- Tested in game days; date of last test visible. Stale (>6 months) runbooks flagged.
- Automate the steps that are always the same (then the runbook calls the automation).

## Gotchas
- Runbooks in a system that is down with the incident (wiki on the same platform) are useless; keep an offline/mirrored copy.
- IAM: on-call needs the permissions the runbook assumes, tested beforehand.

## Verify
- [ ] A new team member resolves a game-day scenario using only the runbook.

## Checked
2026-10-31. Confirmed against "Annotate notifications with user-defined documentation": subject limit, `content` and `links` fields, Link shape, three-link limit, console behaviour, `${resource.type}` and `${resource.label.*}` variables. The gcloud commands in the template were checked against the gcloud reference. Removed: `documentation.content` path wording, `${metric.value}` and `backend_target_name` (not documented variables), and the "newer field" remark. The "stale after 6 months" bar and the example dates are practice guidance, not documented figures. The SRE book and workbook on-call pages were fetched but no figure depends on them.
Method: documentation only; no commands were run.
