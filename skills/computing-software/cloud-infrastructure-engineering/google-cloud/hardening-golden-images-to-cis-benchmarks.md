---
id: computing-software.cloud-infrastructure-engineering.google-cloud.hardening-golden-images-to-cis-benchmarks
name: hardening-golden-images-to-cis-benchmarks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, golden-image, cis-benchmark, packer, ansible, openscap, compute-engine, cis-hardened-images, image-hardening]
level: practitioner
status: docs-checked
description: "Build CIS-hardened Compute Engine golden images: start from CIS Marketplace images or harden in Packer with Ansible, keep the guest agent working, and scan with OpenSCAP."
sources: ["https://cloud.google.com/compute/docs/images/image-management-best-practices", "https://www.cisecurity.org/cis-hardened-images/google", "https://www.open-scap.org/getting-started/", "https://developer.hashicorp.com/packer/integrations/hashicorp/googlecompute/latest/components/builder/googlecompute"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hardening golden images to CIS benchmarks

## Two paths
1. **CIS Hardened Images** from Cloud Marketplace (the CIS page lists Level 1 images such as Windows
   Server 2016-2025). Fastest; can be the base image for Packer. See the marketplace listing for licensing cost.
2. **Harden yourself** from Google public images using CIS benchmark automation (for example
   community Ansible roles), then scan with OpenSCAP.

## Packer + Ansible
The `googlecompute` builder arguments below are documented on the Packer googlecompute builder page.
```hcl
source "googlecompute" "base" {
  project_id              = var.project
  source_image_family     = "ubuntu-2204-lts"
  source_image_project_id = ["ubuntu-os-cloud"]
  zone                    = "europe-west2-b"
  image_family            = "ubuntu-2204-cis"
  image_name              = "ubuntu-2204-cis-{{timestamp}}"
  ssh_username            = "packer"
  use_iap                 = true
  omit_external_ip        = true
}
build {
  sources = ["source.googlecompute.base"]
  provisioner "ansible" { playbook_file = "cis.yml" }
  # then run an OpenSCAP scan with the SCAP content and profile for your OS
}
```
`omit_external_ip` requires `use_internal_ip = true` (the Packer page says so), so add it. Image families
always return the latest non-deprecated image.

## GCP-specific exceptions (do not break these)
- Keep the guest environment (guest agent, OS Login, OS Config agent if you use it) working.
- Do not block the metadata server in host firewall rules.
- CIS partition rules (separate `/tmp`, `/var`) on a single-disk image: use bind mounts or tmpfs, or document an exemption.

## Pipeline
Cloud Build triggers Packer on a schedule, scans, publishes to the image family, deprecates old images, and
the organization policy constraint `constraints/compute.trustedImageProjects` restricts which projects
images may come from.

## Verify
- [ ] Scan score meets target with documented exceptions; a VM from the image passes OS Login SSH and agent checks.

## Checked
2026-10-28. Confirmed: Packer googlecompute argument names and semantics (source_image_family, source_image_project_id,
image_family, image_name, use_iap, omit_external_ip needing use_internal_ip, image families), CIS Level 1 Marketplace
images listed on the CIS page, `constraints/compute.trustedImageProjects` in the org policy constraints list.
Removed (not confirmed): per-hour billing, Ansible role and variable names, the OpenSCAP profile id and content path,
the metadata IP address, GVNIC/UEFI features, NTP advice, and exact guest-agent package names.
Method: documentation only; no commands were run.
