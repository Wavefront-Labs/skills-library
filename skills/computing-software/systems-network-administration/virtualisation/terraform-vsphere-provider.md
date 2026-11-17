---
id: computing-software.systems-network-administration.virtualisation.terraform-vsphere-provider
name: terraform-vsphere-provider
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [terraform-vsphere, vsphere-automation, infrastructure-as-code, vsphere-virtual-machine, terraform, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Provision vSphere VMs with the Terraform vsphere provider: lookups, cloning from a template with customisation, cloning rules, reboot triggers, import."
sources:
  - https://github.com/vmware/terraform-provider-vsphere/blob/main/docs/index.md
  - https://github.com/vmware/terraform-provider-vsphere/blob/main/docs/resources/virtual_machine.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Terraform vSphere provider

## Provider and lookups
```hcl
terraform {
  required_providers {
    vsphere = { source = "vmware/vsphere" }   # pin a version constraint you have tested
  }
}
provider "vsphere" {
  vsphere_server       = var.vcenter
  user                 = var.vsphere_user        # or VSPHERE_USER; never commit credentials
  password             = var.vsphere_password    # or VSPHERE_PASSWORD
  allow_unverified_ssl = false
}
data "vsphere_datacenter" "dc"        { name = "DC1" }
data "vsphere_compute_cluster" "c" {
  name          = "Prod"
  datacenter_id = data.vsphere_datacenter.dc.id
}
data "vsphere_datastore" "ds" {
  name          = "datastore1"
  datacenter_id = data.vsphere_datacenter.dc.id
}
data "vsphere_network" "net" {
  name          = "App-VLAN20"
  datacenter_id = data.vsphere_datacenter.dc.id
}
data "vsphere_virtual_machine" "tpl" {
  name          = "tpl-rhel9"
  datacenter_id = data.vsphere_datacenter.dc.id
}
```
`user`, `password` and `vsphere_server` are required (environment variables `VSPHERE_USER`, `VSPHERE_PASSWORD`, `VSPHERE_SERVER`); `allow_unverified_ssl` is optional (`VSPHERE_ALLOW_UNVERIFIED_SSL`).

## Clone a VM
```hcl
resource "vsphere_virtual_machine" "app" {
  name             = "app01"
  resource_pool_id = data.vsphere_compute_cluster.c.resource_pool_id
  datastore_id     = data.vsphere_datastore.ds.id
  folder           = "Prod/App"
  num_cpus = 4
  memory   = 8192
  guest_id = data.vsphere_virtual_machine.tpl.guest_id
  firmware = data.vsphere_virtual_machine.tpl.firmware
  network_interface {
    network_id   = data.vsphere_network.net.id
    adapter_type = data.vsphere_virtual_machine.tpl.network_interface_types[0]
  }
  disk {
    label            = "Hard Disk 0"
    size             = data.vsphere_virtual_machine.tpl.disks[0].size
    thin_provisioned = data.vsphere_virtual_machine.tpl.disks[0].thin_provisioned
  }
  clone {
    template_uuid = data.vsphere_virtual_machine.tpl.id
    customize {
      linux_options {
        host_name = "app01"
        domain    = "corp.example"
      }
      network_interface {
        ipv4_address = "10.0.20.31"
        ipv4_netmask = 24
      }
      ipv4_gateway    = "10.0.20.1"
      dns_server_list = ["10.0.0.10"]
    }
  }
}
```
- `resource_pool_id` is required, and one of `datastore_id` or `datastore_cluster_id` must be set. `folder` is relative to `/<datacenter>/vm`. `guest_id` defaults to `otherGuest64`; `adapter_type` defaults to `vmxnet3`; `thin_provisioned` defaults to `true`.
- For a `customize` block, `linux_options` is required when customising a Linux guest, with `host_name` and `domain` both required. Omitting `ipv4_address` means DHCP. `dns_server_list` is used by Windows guests and ignored by Linux guests (Linux uses the global DNS settings).
- For templates imported from OVF/OVA, the provider docs recommend the `vapp { properties = {...} }` block rather than `extra_config` (settings may be ignored) and say using `customize` is not recommended there.

## Cloning rules (from the provider docs)
- The source VM must not be powered on, and all its disks must be SCSI disks.
- Specify at least as many `disk` blocks as the template has, matched by `unit_number`; each `size` must be at least the template disk's size. Disk `size` is in whole GB.
- With `linked_clone`, `size`, `thin_provisioned` and `eagerly_scrub` must match the template disk exactly.
- Keep the default of one SCSI controller unless you need more; set `scsi_type` to match the template.

## Operations
- Import: `terraform import vsphere_virtual_machine.vm /dc-01/vm/bar/foo` (the `vm` path segment is required, and folders are included). Imported disks are labelled `Hard Disk N` starting at 0 by SCSI order, so use matching labels in the configuration; disks import with `keep_on_remove` enabled until the first apply. A VM with no storage controllers cannot be imported.
- Tags: set `tags = [...]` with tag IDs from the `vsphere_tag` resource.

## Gotchas
- Changing any of these reboots the VM: `cpu_hot_add_enabled`, `memory_hot_add_enabled`, `firmware`, `guest_id`, `hardware_version`, `extra_config`, `efi_secure_boot_enabled`, `vtpm`, `num_cores_per_socket`, `disk.unit_number`, and `memory` when reducing it or when increasing it with `memory_hot_add_enabled` false. Read the plan.
- CPU and memory hot add are not available on all guest OSes and need at least one apply first.
- Without `host_system_id`, vSphere chooses a host in the cluster according to DRS placement policy.
- `shutdown_wait_timeout` defaults to 3 minutes and `force_power_off` to `true`, so a graceful shutdown that times out is forced off during updates.
- Large disks can hit "context deadline exceeded": raise the provider `api_timeout`.
- Do not label a disk with an `orphaned_disk_` prefix; it is reserved.

## Verify
`terraform plan` after apply shows no changes; the VM in vCenter has the expected folder, network, IP and tags.

## Checked
Checked 2026-11-08 against the terraform-provider-vsphere index and `vsphere_virtual_machine` resource docs on GitHub. Removed (not stated there): the `~> 2.10` version constraint, `ignore_changes` advice for `clone[0].template_uuid`, content-library templates for `clone`, `-parallelism=5`, and the claim that changing `num_cpus` needs hot add (the reboot list does not include `num_cpus`).
Method: documentation only; no commands were run.
