---
id: computing-software.cloud-infrastructure-engineering.google-cloud.customer-care-support-cases-and-escalation
name: customer-care-support-cases-and-escalation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, customer-care, support-cases, escalation, support-tiers, standard-support, enhanced-support, premium-support, technical-account-manager, tam, case-priority, p1-case, support-api, cloud-support-api, service-health, support-iam, third-party-technology-support, value-add-services]
level: practitioner
status: docs-checked
description: "Use Google Cloud Customer Care well: pick a support tier, grant support IAM, file complete cases, escalate correctly, track cases via the Cloud Support API."
sources: ["https://cloud.google.com/support/docs/overview", "https://cloud.google.com/support/docs/customer-care-procedures", "https://cloud.google.com/support/docs/reference/rest", "https://cloud.google.com/service-health/docs/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customer Care: support cases and escalation

**Goal:** when you need Google, the case is answered within the SLA you pay for, carries
everything an engineer needs on first read, and the organisation knows how to escalate without burning goodwill.

## 1. Choose the tier (org-level decision)
| Tier | What the overview says | Pick when |
|---|---|---|
| Basic | included for all customers: documentation, community support, Cloud Billing support, Active Assist recommendations | hobby |
| **Standard** | unlimited 1:1 technical support; Cloud Support API; Active Assist; 4-hour response for P2 cases | small to medium organisations with workloads under development |
| **Enhanced** | faster response times; Cloud Support API, Third-Party Technology Support, Recommender | medium to large companies running production |
| **Premium** | adds Customer Aware Support and an assigned Technical Account Manager (TAM); bought via sales | enterprises with priority workloads |
Value-add services are an extra purchase for Enhanced (Technical Account Advisor Service, Planned Event Support, Assured Support, Media CDN) and Premium (Mission Critical Services, Assured Support, Media CDN). Response times and prices change: read the Technical Support Services Guidelines and the vendor's pricing pages.

## 2. Access (do not make everyone a support editor)
- `roles/cloudsupport.techSupportEditor` to the on-call group (view, create, update, escalate, close cases), `roles/cloudsupport.techSupportViewer` for the rest; `roles/cloudsupport.admin` manages the support account and case sharing. Only Organization Administrators can change the support service, which applies to all projects in the organization.
- Enable the **Cloud Support API** for automation; set up **Personalized Service Health** so Google-side incidents reach you before customers do.

## 3. File a case that gets solved on the first reply
- **Priority** by impact, per the priority table: P1 = critical impact, service unusable in production, no quick workaround; P3 = medium impact, service partially impaired; P4 = low impact, service fully usable. Pick the real priority and change it when impact changes, giving the reason.
- Title: `<service> <symptom> since <UTC time> in <region> — <impact>`.
- Body: project ID/number, resource names, **UTC timestamps**, exact error text and the identifiers from the response, API response excerpts, what changed (deploy, config, IAM), what you tried, business impact in numbers, your contact and timezone.
- Attach: log files and text output; use widely supported non-proprietary formats such as PNG, TXT or PDF. One issue per case.
- **Escalate inside the case** (Escalate button in the console, or `cases.escalate` in the Support API) with a reason. Escalation flags process breaks: for a high-impact issue, raise the priority to P1 first, because escalating shortly after a priority change can slow resolution. An escalated case goes to an Escalation Manager and you are notified within an hour. Your TAM can advise on priority versus escalation.
- Keep the case updated with changes in impact; a closed case can be reopened within 15 days by replying; after that, file a new case.

## 4. Automate case tracking
```bash
gcloud services enable cloudsupport.googleapis.com
```
The Cloud Support API (`cloudsupport.googleapis.com`) manages cases for Customer Care offerings: `cases.create`, `cases.escalate`, `cases.close`, `cases.list`, `cases.search`, `cases.attachments` and `cases.comments`. Use it to mirror cases into your ticketing tool and post updates to the incident channel; see the REST reference for the exact request shapes.

## 5. Premium: using the TAM
Premium includes an assigned Technical Account Manager. Ask the TAM whether to change priority or escalate, and share your launch dates and reliability reports so they can help. Scope of other TAM services: see the Premium Support overview.

## Gotchas
- Support covers the Google product; "my app returns 500" needs your evidence that the platform (not the code) misbehaves — bring the audit log and metrics.
- Third-party technology support helps resolve multi-vendor issues such as organization setup, configuration and troubleshooting.
- The support service applies per organization, so projects outside one depend on that entitlement; confirm yours under Support > Overview.
- Service Health shows only incidents affecting your projects (personalised) — if nothing shows, the problem may be yours.

## Verify
- [ ] Support tier is documented with its SLA table; on-call group has `techSupportEditor`; Service Health alerts route to the on-call channel (test notification received).
- [ ] The case template (title/body/attachments) is in the incident runbook.
- [ ] Cloud Support API script lists open cases and posts to the incident channel on update.

## Checked
2026-10-31. Confirmed in the Customer Care overview, Customer Care procedures and Support API REST reference pages (fetched this batch): tier descriptions, value-add services, IAM roles (techSupportViewer, techSupportEditor, admin), priority definitions, escalation behaviour and reasons, 15-day reopen window (the draft said 14), Support API methods. Removed: P1 response times per tier, percentage-of-spend pricing, Access Transparency claim, TAM service list, curl example and org path, guessed sources (escalation and premium-support-tam pages return 404).
Method: documentation only; no commands were run.
