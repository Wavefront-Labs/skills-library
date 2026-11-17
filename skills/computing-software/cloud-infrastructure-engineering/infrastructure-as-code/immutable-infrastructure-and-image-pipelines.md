---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.immutable-infrastructure-and-image-pipelines
name: immutable-infrastructure-and-image-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, immutable-infrastructure, golden-images, image-pipeline, packer, hcl2-packer, ami, azure-image-builder, ec2-image-builder, shared-image-gallery, ansible-provisioner, image-hardening, cis-benchmark, image-promotion, image-tagging, launch-template, rolling-replace, instance-refresh, blue-green, no-ssh, cloud-init, image-expiry, sbom, provenance]
level: advanced
status: draft
description: "Run immutable infrastructure: build versioned golden images with Packer and Ansible, test and promote them, roll out via launch templates and instance refresh, keep runtime config to cloud-init."
sources: ["HashiCorp Packer documentation - HCL2 templates, amazon-ebs builder, ansible provisioner (https://developer.hashicorp.com/packer/docs)", "AWS documentation - EC2 Image Builder and Auto Scaling instance refresh", "Azure documentation - VM Image Builder and Azure Compute Gallery", "HashiCorp - Immutable infrastructure (Terraform/Packer patterns)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Immutable infrastructure and image pipelines

**Goal:** servers are replaced, never patched in place: every change is a new image
version built by a pipeline, tested, promoted, and rolled out by replacing instances.
No SSH in prod, no drift, rollback = previous image.

## 1. The pipeline
```
base role change / monthly cron
   -> packer build (base image: OS + hardening + agents)          tag: base=2026.10.15
   -> packer build (app image: FROM base + runtime + app bundle)   tag: app=1.42.0, base=2026.10.15
   -> test: boot, run Testinfra/InSpec/goss + smoke test
   -> promote: copy/share to prod account/region, tag env=prod (or AMI alias in SSM Parameter)
   -> terraform apply: launch template version -> ASG instance refresh / rolling
   -> expire images older than N
```
Two layers (base, app) keep app builds fast (minutes) and let base security patches roll
independently.

## 2. Packer (HCL2) with Ansible
```hcl
packer {
  required_plugins {
    amazon  = { source = "github.com/hashicorp/amazon",  version = ">= 1.3" }
    ansible = { source = "github.com/hashicorp/ansible", version = ">= 1.1" }
  }
}
variable "app_version" { type = string }
source "amazon-ebs" "app" {
  region        = "eu-west-1"
  instance_type = "t3.small"
  ssh_username  = "ec2-user"
  source_ami_filter {
    filters     = { name = "acme-base-*", "tag:status" = "promoted" }
    owners      = ["self"]
    most_recent = true
  }
  ami_name = "acme-app-${var.app_version}-{{timestamp}}"
  tags = { Name = "acme-app", app_version = var.app_version, built_by = "packer", source_ami = "{{ .SourceAMI }}" }
  imds_support = "v2.0"
  temporary_key_pair_type = "ed25519"
}
build {
  sources = ["source.amazon-ebs.app"]
  provisioner "ansible" {
    playbook_file   = "ansible/image.yml"
    user            = "ec2-user"
    use_proxy       = false
    extra_arguments = ["-e", "app_version=${var.app_version}", "--scp-extra-args", "'-O'"]
  }
  provisioner "shell" { inline = ["sudo cloud-init clean --logs", "sudo rm -rf /var/log/*.log ~/.ssh/authorized_keys"] }   # generalise
  post-processor "manifest" { output = "manifest.json" }
}
```
`packer init . && packer validate . && packer build -var app_version=1.42.0 .` → the manifest gives the
AMI id for the next stage. Azure: `azure-arm` source + Compute Gallery; GCP: `googlecompute`.
Managed alternatives (EC2 Image Builder, Azure Image Builder) suit teams that want the pipeline
and the SSM/recipe model hosted; Packer is portable across clouds.

The Ansible playbook used for images is the same roles as for mutable hosts, with image-only
tasks (`cloud-init clean`, remove host keys, machine-id reset) at the end; `sshd` config and
users are baked, secrets are **not** — they are fetched at boot from a secrets manager by the
instance role.

## 3. Test before promote
Boot the image in a throwaway instance (Terraform in CI or Packer's own run) and run
`testinfra`/`goss`/`InSpec` against it; CIS benchmark scan for base images; app smoke test on a
test port. Promotion = tagging (`status=promoted`) and copying to prod accounts
(`aws ec2 copy-image`, or share via launch permissions / AMI aliases in SSM: `/acme/ami/app/prod`).
Terraform reads the alias, so a promotion is a parameter change, not a code change.

## 4. Roll out and roll back
- Terraform: `aws_launch_template` with `image_id = data.aws_ssm_parameter.app_ami.value`, ASG with
  `instance_refresh { strategy = "Rolling", preferences { min_healthy_percentage = 90 } }` and
  `lifecycle { create_before_destroy = true }` on the template. Each apply creates a new LT version
  and the ASG replaces instances in waves behind the load balancer health check.
- Blue/green: a second ASG/target group, shift traffic, keep the old one for rollback until bake time expires.
- Rollback = point the SSM alias at the previous image and apply; keep at least two promoted versions.
- Kubernetes nodes: node image via the managed node group version/AMI; same refresh model.

## 5. Runtime config (keep it tiny)
cloud-init/user-data only for: hostname, fetching secrets, writing the environment name, starting
the app. If user-data grows past ~30 lines, it belongs in the image or in a config service. Instance
identity (`env`, `role` tags) comes from Terraform; the app reads them via IMDS/metadata.

## 6. Hygiene
- Expire: deregister AMIs/snapshots older than N versions (`aws ec2 describe-images --owners self` + lifecycle policy; Compute Gallery versions have `end_of_life_date`).
- Provenance: record source image, git SHA, build time in tags; sign images where supported; generate an SBOM (`syft`) per build.
- No SSH: remove authorized keys, use SSM Session Manager/serial console for break-glass; alert on SSH logins.
- Emergency patch of a running fleet is a **rebuild**, not a `yum update` — if it takes too long, the pipeline is the thing to fix.

## Gotchas
- `most_recent = true` on a source filter without an `owners` restriction can pick a stranger's AMI; always set owners and a status tag.
- Ansible provisioner over Packer's SSH proxy breaks with newer OpenSSH scp; `use_proxy = false` and `--scp-extra-args '-O'` (or `ANSIBLE_SCP_IF_SSH`/`sftp`) fix it.
- Forgetting `cloud-init clean` or leaving `/etc/machine-id` populated gives every instance the same identity (DHCP, journald, some licences).
- Instance refresh counts health from the ASG health check; without ELB health checks a broken image is "healthy" when the OS boots. Use ELB checks + `min_healthy_percentage`.
- Baked time-limited things (certs, agent tokens, OS trial licences) expire in the image; fetch at boot or rebuild on a schedule.
- Image build runs in a VPC with egress to repos; air-gapped builds need an internal mirror configured in the base role.

## Verify
- [ ] A base-role change produces a new base image, a new app image, test results and a promoted tag with no manual steps.
- [ ] Changing the SSM AMI alias and applying triggers an instance refresh that completes with zero failed health checks; reverting the alias rolls back the same way.
- [ ] `aws ec2 describe-instances` for prod shows every instance on the promoted image id; no instance has SSH authorized keys.
