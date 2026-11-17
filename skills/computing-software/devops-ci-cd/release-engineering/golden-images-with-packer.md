---
id: computing-software.devops-ci-cd.release-engineering.golden-images-with-packer
name: golden-images-with-packer
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, packer, golden-image, hcl2, ami-pipeline, image-hardening, hcp-packer]
level: practitioner
status: docs-checked
description: "Build versioned golden machine images with Packer: HCL2 templates, provisioners, cloud builders, CI pipelines, image testing and promotion across environments."
sources:
  - https://developer.hashicorp.com/packer/docs
  - https://developer.hashicorp.com/packer/integrations/hashicorp/amazon/latest/components/builder/ebs
  - https://developer.hashicorp.com/packer/docs/templates/hcl_templates
  - https://developer.hashicorp.com/hcp/docs/packer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Golden images with Packer

Golden images bake OS patches, agents and hardening once, so environments launch identical, fast-booting machines and drift less.

## Template (HCL2)
```hcl
packer {
  required_plugins {
    amazon  = { source = "github.com/hashicorp/amazon",  version = "~> 1.3" }
    ansible = { source = "github.com/hashicorp/ansible", version = "~> 1.1" }
  }
}
variable "version" { type = string }

source "amazon-ebs" "base" {
  region        = "eu-west-2"
  instance_type = "t3.small"
  ssh_username  = "ec2-user"
  ami_name      = "base-al2023-${var.version}"
  source_ami_filter {
    filters     = { name = "<base-image-name-pattern>", virtualization-type = "hvm" }
    owners      = ["<owner-account-id>"]
    most_recent = true
  }
  tags = { Version = var.version, GitSha = "{{ env `GITHUB_SHA` }}", SourceAMI = "{{ .SourceAMI }}" }
  ami_users = ["111111111111", "222222222222"]   # share to env accounts
  encrypt_boot = true
}

build {
  sources = ["source.amazon-ebs.base"]
  provisioner "shell"   { inline = ["sudo dnf -y update"] }
  provisioner "ansible" { playbook_file = "ansible/base.yml" }
  provisioner "shell"   { inline = ["sudo rm -f /etc/ssh/ssh_host_*"] }   # generalise
  post-processor "manifest" { output = "manifest.json" }
}
```
```bash
packer init . && packer fmt -check . && packer validate -var version=1.4.0 .
packer build -var version=1.4.0 .
```

## Pipeline
1. Trigger: weekly (patches), on base-OS release, or on change to provisioning code.
2. Build in a dedicated image-build account/subscription with a minimal IAM role.
3. Test the image: launch, run InSpec/Goss/testinfra checks (agents running, CIS controls, no SSH keys baked), then terminate.
4. Publish metadata (for example an SSM parameter `/images/base/latest`; HCP Packer registry channels are another option, see its docs), promote dev -> prod by updating the channel/parameter after soak.
5. Consumers (Terraform/ASGs) reference the parameter, not a hard-coded AMI ID.
6. Deregister old images and snapshots after N versions (keep what running instances use).

## Other builders
Other builders exist for Azure (`azure-arm`) and other platforms; see the Packer integrations docs.

## Pitfalls
- Secrets in provisioners end up in the image or logs; fetch at boot instead (cloud-init, instance role).
- Forgetting to generalise: duplicate machine-ids and SSH host keys.
- `most_recent = true` without tests silently pulls in a new base image; record `SourceAMI` in tags.

## Verify
- [ ] Image build, test and promotion run from CI with versioned outputs; consumers deploy by parameter.
- [ ] A test instance from the image passes compliance checks and boots without manual steps.

## Checked

2026-10-28. Confirmed against Packer docs: `required_plugins` block (Packer 1.7.0 and later) with `~>` version constraints, `packer init`, `packer fmt -check`, `packer validate -var`, `packer build -var`, the `manifest` post-processor `output` option, and amazon-ebs options `source_ami_filter` (with `filters`, `owners`, `most_recent`), `ami_users`, `encrypt_boot` and the `{{ .SourceAMI }}` template variable. Removed: the Amazon Linux AMI name filter and `owners` alias (now placeholders), `use_proxy`, `cloud-init clean`, the Sysprep and builder-list claims, and HCP Packer channel specifics.

Method: documentation only; no commands were run.
