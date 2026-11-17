---
id: computing-software.cloud-infrastructure-engineering.google-cloud.service-account-insights-and-unused-account-cleanup
name: service-account-insights-and-unused-account-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, service-account-insights, unused-service-accounts, key-usage-activity, disable-service-account, service-account-cleanup, policy-intelligence-activity, last-authentication, activity-analyzer, sa-lifecycle, delete-service-account, undelete-service-account]
level: practitioner
status: docs-checked
description: "Find service accounts and keys unused for 90 days with Policy Intelligence insights and Activity Analyzer, then disable, soak and delete them (30-day undelete window)."
sources: ["https://docs.cloud.google.com/policy-intelligence/docs/service-account-insights", "https://docs.cloud.google.com/policy-intelligence/docs/activity-analyzer-service-account-authentication", "https://docs.cloud.google.com/iam/docs/service-accounts-disable-enable", "https://docs.cloud.google.com/iam/docs/service-accounts-delete-undelete"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Service account insights and unused account cleanup

**Goal:** service accounts that have not authenticated in 90 days are found, disabled, observed,
and only then deleted, so removal never breaks a workload.

## 1. Where the data comes from
- **Insights**: findings about service accounts that have not authenticated in the past 90 days (insight type `google.iam.serviceAccount.Insight`, subtype `SERVICE_ACCOUNT_USAGE`, with a `lastAuthenticatedTime`). View needs `roles/recommender.iamViewer`; changing an insight needs `roles/recommender.iamAdmin`.
- **Activity Analyzer** (`gcloud policy-intelligence query-activity`): last authentication per service account (`serviceAccountLastAuthentication`) and per key (`serviceAccountKeyLastAuthentication`). Needs `roles/policyanalyzer.activityAnalysisViewer`.
```bash
gcloud recommender insights list --project=<PROJECT_ID> --location=global \
  --insight-type=google.iam.serviceAccount.Insight
gcloud policy-intelligence query-activity --project=<PROJECT_ID> --activity-type=serviceAccountLastAuthentication
gcloud policy-intelligence query-activity --project=<PROJECT_ID> --activity-type=serviceAccountKeyLastAuthentication
```

## 2. Blind spots to cross-check before acting
- Requests authenticated by API keys bound to service accounts are not recorded, so such accounts can look unused.
- Authentication with Google APIs outside Google Cloud, such as domain-wide delegation to Workspace APIs, is not tracked by Activity Analyzer or insights; cross-reference Cloud Monitoring service account usage metrics first.
- Also check what the account is attached to and whether other projects' IAM policies reference it (for example `gcloud asset search-all-iam-policies --query='policy:<SA_EMAIL>' --scope=organizations/<ORG_ID>`). Seasonal jobs are the usual false positives.

## 3. Disable, soak, delete
```bash
gcloud iam service-accounts disable <SA_EMAIL>      # reversible
# observe for a period you choose; watch logs and tickets
gcloud iam service-accounts enable <SA_EMAIL>       # rollback if something broke
gcloud iam service-accounts delete <SA_EMAIL>
```
Disabling means applications lose access to Google Cloud resources through that account; a disabled
account can be re-enabled. Google recommends disabling unused accounts before deleting them.

You can undelete a service account if it was deleted 30 days ago or less; after 30 days IAM
permanently removes it and Google cannot recover it, even through support. A new account created
with the same name is a separate identity that does not inherit the deleted account's roles
(undeleting keeps the identity and its roles). Bindings for a deleted account appear with a
`deleted:` prefix and a `?uid=` suffix. Check the delete/undelete page for the undelete command
and the identifier it takes.

## Verify
- [ ] Insight and Activity Analyzer lists reviewed for prod projects, with API-key and Workspace-delegation cases excluded.
- [ ] Each deletion ticket records the disable date and the account's identifiers.

## Checked
2026-10-31. Confirmed against the service account insights page (90 days, insight type and subtype, roles, API-key and domain-wide delegation caveats), Activity Analyzer page (query-activity, activity types, role), the disable/enable page (apps lose access; re-enable; disable before deleting) and the delete/undelete page (30 days, permanent removal, separate identity). Removed: console Status badge, one-year data window, default-service-account advice, the unique-ID requirement for undelete, undelete command, automation recipe, mark-accepted usage and the "last authenticated tracks token minting" and cross-project gotchas (not confirmed in fetched pages).
Method: documentation only; no commands were run.
