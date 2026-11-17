---
id: computing-software.networking-hardware-and-wireless.arista-eos.avd-ansible
name: avd-ansible
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, avd, ansible-avd, arista-validated-design, eos-designs]
level: practitioner
status: draft
description: "Generate and deploy EOS configs with AVD roles eos_designs, eos_cli_config_gen and eos_config_deploy."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Arista Validated Design (AVD) with Ansible
Goal: generate a data-center fabric from data models.

```
ansible-galaxy collection install arista.avd
ansible-galaxy collection install arista.cvp
```

```yaml
- hosts: DC1_FABRIC
  gather_facts: false
  tasks:
    - ansible.builtin.import_role:
        name: arista.avd.eos_designs
    - ansible.builtin.import_role:
        name: arista.avd.eos_cli_config_gen
    - ansible.builtin.import_role:
        name: arista.avd.eos_config_deploy_eapi
```

- Inventory group_vars hold fabric topology (spines, leaves, VLANs, tenants).
- `eos_designs` produces structured config; `eos_cli_config_gen` renders EOS CLI and docs; deploy via eAPI or CloudVision (`eos_config_deploy_cvp`).
- Pin AVD and EOS versions together (see the compatibility matrix).

Gotcha: running deploy directly without reviewing generated configs and diffs risks outages. Use `--check --diff` or a configure session with a timer first.

Operational tip: commit both the inputs (group_vars) and the generated configs to Git, so every fabric change shows up as a reviewable diff, and protect secrets with Ansible Vault. Upgrade AVD in a branch and diff the regenerated configs against production before merging, as defaults can change between AVD versions.

## Verify
- Generated files appear under `intended/configs/`, and `ansible-playbook --check --diff` shows only expected changes.
