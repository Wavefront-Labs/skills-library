---
id: computing-software.systems-network-administration.patch-management.golden-vm-image-pipelines-packer
name: golden-vm-image-pipelines-packer
category: computing-software
field: systems-network-administration
product: patch-management
tags: [packer, golden-image, golden-ami, image-pipeline, immutable-infrastructure, azure-compute-gallery, image-patching]
level: advanced
status: docs-checked
description: "Build patched golden VM images with Packer: HCL templates, update and hardening provisioners, testing, versioned publishing to AMIs or Azure Compute Gallery, and retirement."
sources:
  - https://developer.hashicorp.com/packer/docs
  - https://developer.hashicorp.com/packer/integrations/hashicorp/amazon/latest/components/builder/ebs
  - https://developer.hashicorp.com/packer/integrations/hashicorp/ansible/latest/components/provisioner/ansible
  - https://developer.hashicorp.com/packer/docs/commands/init
  - https://learn.microsoft.com/en-us/azure/virtual-machines/azure-compute-gallery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Golden VM image pipelines with Packer

**Goal:** every new VM starts fully patched and hardened, and fleets are refreshed by redeploying the new image rather than patching in place.

## Template (AWS example)
```hcl
packer {
  required_plugins { amazon = { source = "github.com/hashicorp/amazon", version = ">= <plugin-version>" } }
}
source "amazon-ebs" "rhel9" {
  region        = "eu-west-1"
  instance_type = "t3.medium"
  ssh_username  = "ec2-user"
  ami_name      = "golden-rhel9-{{timestamp}}"
  source_ami_filter {
    filters     = { name = "<RHEL 9 AMI name pattern>", virtualization-type = "hvm" }
    owners      = ["<AMI publisher account ID>"]
    most_recent = true
  }
  tags = { Base = "rhel9" }
}
build {
  sources = ["source.amazon-ebs.rhel9"]
  provisioner "shell" { inline = ["sudo dnf -y update", "sudo dnf -y install amazon-ssm-agent"] }
  provisioner "ansible" { playbook_file = "harden-cis.yml" }
  provisioner "shell" { inline = ["sudo cloud-init clean", "sudo rm -f /etc/ssh/ssh_host_*"] }
}
```
```bash
packer init . && packer validate . && packer build .
```
Windows images need an update provisioner, restarts between passes and a final sysprep; see the Packer provisioner documentation.

## Pipeline
1. Monthly (and on critical advisories): build from the newest vendor base.
2. Test: boot an instance, run InSpec/Goss checks (hardening, agents present, no pending updates), vulnerability scan.
3. Publish: share/promote the AMI or Azure Compute Gallery image version; update the launch template / scale set model to the new version via IaC.
4. Roll fleets (instance refresh / node rotation).
5. Retire images older than N versions; deregister and delete snapshots.

## Gotchas
- Leaving machine-specific state (SSH host keys, cloud-init state, Windows SID without sysprep) in the image causes duplicates.
- Pin plugin versions; Packer plugin changes can break builds.

## Verify
New instances from the image show zero missing updates on first assessment, and inventory shows all running instances on images younger than the policy age.

## Checked
Date: 2026-10-27. Documentation checked: Packer `amazon-ebs` builder reference (`source_ami_filter` with `filters`, `owners`, `most_recent`; `ami_name` must be unique, `{{timestamp}}`), Packer `ansible` provisioner page (`playbook_file`), `packer init` page (`required_plugins`, HCL templates only). Replaced the Red Hat AMI owner ID, AMI name pattern, plugin version pin and `isotime` tag value, which were not confirmed, with placeholders, and removed the named Windows provisioners.

Method: documentation only; no commands were run.
