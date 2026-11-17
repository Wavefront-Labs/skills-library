---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-principal-access-boundary-denials
name: troubleshooting-principal-access-boundary-denials
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, principal-access-boundary, pab-troubleshooting, principal-access-boundary-denials, policy-troubleshooter, iam]
level: practitioner
status: docs-checked
description: "Diagnose access denied by principal access boundary policies: identify bound policies for a principal, read Policy Troubleshooter PAB results, and fix rules or bindings."
sources: ["https://cloud.google.com/iam/docs/principal-access-boundary-policies", "https://cloud.google.com/iam/docs/troubleshoot-policies", "https://cloud.google.com/iam/docs/principal-access-boundary-policies-view"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Troubleshooting principal access boundary denials

A PAB policy limits which resources a principal is **eligible** to access regardless of allow
grants. Symptom: user has the right role, Policy Troubleshooter says access is denied by a
principal access boundary.

## 1. Which PAB policies apply to the principal?
Bindings attach PAB policies to principal sets (workforce pools, Workspace/Cloud Identity domain,
projects' principals):
```bash
gcloud iam policy-bindings search-target-policy-bindings --organization=<ORG> --location=global \
  --target="//cloudresourcemanager.googleapis.com/organizations/<ORG>"
gcloud iam principal-access-boundary-policies describe <PAB_ID> --organization=<ORG> --location=global
```

## 2. Run Policy Troubleshooter
Use Policy Troubleshooter in the console or the REST API. Troubleshooting Principal Access Boundary policies is a Preview feature, and the API response includes a
`pabPolicyExplanation` alongside `denyPolicyExplanation` and the allow-policy explanation. The gcloud reference
describes `gcloud policy-intelligence troubleshoot-policy iam` (`--principal-email`, `--permission`) as covering allow and deny policies,
so use the console or REST for the PAB part.

## 3. Fix
- Resource outside every boundary: add it (or its project/folder/org) to a PAB rule's resources:
  ```yaml
  details:
    rules:
    - effect: ALLOW
      resources: ["//cloudresourcemanager.googleapis.com/organizations/<ORG>",
                  "//cloudresourcemanager.googleapis.com/projects/partner-share-prj"]
  ```
  then `gcloud iam principal-access-boundary-policies update ... --details-rules=...`.
- Wrong population bound: narrow the binding with a CEL condition on `principal.type` / `principal.subject`.

## Gotchas
- The enforcement version (`enforcementVersion`, for example `1` or `latest`) decides which permissions the policy can block; Google adds new versions over time.
- Multiple PAB policies bound to a principal are additive: eligibility is the **union** of their resources.
- PAB does not grant anything; allow policies are still needed.

## Verify
- [ ] Troubleshooter shows the principal as eligible under PAB and access granted.

## Checked

- Date: 2026-10-27
- Confirmed against the PAB overview and view/create guides (policy-binding search by principal set, additive policies, enforcement versions), the troubleshooting-access page (Preview PAB troubleshooting; `pabPolicyExplanation`, `denyPolicyExplanation`, `overallAccessState`), the IAM API v3 schema (`enforcementVersion`, rule `resources` and `effect`) and the gcloud references for `iam policy-bindings search-target-policy-bindings` (`--target`, `--organization`, `--location`), `principal-access-boundary-policies describe` and `update` (`--details-rules`, `--add-details-rules`).
- Fixed: the dead source URL (404; the page is `principal-access-boundary-policies-view`), the missing `--location` on the search command, and the gcloud troubleshooter claim (the reference says allow and deny only). Removed: the 4-week `latest` delay and the propagation-time note.

Method: documentation only; no commands were run.
