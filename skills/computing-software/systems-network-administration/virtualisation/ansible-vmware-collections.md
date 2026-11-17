---
id: computing-software.systems-network-administration.virtualisation.ansible-vmware-collections
name: ansible-vmware-collections
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ansible-vmware, ansible, community-vmware, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Automate vSphere with Ansible VMware collections: install, authentication defaults, cloning with vmware_guest, dynamic inventory and idempotency gotchas."
sources:
  - https://docs.ansible.com/projects/ansible/latest/collections/community/vmware/index.html
  - https://docs.ansible.com/projects/ansible/latest/collections/vmware/vmware_rest/index.html
  - https://docs.ansible.com/projects/ansible/latest/collections/community/vmware/vmware_guest_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ansible VMware collections

**Goal:** manage vSphere objects declaratively from Ansible.

## Collections
- `community.vmware`: broad module set over pyVmomi (VMs, hosts, networking, storage).
- `vmware.vmware_rest`: modules over the vSphere REST API.
```bash
ansible-galaxy collection install community.vmware vmware.vmware_rest
pip install pyvmomi    # plus the vSphere Automation SDK for tag modules
```

## Connection defaults
```yaml
- hosts: localhost
  gather_facts: false
  module_defaults:
    group/community.vmware.vmware:
      hostname: vcsa01.example.com
      username: "{{ vc_user }}"
      password: "{{ vc_pass }}"
      validate_certs: true
  tasks:
    - name: Clone web VM from template
      community.vmware.vmware_guest:
        name: web01
        template: tpl-rhel9
        datacenter: DC1
        cluster: CL1
        folder: /DC1/vm/web
        datastore: ds-gold
        state: poweredon
        hardware: { num_cpus: 2, memory_mb: 4096 }
        networks:
          - name: pg-web
            ip: 10.0.10.21
            netmask: 255.255.255.0
            gateway: 10.0.10.1
        customization: { hostname: web01, domain: example.com, dns_servers: [10.0.0.10] }
        wait_for_ip_address: true
```
Modules run on the control node (`hosts: localhost` or `delegate_to: localhost`), not on the ESXi host.

## Dynamic inventory
`vmware_vm_inventory` plugin (`*.vmware.yml`) builds groups from tags, folders and guest OS; use `compose` to set `ansible_host` from `guest.ipAddress`.

## Gotchas
- `vmware_guest` changes hardware only when the VM is powered off unless hot-add is enabled; idempotent runs can report changes for MAC or disk ordering differences; pin values.
- Store credentials in Ansible Vault or a secret store; never inline.
- Folder paths include the datacenter and the `vm` root.

## Verify
A second run reports `changed=0`; `community.vmware.vmware_guest_info` returns the expected config.

## Checked
2026-10-31: The `community.vmware.vmware_guest` module and its `num_cpus`, `memory_mb`, `state: poweredon`, `validate_certs` and `wait_for_ip_address` parameters, plus `vmware_guest_info`, confirmed on the collection index and the vmware_guest module documentation page; the `vmware.vmware_rest` collection and the `vmware_vm_inventory` inventory plugin confirmed on the collection index pages. Removed the unconfirmed `vmware.vmware` collection claim.
Method: documentation only; no commands were run.
