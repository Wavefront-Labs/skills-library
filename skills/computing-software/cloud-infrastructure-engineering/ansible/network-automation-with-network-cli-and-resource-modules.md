---
id: computing-software.cloud-infrastructure-engineering.ansible.network-automation-with-network-cli-and-resource-modules
name: network-automation-with-network-cli-and-resource-modules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, network-cli, netconf, httpapi, resource-modules, cisco-ios, cisco-iosxr, cisco-nxos, arista-eos, juniper-junos, ansible-netcommon, ansible-utils, cli-config, cli-command, gathered, parsed, rendered, overridden, merged, replaced, network-os, enable-mode, persistent-connection, config-backup, textfsm, ntc-templates, cli-parse]
level: advanced
status: docs-checked
description: "Automate switches and routers with Ansible: network_cli, netconf, httpapi, ansible_network_os, resource module states, cli_parse, config backup and diff."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/platform_index.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_resource_modules.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_debug_troubleshooting.rst", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/modules/cli_config.py", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/httpapi.py", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/netconf.py", "https://github.com/ansible-collections/ansible.utils/blob/main/plugins/modules/cli_parse.py", "https://github.com/ansible-collections/cisco.ios/blob/main/plugins/modules/ios_config.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network automation with network_cli and resource modules

**Goal:** device config declared as data, pushed idempotently with a diff, and read
back as structured facts — not `send_command` strings and regexes.

## 1. Connection and inventory
```yaml
switches:
  hosts:
    core01: {ansible_host: 10.0.0.1}
  vars:
    ansible_connection: ansible.netcommon.network_cli   # ssh CLI; netconf / httpapi for API devices
    ansible_network_os: cisco.ios.ios                   # arista.eos.eos, cisco.nxos.nxos, junipernetworks.junos.junos, cisco.iosxr.iosxr
    ansible_user: automation
    ansible_password: "{{ vault_net_pw }}"
    ansible_become: true
    ansible_become_method: enable
    ansible_become_password: "{{ vault_enable_pw }}"
    ansible_command_timeout: 60
```
Network modules run **on the control node** (no Python on the device) over a persistent
connection (`persistent_connect_timeout`, `persistent_command_timeout`). Play keywords:
`gather_facts: true` works via the platform's `*_facts` module (`gather_subset: [min]`,
`gather_network_resources: [interfaces, vlans]`). `httpapi` for NX-API/eAPI/RESTCONF needs
`ansible_httpapi_use_ssl` and `ansible_httpapi_validate_certs`; `netconf` needs `ncclient`.

## 2. Resource modules: the declarative core
Each platform collection has `<os>_interfaces`, `_l2_interfaces`, `_l3_interfaces`,
`_vlans`, `_bgp_global`, `_ospfv2`, `_acls`, `_static_routes`, ... with a `state`:
| state | effect |
|---|---|
| `merged` (default) | add/update the listed objects, leave others |
| `replaced` | listed objects become exactly as given |
| `overridden` | whole resource becomes exactly as given (deletes unlisted) |
| `deleted` | remove listed (or all) |
| `gathered` | read current config as structured data |
| `rendered` | produce CLI lines from data without connecting |
| `parsed` | turn a saved `running-config` into data (`running_config:`) |
```yaml
- cisco.ios.ios_vlans:
    config: "{{ vlans }}"          # [{vlan_id: 10, name: users}, ...]
    state: overridden
  register: r
- ansible.builtin.debug: {var: r.commands}     # exact CLI the module sent (or would send in --check)
```
`--check` reports the commands without applying them. Brownfield adoption: run `state: gathered`,
save as `host_vars`, review, then switch to `replaced`/`overridden`.

## 3. Commands, raw config, parsing
```yaml
- ansible.netcommon.cli_command: {command: show ip interface brief}
  register: out
- ansible.utils.cli_parse:
    command: show ip interface brief
    parser: {name: ansible.netcommon.ntc_templates}     # also ansible.netcommon.pyats / native, ansible.utils.textfsm / ttp
  register: parsed                 # parsed.parsed is a list of dicts
- ansible.netcommon.cli_config:
    config: "{{ lookup('template', 'banner.j2') }}"
    backup: true                   # saves running-config to backup/ before change
    diff_match: line
- cisco.ios.ios_config:
    lines: [ntp server 10.0.0.5]
    save_when: modified            # write memory only if changed
```
`cli_parse` needs `ntc-templates`/`pyats` on the control node. Prefer resource modules;
`*_config` for things without one.

## 4. Backups and compliance
```yaml
- cisco.ios.ios_config:
    backup: true
    backup_options: {dir_path: "backups/{{ inventory_hostname }}", filename: running.cfg}
- ansible.utils.fact_diff:
    before: "{{ golden.interfaces }}"
    after: "{{ ansible_network_resources.interfaces }}"
```
Commit backups to git from the playbook for a change history; `fact_diff` + `assert`
gives a compliance check in CI.

## 5. Safety for config pushes
- `serial: 1` and a `cli_command: show ... | include` post-check per device.
- `ios_config` with `diff_against: intended` and `intended_config` for intent comparison.
- Rollback: Junos `junos_config: {confirm: 5}` (commit confirmed, minutes); elsewhere keep the `backup` and test a restore path in a lab.
- Run with `ansible_command_timeout` large enough for `write memory` on big configs.

## Gotchas
- `ansible_connection: network_cli` needs `ansible_network_os` so Ansible can pick the platform plugins.
- `become` on network devices is enable mode, not sudo; wrong `become_method` hangs at the prompt.
- Resource modules are per-platform and version-sensitive; `rendered` on a lab control node shows expected CLI, but test `replaced`/`overridden` on a lab device first — `overridden` on `interfaces` can shut every unlisted port.
- Facts namespace: `ansible_net_*` and `ansible_network_resources`, not `ansible_facts.default_ipv4`.
- Jump hosts: network connections use `ansible_libssh_proxy_command` (libssh); `ansible_paramiko_proxy_command` is deprecated along with paramiko.
- Concurrency: slow device CLIs can time out at high `forks`; lower `forks` or raise `ansible_command_timeout` (default 30 s).

## Verify
- [ ] `ansible switches -m cisco.ios.ios_facts -a 'gather_network_resources=vlans'` returns `ansible_network_resources.vlans` for every device.
- [ ] A `state: overridden` run in `--check --diff` prints only the commands you expect, and the second real run reports `changed=0`.
- [ ] Backups directory contains today's running-config for each device after the play.

## Checked

Checked 2026-10-26 against the Ansible network documentation, the ansible.netcommon and ansible.utils sources and the cisco.ios `ios_config` source (main). Confirmed: connection plugins and `ansible_network_os` values; `ansible_become_method: enable`; `ansible_httpapi_use_ssl` and `ansible_httpapi_validate_certs`; `netconf` needs `ncclient`; resource module states and the `rendered` / `parsed` offline behaviour; `cli_parse` parser names (`ansible.netcommon` ntc_templates, pyats, native; `ansible.utils` textfsm, ttp); `cli_config` `backup` and `diff_match`; `ios_config` `save_when`, `diff_against` and `backup_options`; Junos `confirm`; `ansible_command_timeout` default 30 and the libssh proxy variable. Removed the unconfirmed error text, ProxyJump claim and forks numbers.

Method: documentation only; no commands were run.
