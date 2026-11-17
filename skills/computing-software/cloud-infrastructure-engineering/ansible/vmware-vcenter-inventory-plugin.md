---
id: computing-software.cloud-infrastructure-engineering.ansible.vmware-vcenter-inventory-plugin
name: vmware-vcenter-inventory-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, vmware-inventory, vmware-vm-inventory, vcenter, community-vmware, vmware-vmware-collection, vsphere, guest-ip, vmware-tools, keyed-groups, properties, with-tags, vm-folders, esxi-inventory]
level: practitioner
status: docs-checked
description: "Build an inventory from vCenter with the vmware.vmware.vms plugin: trimmed properties, filters, groups by folder, tag and guest OS, and ansible_host from VMware Tools."
sources: ["https://github.com/ansible-collections/vmware.vmware/blob/main/plugins/inventory/vms.py", "https://github.com/ansible-collections/community.vmware/blob/main/CHANGELOG.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMware vCenter inventory plugin

The `community.vmware.vmware_vm_inventory` plugin is deprecated; its documentation points to
`vmware.vmware.vms` as the supported replacement (the collection ships a migration guide). Use that plugin.

## 1. Prerequisites on the control node / EE
- Install the `vmware.vmware` collection (`ansible-galaxy collection install vmware.vmware`) and the Python requirements listed in its documentation.
- `gather_tags: true` needs the vSphere Automation SDK.

## 2. Plugin config
```yaml
# inventories/dc1/dc1.vmware_vms.yml   (file name must end in vms.yml, vms.yaml, vmware_vms.yml or vmware_vms.yaml)
plugin: vmware.vmware.vms
hostname: vcenter.example.com
username: svc-ansible@vsphere.local
password: "{{ lookup('ansible.builtin.env', 'VMWARE_PASSWORD') }}"
validate_certs: true
gather_tags: true                   # adds tags and tags_by_category
search_paths:                       # only VMs under these vSphere folder paths
  - /DC1/vm/production
properties:                         # fetch only what you use
  - name
  - config.name
  - config.guestId
  - config.instanceUuid
  - guest.ipAddress
  - guest.hostName
  - summary.runtime.powerState
filter_expressions:                 # VMs matching an expression are filtered out
  - 'summary.runtime.powerState == "poweredOff"'
hostnames:
  - config.name
compose:
  ansible_user: "'Administrator' if 'windows' in config.guestId else 'automation'"
  ansible_connection: "'winrm' if 'windows' in config.guestId else 'ssh'"
keyed_groups:
  - key: config.guestId
    prefix: os
    separator: _
  - key: tags_by_category.keys()
    prefix: vmware_tag_category_name_
    separator: ""
group_by_paths: true
```
```bash
VMWARE_PASSWORD=... ansible-inventory -i inventories/dc1/dc1.vmware_vms.yml --graph
```

## 3. Notes
- `set_ansible_host` (default true) sets `ansible_host`; `guest.ipAddress` is the primary address reported by VMware Tools, so powered-off VMs and VMs without Tools have none.
- `gather_path` (default true) computes the folder `path` variable; it is needed for `group_by_paths` or any use of `path`.
- `gather_compute_objects: true` adds `cluster` and `esxi_host` to each VM and costs extra time.
- To pick a specific address use `compose` on `guest.net` (add `guest.net` to `properties`), as in the plugin's examples.
- When several VMs have the same hostname only the first is shown with a warning (a fatal error with `strict: true`); use `config.instanceUuid` in `hostnames` to disambiguate.

## Gotchas
- `validate_certs: false` is common in labs; never in a config that goes to the controller.

## Verify
- [ ] `ansible-inventory --graph` shows the expected OS, tag and folder groups.
- [ ] `ansible all -m ping` does not report hosts UNREACHABLE because of a missing IP.

## Checked

Checked 2026-10-26 against the vmware.vmware `vms` inventory plugin source (main) and the community.vmware changelog. Confirmed: the plugin is the supported replacement for the deprecated `community.vmware.vmware_vm_inventory`; configuration file names ending vms.yml, vms.yaml, vmware_vms.yml or vmware_vms.yaml; options `properties`, `search_paths`, `filter_expressions`, `hostnames`, `compose`, `keyed_groups`, `groups`, `group_by_paths`, `gather_tags`, `gather_path`, `gather_compute_objects`, `set_ansible_host`, `strict`; the vSphere Automation SDK requirement for tags; duplicate-hostname behaviour. The old community.vmware plugin no longer exists in the collection source, so the previous body was replaced. Removed the controller-UI and vCenter role remarks.

Method: documentation only; no commands were run.
