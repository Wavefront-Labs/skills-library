---
id: computing-software.cloud-infrastructure-engineering.google-cloud.updating-marketplace-vm-deployments
name: updating-marketplace-vm-deployments
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-marketplace, marketplace-image-updates, marketplace-vm-upgrades, infrastructure-manager, terraform]
level: practitioner
status: docs-checked
description: "Keep Marketplace VM solutions current: find deployments, update by deploying a newer product version, snapshot first, and how deletion and Terraform deployments behave."
sources: ["https://docs.cloud.google.com/marketplace/docs/manage-deployments", "https://docs.cloud.google.com/marketplace/docs/deploy-through-CLI", "https://docs.cloud.google.com/marketplace/docs/manage-cli-deployments", "https://docs.cloud.google.com/infrastructure-manager/docs/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating Marketplace VM deployments

Per the Marketplace "Managing deployments" page, a software package is updated by deploying a newer version of the product from its Product Details page (the page's example: a LAMP stack with an older PHP is updated by deploying a version that includes a newer PHP). It does not describe in-place patching, so treat that as a vendor-specific decision and read the vendor's own upgrade notes.

## 1. Inventory what you run
- Console: from a product's Marketplace page a dropdown lists your previous deployments. For VM-based deployments, Deployment Manager shows a tree of the resources in each deployment; SSH from there or manage them on the VM instances page.
- Deployments made through the CLI (Terraform) appear on the VM instances page; from the listing's Command-line deployment tab, follow the link to Compute Engine and View running instances.
```bash
gcloud compute instances list
gcloud deployment-manager deployments list
gcloud infra-manager deployments list --location=<REGION>
```
The third command lists Infrastructure Manager deployments in general; the Marketplace pages do not say that Marketplace VM deployments appear there.

## 2. Choose the upgrade path
| Situation | Path |
|---|---|
| New product version available | deploy the newer version from the listing, migrate data and config, switch DNS or load balancer, retire the old deployment |
| Vendor documents an in-place upgrade | follow the vendor's procedure after a snapshot (not described in Google's pages) |
| Operating system patches only | use VM Manager patch jobs, as for any Compute Engine VM |
```bash
gcloud compute snapshots create pre-upgrade-<DATE> --source-disk=<BOOT_DISK> --source-disk-zone=<ZONE>
```

## 3. CLI (Terraform) deployments
Some VM listings support deployment with Terraform: the Command-line deployment tab offers either a downloadable module (follow its `README.md`) or generated code to paste into `main.tf`, then `terraform init` and `terraform apply`. You need Terraform, gcloud configured with the commands shown on the tab, and a service account with `roles/compute.admin`. Support is per listing. Google's pages for viewing CLI deployments cover viewing only, not update or delete steps; treat updates as a new `terraform apply` of the module version you choose and check the module README.

Infrastructure Manager, separately, runs Terraform for you: a deployment is updated by creating a new revision, a preview shows the effect first, and deleting a deployment runs `terraform destroy` on its resources.

## Gotchas
- Deleting a Deployment Manager deployment removes all of that deployment's instances and the persistent disks created at launch; software that uses Cloud Storage resources leaves them behind to delete by hand. Snapshot first.
- You cannot deploy multiple products to a single instance.
- Deployments carry default labels including `marketplace-suppress-benign-warnings`; remove it to see hidden warnings.
- Apps that include Cloud Logging and Monitoring agents can incur charges beyond the free allotment.

## Verify
- [ ] Every Marketplace VM is listed with product, version and owner.
- [ ] Post-upgrade health checks pass and the rollback snapshot is kept for the agreed period.

## Checked
Checked 2026-11-08 against the Marketplace "Managing deployments", "Deploy VM products using the CLI", "Manage CLI deployments" and Infrastructure Manager overview pages; the three gcloud command groups passed `check_commands.py`. Removed: boot-disk licence URL identification, BYOL instance-ID binding, the `source_image` Terraform variable example and the `--git-source-ref` flag, which none of the pages state.
Method: documentation only; no commands were run.
