---
id: computing-software.cloud-infrastructure-engineering.google-cloud.custom-images-and-image-pipelines
name: custom-images-and-image-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, custom-images, image-families, golden-image, image-pipeline, packer, compute-engine-images, image-import, image-sharing, trusted-image-projects, deprecate-image, guest-environment, shielded-vm-images, image-build, os-hardening, cis-image]
level: practitioner
status: docs-checked
description: "Build golden Compute Engine images with Packer, roll out and back with image families, share across projects, and restrict launches with the trusted-image org policy."
sources: ["https://cloud.google.com/compute/docs/images", "https://cloud.google.com/compute/docs/images/create-custom", "https://cloud.google.com/compute/docs/images/image-families-best-practices", "https://developer.hashicorp.com/packer/integrations/hashicorp/googlecompute/latest/components/builder/googlecompute", "https://cloud.google.com/compute/docs/images/restricting-image-access", "https://cloud.google.com/compute/docs/images/guest-environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom images and image pipelines

**Goal:** every VM boots from an image your pipeline built this month, with patches and agents
baked in, promotable and roll-back-able through an image family, and nobody can launch from a random public image.

## 1. Where images live
- One **image project** per org (`prj-c-images`), images are global resources inside it.
- Share with `roles/compute.imageUser` to the consuming projects' service accounts/groups on the image project.
- Org policy `compute.trustedImageProjects` lists the allowed source projects (Google's public
  `debian-cloud`, `ubuntu-os-cloud` etc. plus yours); anything else is refused at instance creation.

## 2. Build with Packer (the common path)
```hcl
source "googlecompute" "app" {
  project_id          = "prj-c-images"
  source_image_family = "debian-12"
  zone                = "europe-west1-b"
  machine_type        = "e2-standard-2"
  image_name          = "app-base-{{timestamp}}"
  image_family        = "app-base"
  image_labels        = { built_by = "cloudbuild", cis = "level1" }
  ssh_username        = "packer"
  use_iap             = true          # no external IP needed
  omit_external_ip    = true
  enable_secure_boot  = true          # keep Shielded VM features in the image
  enable_vtpm         = true
  enable_integrity_monitoring = true
  service_account_email = "packer@prj-c-images.iam.gserviceaccount.com"
}
build {
  sources = ["source.googlecompute.app"]
  provisioner "shell" { scripts = ["harden.sh", "install-ops-agent.sh", "app-deps.sh", "cleanup.sh"] }
}
```
- `cleanup.sh`: `apt-get clean`, remove ssh host keys, truncate logs, `cloud-init clean` or equivalent,
  so each VM gets unique keys and the image is small.
- Keep the **guest environment** installed on images you build (see the Guest environment page).
- Run Packer from your CI system with a build service account that has only the Compute Engine and IAP permissions the build needs; check the Packer googlecompute builder page for required settings.

## 3. Alternatives
- `gcloud compute images create app-v3 --source-disk=<DISK> --source-disk-zone=...` from a prepared VM (stop it first for a clean filesystem).
- `gcloud compute images import` for VMDK/VHD/raw from on-prem (the virtual disk import tool, for existing on-prem or other-cloud images).
- Manual image build from a stopped VM is fine for one-offs; anything repeated goes in the pipeline.

## 4. Families for rollout and rollback
- A family (`app-base`) points to its most recent image. Instance templates that
  reference `--image-family=app-base` pick up the latest at *next VM creation*, not for running VMs.
- Promote = build a new image into the family. Roll back = deprecate the bad one:
  `gcloud compute images deprecate app-base-1729000000 --state=DEPRECATED` → family resolves to the previous image.
  The deprecation state is one of `ACTIVE`, `DEPRECATED`, `OBSOLETE`, `DELETED` (Compute API `DeprecationStatus`). To roll back, the previous image must not itself be deprecated.
- For controlled fleets pin the resolved image name in the MIG template and let the pipeline
  roll it with a canary (see `gce-autoscaling`); use the family only for dev/sandbox templates.

## 5. Hygiene
- Label images with source commit and build time, and prune old images on a schedule you choose.
- Scan the built image before promoting it into the family.
- Never bake secrets or long-lived service-account keys; fetch at boot from Secret Manager using the VM's attached SA.

## Verify
- [ ] `gcloud compute images describe-from-family app-base --project=prj-c-images` returns today's build.
- [ ] Launching from an image project not in `trustedImageProjects` fails with `constraints/compute.trustedImageProjects`.
- [ ] A VM from the image has unique SSH host keys, your agents running, and Secure Boot enabled.
- [ ] Deprecating the newest image makes the family resolve to the previous one.

## Checked
2026-10-31. Confirmed: Packer googlecompute builder fields (image_labels, use_iap, omit_external_ip, enable_secure_boot, enable_vtpm, enable_integrity_monitoring, service_account_email, image_family) on the HashiCorp builder page; `roles/compute.imageUser` and `compute.trustedImageProjects` on the Compute Engine image-access pages; family rollback by deprecating the newest image; deprecation states from the Compute API discovery document; gcloud commands validated by check_commands.py. Removed: unconfirmed guest-agent behaviour, Cloud Build service-account roles, import tool claims, Cloud Run pruning, Trivy, keep-last-3 rule. Names such as `prj-c-images` and `app-base` are illustrative.
Method: documentation only; no commands were run.
