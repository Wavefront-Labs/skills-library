---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ansible-junos
name: ansible-junos
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ansible, junipernetworks.junos, playbook]
level: practitioner
status: draft
description: "Manage Junos configuration with the Juniper.junos Ansible collection and netconf connection."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ansible with Junos
Goal: idempotent config pushes with Ansible.

```
ansible-galaxy collection install junipernetworks.junos
```

```yaml
- hosts: junos
  gather_facts: false
  vars:
    ansible_connection: ansible.netcommon.netconf
    ansible_network_os: junipernetworks.junos.junos
  tasks:
    - name: set ntp
      junipernetworks.junos.junos_config:
        lines:
          - set system ntp server 192.0.2.10
        comment: ansible ntp
        confirm: 5
```

- Needs `netconf ssh` on the device and the `ncclient` and `jxmlease` Python libs.
- Use `junos_facts`, `junos_command`, and resource modules (`junos_interfaces`, `junos_ospfv2`...).
- Check mode shows the diff without committing: `ansible-playbook --check --diff`.

Gotcha: `confirm` leaves an automatic rollback unless a later task confirms; also module names changed from the older `junos_*` collection, so confirm on your version.

Operational tip: keep inventories in version control, run first with check and diff mode, and limit blast radius with --limit or serial batches. Store credentials in Ansible Vault, never in the inventory file.

## Verify
- `ansible-playbook -i inv.yml site.yml --check --diff` shows no diff on the second run.
