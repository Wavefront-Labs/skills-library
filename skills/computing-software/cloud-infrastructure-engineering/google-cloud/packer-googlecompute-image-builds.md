---
id: computing-software.cloud-infrastructure-engineering.google-cloud.packer-googlecompute-image-builds
name: packer-googlecompute-image-builds
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, custom-images, packer, packer-googlecompute, packer-cloud-build, golden-image, image-pipeline, iap-tunnel]
level: practitioner
status: docs-checked
description: "Build Compute Engine golden images with the Packer googlecompute builder over IAP with no external IP, publish to an image family, and run it in Cloud Build."
sources: ["https://developer.hashicorp.com/packer/integrations/hashicorp/googlecompute/latest/components/builder/googlecompute", "https://docs.cloud.google.com/build/docs/building/build-vm-images-with-packer", "https://docs.cloud.google.com/compute/docs/images/image-families-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packer googlecompute image builds

## 1. Template
```hcl
packer {
  required_plugins {
    googlecompute = { source = "github.com/hashicorp/googlecompute", version = ">= 1.1.1" }
  }
}
variable "project" { type = string }
variable "git_sha" { type = string }
source "googlecompute" "app" {
  project_id              = var.project
  zone                    = "<ZONE>"
  source_image_family     = "debian-12"
  source_image_project_id = ["debian-cloud"]
  machine_type            = "<MACHINE_TYPE>"
  image_name              = "app-base-<VERSION>"
  image_family            = "app-base"
  image_storage_locations = ["<REGION>"]      # accepts exactly 1 value
  image_labels            = { built-by = "packer", git-sha = var.git_sha }
  subnetwork              = "projects/<HOST>/regions/<REGION>/subnetworks/build"
  omit_external_ip        = true            # requires use_internal_ip = true
  use_internal_ip         = true
  use_iap                 = true            # SSH via IAP; the IAP API must be enabled and the firewall must allow IAP
  ssh_username            = "packer"
  service_account_email   = "packer-vm@${var.project}.iam.gserviceaccount.com"
  enable_secure_boot      = true            # Shielded VM image with Secure Boot
}
build {
  sources = ["source.googlecompute.app"]
  provisioner "shell" { script = "provision.sh" }
}
```
```bash
packer init . && packer validate -var project=<P> . && packer build -var project=<P> -var git_sha=<SHA> .
```

## 2. In Cloud Build
Cloud Build provides a community Packer builder image that you must build and push to Artifact Registry before you can use it as a step (see the Cloud Build "Build VM images with Packer" page). Then invoke `packer build` as a step with the template and `-var project_id=...`.
The build service account needs Compute Engine Instance Admin (v1) (`roles/compute.instanceAdmin.v1`) and Service Account User (`roles/iam.serviceAccountUser`); to store images in Artifact Registry it also needs Artifact Registry Writer. For IAP, the Packer docs say to add the service account to project-level IAP permissions with the "IAP-secured Tunnel User" role.

## 3. Release discipline
- Images go into a family; consumers reference `--image-family=app-base` and get the latest image available to their zone (family heads can differ by zone during rollout).
- Test the image (boot and smoke test) before it becomes visible: build into a staging family, then promote by re-creating in the prod family.
- Keep previous images in the family so rollback is a `--image=` away; see the image-families best-practices page for deprecation and rollback.

## Gotchas
- `use_iap` without the IAP prerequisites (API enabled, tunnel permission, firewall rule) leaves Packer waiting for SSH.
- OS Login enforced org-wide: set `use_os_login = true`, which imports a temporary SSH key into the account's login profile and sets `enable-oslogin` to TRUE in instance metadata.
- Using the default compute service account on the build VM can trigger org policy denials in hardened orgs.
- Clean cloud-init and agent state and SSH host keys in the provisioner so clones are unique.

## Verify
- [ ] `gcloud compute images describe-from-family app-base --project=<P>` returns the new image with the git-sha label.
- [ ] A VM from the family boots and passes the smoke test.

## Checked
2026-10-31. Confirmed in the Packer googlecompute builder page: `use_iap` prerequisites and IAP-secured Tunnel User role, `omit_external_ip` needs `use_internal_ip`, `image_storage_locations` takes 1 value, `image_labels`, `source_image_project_id`, `subnetwork` URL form, `use_os_login` behaviour, `enable_secure_boot`; in the Cloud Build page: community builder image must be built first, roles, plugin version form; in the image-families page: family head per zone and rollback. Corrected: `shielded_instance_config` block (the builder option is `enable_secure_boot`) and plugin constraint (`>= 1.1.1`). Removed: `execute_command`, the `{{timestamp}}` and `env()` template functions (not on the pages read), the unverified `hashicorp/packer:1.11` Cloud Build YAML, the IAP source range, `roles/iap.tunnelResourceAccessor` and `roles/compute.osAdminLogin` IDs, the deprecate-don't-delete advice and the Shared VPC role claim; the region, zone and machine type are placeholders.
Method: documentation only; no commands were run.
