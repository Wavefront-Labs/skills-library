---
id: computing-software.networking-hardware-and-wireless.arista-eos.ansible-eos-modules
name: ansible-eos-modules
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, ansible, arista.eos, eos_config, eos_facts]
level: practitioner
status: draft
description: "Use the arista.eos collection for facts, commands and idempotent configuration over eAPI or network_cli."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ansible arista.eos collection
Goal: run ad-hoc and playbook automation on EOS.

```yaml
- hosts: eos
  gather_facts: false
  vars:
    ansible_connection: ansible.netcommon.httpapi
    ansible_network_os: arista.eos.eos
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_become: true
    ansible_become_method: enable
  tasks:
    - arista.eos.eos_config:
        lines: [ "ntp server vrf MGMT 192.0.2.10" ]
        save_when: modified
    - arista.eos.eos_command:
        commands: [ "show version" ]
```

- `eos_facts`, `eos_vlans`, `eos_interfaces`, `eos_bgp_global` are resource modules.
- Use `ansible_connection=network_cli` for SSH instead of httpapi.
- `eos_config` can use `match` and `replace` parameters.

Gotcha: `validate_certs: false` is lab-only. `become: enable` is required for config commands, else tasks fail with authorization errors.

Operational tip: gather facts only when needed, use `--limit` to stage rollouts, and pair tasks with `save_when: modified` so reload-safe configs persist across restarts. Test idempotency in a lab by running the playbook twice and requiring zero changes on the second run, which catches unstable line ordering.

## Verify
- Second run reports `changed=0`; `show running-config | include ntp` shows the line.
