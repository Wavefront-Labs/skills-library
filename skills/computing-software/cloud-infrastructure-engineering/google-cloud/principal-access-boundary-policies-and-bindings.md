---
id: computing-software.cloud-infrastructure-engineering.google-cloud.principal-access-boundary-policies-and-bindings
name: principal-access-boundary-policies-and-bindings
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, principal-access-boundary, pab-policy, pab-binding, principal-set, data-exfiltration, policy-bindings]
level: advanced
status: docs-checked
description: "Limit which resources a set of principals can ever access with Principal Access Boundary policies, bind them to principal sets, pin enforcement versions and test before rollout."
sources: ["https://cloud.google.com/iam/docs/principal-access-boundary-policies", "https://cloud.google.com/iam/docs/principal-access-boundary-policies-create", "https://cloud.google.com/sdk/gcloud/reference/iam/principal-access-boundary-policies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Principal access boundary (PAB) policies

**What it does:** a PAB policy says "principals in this set are only *eligible* to access
resources in these orgs/folders/projects". It never grants access; allow policies still do.
Use it to stop your users or service accounts using any role they hold — or are tricked into
holding — on resources outside your org.

## 1. Create the policy (org-scoped, location global)
```bash
gcloud iam principal-access-boundary-policies create corp-only \
  --organization=<ORG_ID> --location=global --display-name="Corp resources only" \
  --details-rules=description="own org",resources=//cloudresourcemanager.googleapis.com/organizations/<ORG_ID>,effect=ALLOW \
  --details-enforcement-version=<ENFORCEMENT_VERSION>
```
The enforcement version pins which permissions the policy can block. The API describes it as a version number (for example `1` or `latest`);
Google adds new versions over time, and each new version can block everything the previous one did, so pin a number for predictable behaviour and update deliberately.
A policy holds up to 500 rules and its name can be at most 63 characters.

## 2. Bind it to a principal set
```bash
gcloud iam policy-bindings create corp-only-workspace \
  --organization=<ORG_ID> --location=global \
  --policy=organizations/<ORG_ID>/locations/global/principalAccessBoundaryPolicies/corp-only \
  --target-principal-set=//iam.googleapis.com/locations/global/workspace/<WORKSPACE_ID>
```
Principal sets for bindings parented by an organisation (gcloud reference): organisation `//cloudresourcemanager.googleapis.com/organizations/<ORG_ID>`,
workforce pool `//iam.googleapis.com/locations/global/workforcePools/<POOL_ID>`, Workspace `//iam.googleapis.com/locations/global/workspace/<WORKSPACE_ID>`;
folders and projects have their own `//cloudresourcemanager.googleapis.com/...` forms (see the same page).

A binding can carry a condition (`--condition-expression`, `--condition-title`); see the *Create and apply PAB policies* guide for supported expressions.

## 3. Roll out
1. Start with SA principal sets of one project; run the workload; check Policy Troubleshooter for any denied call.
2. Extend to folders, then Workspace users.
3. Keep rules few and broad (whole orgs/folders); every Resource Manager resource (project, folder, organisation) the principals legitimately use must be listed.

## Gotchas
- Policy Troubleshooter can show Principal Access Boundary evaluation (Preview feature).
- Not all permissions are blocked at every version; read the enforcement-version list for the version you pin.
- PAB policies are additive: a principal's eligible resources are the union of all PAB policies it is subject to.
- Creating bindings needs permissions on the policy and on the principal set; the create guide lists the roles per principal-set type.

## Verify
- [ ] `gcloud iam policy-bindings search-target-policy-bindings --target=<set> --organization=<ORG_ID> --location=global` lists the binding.
- [ ] A bound SA with Storage Admin in a foreign project's bucket is denied; access inside the org works.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud references for `iam principal-access-boundary-policies create` (`--organization`, `--location`, `--display-name`, `--details-rules`, `--details-enforcement-version`), `iam policy-bindings create` (`--policy`, `--target-principal-set`, `--condition-expression`; principal set forms for organisation, workforce and Workspace) and `search-target-policy-bindings` (`--target`, `--location`), the PAB overview and create guides (additive policies, 500 rules, 63-character name, enforcement versions) and the IAM API v3 schema (`enforcementVersion` such as `1` or `latest`, rule `resources` and `effect`).
- Removed: the principal-set table rows not seen on the reference page (workload identity pool and SA sets), the `principal.type` condition example, and the claim about Google-owned public datasets. Added the missing `--location` to the search command.

Method: documentation only; no commands were run.
