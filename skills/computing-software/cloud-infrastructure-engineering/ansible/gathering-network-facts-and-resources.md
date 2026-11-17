---
id: computing-software.cloud-infrastructure-engineering.ansible.gathering-network-facts-and-resources
name: gathering-network-facts-and-resources
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, network-facts, gather-network-resources, ios-facts, network-inventory]
level: practitioner
status: docs-checked
description: "Gather facts from network devices with platform facts modules or gather_facts, select gather_subset and gather_network_resources, and use the structured results for audits."
sources: ["https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_facts.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_resource_modules.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/platform_index.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gathering network facts and resources

Network devices run no Python; facts modules run on the controller over `network_cli`,
`netconf` or `httpapi`.

## Inventory basics
```yaml
switches:
  hosts: {sw1: {ansible_host: 10.0.0.11}}
  vars:
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
    ansible_user: netops
    ansible_become: true
    ansible_become_method: enable
```

## Gathering
```yaml
- hosts: switches
  gather_facts: false
  tasks:
    - name: Collect legacy + resource facts
      cisco.ios.ios_facts:
        gather_subset: [min]                   # default min; also all, default, hardware, config, interfaces; !name excludes
        gather_network_resources: [interfaces, l2_interfaces, vlans, l3_interfaces]
```
Results:
- `ansible_net_hostname`, `ansible_net_version`, `ansible_net_model`, `ansible_net_serialnum`, `ansible_net_interfaces` (legacy subsets)
- `ansible_network_resources.vlans` — a list in the **same schema** the resource module accepts (`config:`), e.g. `[{vlan_id: 10, name: users, state: active}]`.

Same keys across vendors with resource modules: `arista.eos.eos_facts`, `junipernetworks.junos.junos_facts`, `cisco.nxos.nxos_facts`.

## Uses
- Inventory/audit report:
```yaml
- ansible.builtin.copy:
    content: "{{ ansible_network_resources | to_nice_yaml }}"
    dest: "facts/{{ inventory_hostname }}.yml"
  delegate_to: localhost
```
- Seed source of truth: the gathered YAML becomes host_vars for `state: replaced/overridden` runs.
- Compliance: `assert` that `ansible_net_version` is in an approved list.

## Gotchas
- `gather_subset: all` with `config` pulls the full running config — slow on large chassis; ask only for what you need.
- `gather_network_resources` accepts only the resource names that module lists (for `ios_facts` for example `interfaces`, `l2_interfaces`, `l3_interfaces`, `vlans`, `acls`, `static_routes`); set `available_network_resources: true` to list what a platform supports.
- Use the FQCN form (`cisco.ios.ios`) for `ansible_network_os`.

## Verify
- [ ] `ansible sw1 -m cisco.ios.ios_facts -a 'gather_network_resources=vlans'` returns `ansible_network_resources.vlans`.

## Checked

Checked 2026-10-26 against the cisco.ios `ios_facts` module source (main) and the Ansible network resource module page. Confirmed: `gather_subset` values all, min, default, hardware, config and interfaces with default `min` and `!` exclusion; `gather_network_resources` valid names and `available_network_resources`; `ansible_net_hostname`, `ansible_net_version`, `ansible_net_model`, `ansible_net_serialnum` and `ansible_net_interfaces` return keys; `gather_facts: false` with network plays. Removed the `ansible_facts_modules` / `module_defaults` sentence and the running-versus-startup claim, which no page confirms.

Method: documentation only; no commands were run.
