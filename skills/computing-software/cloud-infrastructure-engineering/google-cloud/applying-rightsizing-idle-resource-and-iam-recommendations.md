---
id: computing-software.cloud-infrastructure-engineering.google-cloud.applying-rightsizing-idle-resource-and-iam-recommendations
name: applying-rightsizing-idle-resource-and-iam-recommendations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, active-assist, vm-rightsizing-recommender, machine-type-recommendations, idle-vm-recommender, idle-disk-recommender, role-recommendations, iam-recommender-apply, cost-optimisation]
level: practitioner
status: docs-checked
description: "Act on the three most valuable recommenders safely: VM machine-type rightsizing, idle VMs, disks, IPs and images, and IAM role recommendations with rollback."
sources: ["https://docs.cloud.google.com/compute/docs/instances/apply-machine-type-recommendations-for-instances", "https://docs.cloud.google.com/compute/docs/instances/viewing-and-applying-idle-vm-recommendations", "https://docs.cloud.google.com/compute/docs/viewing-and-applying-idle-resources-recommendations", "https://docs.cloud.google.com/policy-intelligence/docs/review-apply-role-recommendations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying rightsizing, idle-resource and IAM recommendations

## 1. Machine-type rightsizing
Recommender: `google.compute.instance.MachineTypeRecommender` (zonal). Recommendations are generated from Cloud Monitoring metrics over the previous 8 days, so workloads with infrequent spikes (for example monthly) are not captured: skip those VMs. Installing the **Ops Agent** improves accuracy because it supplies memory metrics. Applying needs `compute.instances.stop` on the instance.
Apply to a VM:
```bash
gcloud compute instances stop app-1 --zone=<Z>
gcloud compute instances set-machine-type app-1 --zone=<Z> --machine-type=<RECOMMENDED>
gcloud compute instances start app-1 --zone=<Z>
```

## 2. Idle resources
| Recommender | Typical action |
|---|---|
| `google.compute.instance.IdleResourceRecommender` | snapshot or machine image, then stop (optionally delete) |
| `google.compute.disk.IdleResourceRecommender` | snapshot, then delete the unattached disk |
| `google.compute.address.IdleResourceRecommender` | release unused static IPs |
| `google.compute.image.IdleResourceRecommender` | delete old images |
```bash
gcloud compute snapshots create pre-delete-data-7 --source-disk=data-7 --source-disk-zone=<Z>
gcloud compute disks delete data-7 --zone=<Z>
```
A stopped but undeleted VM still incurs disk charges, and deleting a VM can lose data: snapshot first. Tag the snapshot with the ticket and a delete-after date.

## 3. IAM role recommendations
`google.iam.policy.Recommender` (location `global`) proposes removing or replacing roles whose permissions were not used in the past 90 days; it does not analyse every role.
```bash
gcloud recommender recommendations list --project=<P> --location=global --recommender=google.iam.policy.Recommender --format=json
```
Needed roles: IAM Recommender Viewer (`roles/recommender.iamViewer`) to read, IAM Recommender Admin (`roles/recommender.iamAdmin`) to apply. Apply in the console or by editing the policy as the recommendation's operations describe; record the original binding so you can restore it. The console keeps a recommendations history: a change can be reverted there within 90 days. Exclude break-glass accounts and rarely used but critical roles (DR, quarterly jobs) because the usage window cannot see them.

## Gotchas
- Machine-type changes need a stop; schedule with owners.
- A VM idle by design (standby) can be flagged; dismiss with a reason.
- Read each IAM recommendation's details before applying.

## Verify
- [ ] After rightsizing, CPU and memory are healthy over a full weekly cycle and the cost change is visible in billing.
- [ ] Applied IAM recommendations have a rollback record and no access incidents reported.

## Checked
2026-10-31. Confirmed in the Compute Engine machine-type, idle VM and idle disk/address/image recommendation pages and the Policy Intelligence role-recommendation page: recommender IDs, the 8-day window, Ops Agent advice, stop permission, the unused-for-90-days wording, the two IAM Recommender roles, the 90-day revert note. Removed: the instanceGroupManager recommender, the `content.overview.*` format fields (overview is a free-form map), the 80 percent target, "billed while unattached" for IPs and the group-binding claim. The disk, address and image idle page URL is the redirect target of the old disks path.
Method: documentation only; no commands were run.
