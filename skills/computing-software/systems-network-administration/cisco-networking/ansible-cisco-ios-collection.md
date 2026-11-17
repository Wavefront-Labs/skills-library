---
id: computing-software.systems-network-administration.cisco-networking.ansible-cisco-ios-collection
name: ansible-cisco-ios-collection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, network-automation, ansible, ansible-network, cisco-ios-collection, ios-config, ios-facts, resource-modules, network-cli, ansible-check-mode, diff-mode, state-merged, state-replaced, state-overridden]
level: practitioner
status: docs-checked
description: "Manage Cisco IOS with Ansible cisco.ios: network_cli inventory, ios_facts, resource modules and their states (merged, replaced, overridden), ios_config options and --diff."
sources:
  - https://docs.ansible.com/ansible/latest/collections/cisco/ios/index.html
  - https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html
  - https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_config_module.html
  - https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_facts_module.html
  - https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_vlans_module.html
  - https://docs.ansible.com/ansible/latest/network/user_guide/platform_ios.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ansible with the cisco.ios collection

The collection index (version 11.6.0 when read) lists `ios_facts` (collect facts), `ios_config`
(manage configuration sections), `ios_vlans` (resource module for VLANs) and `ios_command` (run
commands). It requires ansible-core 2.16.0 or newer.

## Inventory and connection
The Ansible IOS platform guide gives these connection settings:
```yaml
# group_vars/ios.yml
ansible_network_os: cisco.ios.ios
ansible_connection: ansible.netcommon.network_cli
ansible_user: netops
ansible_password: "{{ vault_net_pass }}"
ansible_become: true
ansible_become_method: enable
ansible_become_password: "{{ vault_enable_pass }}"
```
`ansible_connection: local` is deprecated for network modules. Keep passwords in a vault.

## Facts
```yaml
- hosts: ios
  gather_facts: false
  tasks:
    - cisco.ios.ios_facts:
        gather_subset: [min]
        gather_network_resources: [interfaces, vlans]
```
`gather_subset` choices are `all`, `min` (the default), `default`, `hardware`, `config` and
`interfaces`; a `!` prefix excludes one. `gather_network_resources` accepts `all` or individual
resources such as `interfaces`, `vlans`, `l2_interfaces`, `l3_interfaces`, `acls`, `static_routes`,
`ntp_global` and `ospfv2`. The module works with `network_cli`. On L3 devices, unsupported
resources such as `vlans` are expected to return blank output.

## Resource modules (declarative)
```yaml
- cisco.ios.ios_vlans:
    config:
      - {vlan_id: 10, name: USERS, state: active}
      - {vlan_id: 20, name: VOICE, state: active}
    state: merged
```
`ios_vlans` `config` suboptions include `vlan_id` (required, 1-4094), `name`, `state`
(`active` or `suspend`), `shutdown` (`enabled` or `disabled`) and `remote_span`. Its `mtu` option
is deprecated in favour of `ios_interfaces`.

Top-level `state` for resource modules (`ios_vlans` default is `merged`):
- `merged`: combine the on-device configuration with the task's configuration.
- `replaced`: replace an on-device configuration subsection with the one in the task.
- `overridden`: replace the resource's on-device configuration with the task's. The Ansible guide
  warns to use caution, as you could remove your access to the device.
- `deleted`: remove the on-device subsection and reset it to defaults. (`ios_vlans` also lists `purged`.)
- `gathered`: collect resource details from the device, returned under the `gathered` key.
- `rendered`: convert the task's config into native CLI, returned under `rendered`. It does not
  communicate with the device and can be used offline.
- `parsed`: convert the `running_config` option into structured data under `parsed`. It does not
  fetch configuration from the device, so it also works offline.

## ios_config (line-based, when no resource module fits)
```yaml
- cisco.ios.ios_config:
    parents: line vty 0 15
    lines:
      - transport input ssh
    save_when: modified
```
- `parents` identifies the section; without it, commands are checked against top-level commands.
- `lines` must be the exact same commands as found in the device running-config to stay
  idempotent and give a correct diff; abbreviated commands are not idempotent.
- `save_when` choices: `always`, `never` (default), `modified`, `changed` (save only when the task made a change).
- `match`: `line` (default), `strict`, `exact`, `none`. `replace`: `line` (default) or `block`.
- `backup: true` takes a running-config backup first (default false). `defaults: true` gathers
  with `show running-config all` (default false).
- `diff_against`: `running`, `startup` or `intended` (`intended` needs `intended_config`) sets the
  comparison for `--diff` output.

## Verify
- [ ] `ansible-playbook site.yml --diff` shows only the expected lines.
- [ ] A second run reports no changes (idempotent).
- [ ] Start new resource-module plays with `merged`, not `overridden`.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the cisco.ios collection index, the `ios_config`, `ios_facts` and `ios_vlans` module pages, the Ansible network resource modules page and the IOS platform guide. Removed because the pages read do not state them: the `ansible-galaxy collection install` command, "modules run on the control node, no Python on the device", `--check` behaviour (the module pages do not document check mode), `serial: 2`, `--forks`, `ansible_command_timeout`, `ansible.netcommon.cli_command` advice, and the `save_when: modified` semantics beyond the listed choices. The `ios_vlans` example now uses documented options only.
