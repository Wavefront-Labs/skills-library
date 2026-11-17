---
id: computing-software.cloud-infrastructure-engineering.google-cloud.requiring-shielded-and-confidential-vms-by-org-policy
name: requiring-shielded-and-confidential-vms-by-org-policy
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shielded-vm, require-shielded-vm, restrict-non-confidential-computing, confidential-computing, org-policy, trusted-image-projects]
level: practitioner
status: docs-checked
description: "Enforce Shielded VM and Confidential Computing with org policy: compute.requireShieldedVm, restrictNonConfidentialComputing, tag-based exceptions and rollout checks."
sources: ["https://cloud.google.com/compute/shielded-vm/docs/shielded-vm", "https://cloud.google.com/confidential-computing/confidential-vm/docs/org-policy-constraints", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requiring Shielded and Confidential VMs by org policy

You need the Organization Policy Administrator role (`roles/orgpolicy.policyAdmin`) to set these.

## Shielded VM
`constraints/compute.requireShieldedVm` (boolean): when enforced, all new Compute Engine VMs must use Shielded disk images with Secure Boot, vTPM and Integrity Monitoring enabled (Secure Boot can be disabled after creation if desired). Existing running instances keep working. By default none of these features are required.
```yaml
name: folders/<PROD>/policies/compute.requireShieldedVm
spec: {rules: [{enforce: true}]}
```
```bash
gcloud org-policies set-policy require-shielded.yaml
```

## Confidential Computing
`constraints/compute.restrictNonConfidentialComputing` (list): deny the services that would create non-confidential resources. The Confidential VM guide denies `compute.googleapis.com`:
```yaml
name: folders/<REGULATED>/policies/compute.restrictNonConfidentialComputing
spec:
  rules:
  - values: {deniedValues: ["compute.googleapis.com"]}
```
Console path: Organization policies > Restrict Non-Confidential Computing > Manage policy > Customize > Add a rule > Custom, Deny, value `compute.googleapis.com`. To lift it, set Allow all or delete the policy. A managed form, `constraints/compute.managed.restrictNonConfidentialComputing` (Preview in the constraints reference), can be applied or exempted with tags and conditional rules.

## Rollout
1. Test on one folder or project first; organization policies take a moment to propagate.
2. Check how the create-VM page looks in that project: the Confidential VM service section shows whether the policy is enforced.
3. Update instance templates and Terraform modules before enforcing.
4. Handle legacy appliances with a tag-conditioned rule or a separate folder.

## Gotchas
- Existing running instances are not affected (Shielded VM constraint); only new VMs are checked.
- Test every image source you use (custom, Marketplace) on a sandbox folder before enforcing broadly.

## Verify
- [ ] Creating a non-Shielded VM in the folder is refused; in the console the Confidential VM section shows the policy is enforced.

## Checked
2026-10-31. Confirmed against the organization policy constraints reference (requireShieldedVm wording and default, the managed restrictNonConfidentialComputing entry with tag exemption), the Shielded VM page (the constraint and the policy-admin requirement) and the "Enforce Confidential VM use" page (deny `compute.googleapis.com`, console steps, verification, how to disable). Removed: `UEFI_COMPATIBLE`, `--no-shielded-secure-boot`, `restrictConfidentialComputingType`, the `--confidential-compute-type` values, `policyViolationInfo`, the Asset Inventory image query, and claims about GKE/Dataproc and Confidential VM machine-type limits (none appear on the pages read).
Method: documentation only; no commands were run.
