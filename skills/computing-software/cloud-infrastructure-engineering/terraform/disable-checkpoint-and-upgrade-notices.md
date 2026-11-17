---
id: computing-software.cloud-infrastructure-engineering.terraform.disable-checkpoint-and-upgrade-notices
name: disable-checkpoint-and-upgrade-notices
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, disable-checkpoint, checkpoint-disable, cli-config, air-gapped, telemetry]
level: practitioner
status: docs-checked
description: "Turn off Terraform's checkpoint version and security-bulletin checks with disable_checkpoint, disable_checkpoint_signature or CHECKPOINT_DISABLE for offline and locked-down hosts."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file", "https://developer.hashicorp.com/terraform/cli/commands/version", "https://checkpoint.hashicorp.com/", "https://raw.githubusercontent.com/hashicorp/go-checkpoint/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling checkpoint

## What checkpoint is
Checkpoint is a HashiCorp service that provides version and alert information. Products may occasionally send it information about the product currently running, to detect outdated versions and security vulnerabilities and other alerts. This is configurable and not required. Terraform is one of the products it knows; Terraform providers are intentionally not integrated with it.

In Terraform, `terraform version` shows the Terraform version, platform, installed providers and the results of upgrade and security checks unless they are disabled. `terraform version -json` includes no upgrade or security information beyond the outdated flag shown in its example output.

## Off switches
CLI configuration file (`~/.terraformrc`, `terraform.rc` in `%APPDATA%` on Windows, or the file named by `TF_CLI_CONFIG_FILE`):
```hcl
disable_checkpoint           = true   # disables upgrade and security bulletin checks that reach HashiCorp services
disable_checkpoint_signature = true   # keeps the checks, but drops the anonymous id used to de-duplicate warnings
```
Environment: HashiCorp's go-checkpoint client documents `CHECKPOINT_DISABLE`, which makes the underlying checkpoint component itself disabled (its example is `CHECKPOINT_DISABLE=1 packer build`); each application also has its own setting.
```bash
export CHECKPOINT_DISABLE=1
```

## When to disable
Air-gapped or egress-filtered hosts, CI where unexpected outbound calls raise alerts, and environments whose policy forbids sending any product information. Disabling the checks also removes the "out of date" notice, so track Terraform upgrades another way.

## Checked
Date: 2026-11-07. Read in full: the CLI configuration file page (Available Settings and the rest), the `terraform version` page, the checkpoint.hashicorp.com landing page and the go-checkpoint README. Removed as unsupported: the `checkpoint-api.hashicorp.com` endpoint and the list of commands that call it, the claims about what is sent and where the signature is stored, the time-delay claim, the OpenTofu statement, the Renovate/Dependabot and bulletin-subscription advice, and both Verify items. Whether `CHECKPOINT_DISABLE` is honoured by every Terraform release is not stated by the Terraform pages; it comes from the go-checkpoint README only.
Method: documentation only; no commands were run.
