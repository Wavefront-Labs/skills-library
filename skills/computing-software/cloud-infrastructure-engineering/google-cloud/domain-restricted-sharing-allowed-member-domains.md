---
id: computing-software.cloud-infrastructure-engineering.google-cloud.domain-restricted-sharing-allowed-member-domains
name: domain-restricted-sharing-allowed-member-domains
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, org-policy, domain-restricted-sharing, allowed-policy-member-domains, iam, customer-id, tags]
level: advanced
status: docs-checked
description: "Restrict IAM grants to your own customer IDs or organization principal set with iam.allowedPolicyMemberDomains, tag-conditioned exceptions and a dry-run rollout."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/restricting-domains", "https://cloud.google.com/resource-manager/docs/organization-policy/tags-organization-policy", "https://cloud.google.com/sdk/gcloud/reference/org-policies/set-policy"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Domain restricted sharing (allowed policy member domains)

**Goal:** only identities that belong to your organization principal set or your Google Workspace customer IDs can be added to allow policies, unless the organisation deliberately allows more.

## 1. Find the identifiers (not domain names)
The legacy constraint takes **Google Workspace customer IDs** or organization principal sets such as `is:principalSet://cloudresourcemanager.googleapis.com/organizations/<ORG_ID>` (the page also shows `principalSet://iam.googleapis.com/organizations/<ORG_ID>`), not domain names. The customer ID is the `DIRECTORY_CUSTOMER_ID` column of:
```bash
gcloud organizations list
```
You need `resourcemanager.organizations.get` on each organization. Collect one per trusted directory (your own, subsidiaries, a trusted partner). Entering the organization principal set also allows workforce identity pools, service accounts and workload identity pools in the organization, and service agents; a customer ID also allows all identities in its domains.

## 2. Set the policy at the organisation
```yaml
# policy.yaml
name: organizations/<ORG_ID>/policies/iam.allowedPolicyMemberDomains
spec:
  rules:
  - values:
      allowedValues: [C03abc123, C04def456]
```
```bash
gcloud org-policies set-policy policy.yaml
gcloud org-policies describe iam.allowedPolicyMemberDomains --project=<P> --effective
```
The managed constraint `iam.managed.allowedPolicyMembers` is the newer way to implement this and takes `allowedPrincipalSets`; see the restricting-domains page for its YAML. To dry-run from the CLI use `gcloud org-policies set-policy POLICY_PATH --update-mask=dryRunSpec`.

## 3. Exceptions via tags, not per-project overrides
A rule can carry a condition that matches a tag, so a tagged resource gets a different allowed set:
```yaml
spec:
  rules:
  - condition:
      expression: "resource.matchTag('<ORG_ID>/<TAG_KEY>', '<TAG_VALUE>')"
    values:
      allowedValues: [C03abc123, <EXTRA_CUSTOMER_ID>]
  - values:
      allowedValues: [C03abc123]
```
`matchTag` takes the namespaced tag key and the value short name. Control who may attach that tag value, since attaching it changes the policy outcome.

## 4. Roll out safely
1. Inventory existing external members first with Cloud Asset Inventory (`gcloud asset search-all-iam-policies --scope=organizations/<ORG_ID>`, filtered on the domains you do not trust).
2. Apply in dry-run (`dryRunSpec:` in the policy file or `--update-mask=dryRunSpec`) and watch the policy-violation logs.
3. Enforce at a test folder, then the org.

## Gotchas
- A violation fails with `FAILED_PRECONDITION: One or more users named in the policy do not belong to a permitted customer`.
- A partner's domain name alone is not enough; add its customer ID or principal set.
- Integrations that grant roles to identities outside your set will fail; add the customer ID or a tagged exception.

## Verify
- [ ] Granting a role to a user outside the allowed set in a test project fails with the error above.
- [ ] The tagged resource accepts the extra customer ID; an untagged one rejects it.
- [ ] Asset search for external members returns only documented exceptions.

## Checked
2026-10-31. Confirmed against "Restricting identities by domain" and "Scope policies with tags": constraint name and YAML, customer ID vs principal set, `DIRECTORY_CUSTOMER_ID`, what each identifier allows, `matchTag` syntax and conditional rule structure, `--update-mask=dryRunSpec`, the exact error text; `gcloud org-policies` and `asset search-all-iam-policies` flags checked against the gcloud reference. Removed: the `allUsers` and public-bucket exception (`allowAll`), the `owner.directoryCustomerId` format key, the non-retroactive claim, the asset-search query string and `gmail.com` examples (not on the pages read).
Method: documentation only; no commands were run.
