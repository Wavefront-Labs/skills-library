---
id: computing-software.cloud-infrastructure-engineering.google-cloud.unattended-project-recommender-and-cleanup
name: unattended-project-recommender-and-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, recommender, unattended-project-cleanup, project-utilization-recommender, idle-projects, project-deletion]
level: practitioner
status: docs-checked
description: "Find unattended Google Cloud projects with the project utilization recommender: CLEANUP_PROJECT and RECLAIM_PROJECT subtypes, access levels, listing commands and limits."
sources: ["https://cloud.google.com/recommender/docs/unattended-project-recommender", "https://cloud.google.com/recommender/docs/recommenders#unattended_project", "https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unattended project recommender and cleanup

The unattended project recommender analyses usage across projects in your organisation over the last
30 days and gives usage insights (networking, API, project owner, service activity and more),
recommendations to turn down low-usage projects, and recommendations to assign a new owner to
high-usage projects with no active owner. It works only for projects assigned to Google Cloud
organisations, and generates nothing for Apps Script projects (auto-deleted with their scripts).
Impact categories listed: SECURITY, COST, SUSTAINABILITY.

| Usage over 30 days | Recommendation | Subtype |
|---|---|---|
| low | review or delete the project | `CLEANUP_PROJECT` |
| high, user owners exist but none active | reclaim by assigning a new owner | `RECLAIM_PROJECT` |
Insights use subtype `PROJECT_ACTIVITY`. If the API returns no recommendations, the project is either not
unattended or is under 30 days old.

## Access
Project Owners see their projects; Organization Administrators see the organisation's projects; Billing
Administrators see projects on a billing account. Insights and recommendations per organisation or billing
account are limited to 10,000; for larger estates use project-level views or the BigQuery export.

## List
```bash
gcloud recommender recommendations list --organization=<ORG> --location=global \
  --recommender=google.resourcemanager.projectUtilization.Recommender
gcloud recommender recommendations list --project=<P> --location=global \
  --recommender=google.resourcemanager.projectUtilization.Recommender
```
Insights use `--insight-type=google.resourcemanager.projectUtilization.Insight`. When viewing a different
project or the organisation, the page passes `--billing-project=<PROJECT_WITH_RECOMMENDER_API>`; check the
page for the exact flags before scripting.

## Before acting
Check the project's utilization insight before deleting, since the page says the low or high usage ranking
is computed from it. The cited shutdown page does not
document liens or recovery; see the project-liens skill for those.

## Verify
- [ ] Each cleanup recommendation is acted on or dismissed with a reason.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the recommender page: 30-day window, subtypes, access levels, 10,000 limit, recommender and
insight type IDs. The org and project `gcloud recommender` commands passed the command checker. Removed
as not stated on the cited pages: owner-notification process, label scheme, claim and success states, billing
unlink step, `projects delete` recovery text, and cost-avoided tracking.
