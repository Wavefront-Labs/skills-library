---
id: computing-software.cloud-infrastructure-engineering.google-cloud.opening-a-google-cloud-support-case
name: opening-a-google-cloud-support-case
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, support, support-case, customer-care, incident-response, priority, open-support-case, case-creation]
level: practitioner
status: docs-checked
description: "Open Google Cloud support cases that get solved fast: choose priority honestly, include resource names, UTC timestamps and verbatim errors, attach evidence, use the API."
sources: ["https://cloud.google.com/support/docs/best-practice", "https://cloud.google.com/support/docs/manage-cases", "https://cloud.google.com/support/docs/reference/rest", "https://cloud.google.com/support/docs/procedures"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Opening a Google Cloud support case

## 1. Priority (be honest)
| Priority | Meaning (Google's definitions, abridged) |
|---|---|
| P1 Critical | unusable in production, critical business impact; immediate attention needed |
| P2 High | production degraded, noticeable user-facing errors, moderate business impact |
| P3 Medium | limited scope or severity, no user-visible impact |
| P4 Low | little or no impact; consultative tickets |
Explain in detail why you chose P1. A P1 alerts an expert immediately and starts with a live call (Google Meet by
default; give your own video link if you cannot use it). You can raise an existing P2-P4 case to P1 when production
is impacted. Setting the right priority for long enough is usually better than escalating; escalate when the
process is not working for you.

## 2. What to include (template)
```
Summary: Cloud SQL instance orders-prod (project acme-prod, us-east1) rejects new connections since 2026-10-16T09:42Z.
Impact: checkout down for many users; P1 because ...
Resources: projects/acme-prod/instances/orders-prod; Cloud Run service checkout (revision checkout-00142).
Timeline (ISO 8601, UTC): 09:40 deploy of revision 00142; 09:42 first "too many connections"; 09:55 rolled back, no change.
Errors (verbatim): FATAL: remaining connection slots are reserved ... ; request IDs from logs.
What we tried: restart at 10:05; increased max_connections at 10:10.
Ask: why connections remain exhausted after rollback.
Contact: on-call channel / timezone.
```
Attach: log snippets, example stack traces, screenshots showing exactly what you see, and for network issues packet captures taken
at both endpoints at the same time (tcpdump or Wireshark; practise before you need it). Redact secrets and PII first.

## 3. Mechanics
- Console: Support, create a case, and pick the product and the specific feature having the issue.
- Managing cases needs Tech Support Editor (`roles/cloudsupport.techSupportEditor`) on the project, folder or organization.
- Cloud Support API v2: `POST /v2/{parent}/cases` creates a case, `GET /v2/caseClassifications:search` lists valid
  classifications, `:escalate` and `:close` act on a case. Look up the request body fields on the Case reference
  page before automating.
```bash
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://cloudsupport.googleapis.com/v2/caseClassifications:search?query=<TEXT>"
```

## Gotchas
- Without resource names and timestamps the engineer has to ask first.
- Basic Support is included for all customers and covers billing and payments support; check your package for technical cases.

## Verify
- [ ] Case has priority, resources, UTC timeline, verbatim errors, evidence and a clear ask before submission.

## Checked
2026-10-28. Confirmed on the support best-practice, manage-cases and REST reference pages: priority definitions, P1
live-call behaviour, raising to P1, escalation advice, ISO 8601 timestamps, tcpdump/Wireshark and simultaneous
captures, role id, API methods, Basic Support wording. Removed (not on the pages): response-time targets by tier,
example impact percentage, HAR advice, Access Approval advice, the POST body field list and the `q` query shape of
the classification search beyond the documented method.
Method: documentation only; no commands were run.
