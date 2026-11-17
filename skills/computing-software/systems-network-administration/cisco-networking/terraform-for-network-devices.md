---
id: computing-software.systems-network-administration.cisco-networking.terraform-for-network-devices
name: terraform-for-network-devices
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [terraform-network, terraform, iosxe-provider, infrastructure-as-code, network-automation, state, plan-apply]
level: practitioner
status: draft
description: "Manage Cisco IOS-XE configuration with the Terraform iosxe provider (RESTCONF): provider setup, resources, plan/apply workflow, import and drift handling."
sources:
  - https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest/docs
  - https://developer.hashicorp.com/terraform/cli/commands/plan
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terraform for network devices

The `CiscoDevNet/iosxe` provider configures IOS-XE over RESTCONF. Similar providers exist for
NX-OS, ACI, Meraki, SD-WAN, Catalyst Center, Palo Alto, Fortinet.

## Setup
```hcl
terraform {
  required_providers {
    iosxe = { source = "CiscoDevNet/iosxe" }
  }
}
provider "iosxe" {
  username = var.user
  password = var.password
  devices = [
    { name = "sw1", url = "https://10.99.0.21" },
    { name = "sw2", url = "https://10.99.0.22" },
  ]
}
resource "iosxe_vlan" "users" {
  for_each = toset(["sw1", "sw2"])
  device   = each.key
  vlan_id  = 10
  name     = "USERS"
}
```
Device needs `restconf` + `ip http secure-server` + an AAA user with privilege 15.

## Workflow
```bash
terraform init
terraform plan -out tf.plan      # review the diff: this is the change record
terraform apply tf.plan
```
- State is the source of truth for what Terraform owns. Store it remotely (S3 + lock,
  Terraform Cloud) and never edit it by hand.
- Existing config: `terraform import` or `import {}` blocks to adopt objects before managing them.
- Drift (someone used the CLI): next `plan` shows a change back. Decide: re-apply or update code.
- Terraform manages only resources it knows; it does not remove unknown CLI config.

## Gotchas
- `iosxe_save_config` (or a provider setting) is needed to persist running->startup.
- Applying to many devices: use `-parallelism` carefully; RESTCONF on small switches is slow.
- Secrets: pass via env (`TF_VAR_password`) or a vault; state files contain them in clear.

## Verify
- [ ] `terraform plan` shows "No changes" after apply; CLI shows the intended config; state stored remotely with locking.
