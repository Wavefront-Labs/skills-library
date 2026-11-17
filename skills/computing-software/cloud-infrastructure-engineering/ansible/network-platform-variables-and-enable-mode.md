---
id: computing-software.cloud-infrastructure-engineering.ansible.network-platform-variables-and-enable-mode
name: network-platform-variables-and-enable-mode
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, network-automation, ansible-network-os, network-enable, network-cli, become]
level: practitioner
status: docs-checked
description: "Set ansible_network_os, connection types and platform options per device family, and enter privileged enable mode with become for Cisco IOS, NX-OS and similar."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/platform_index.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/network_best_practices_2.5.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/platform_nxos.rst", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/connection/network_cli.py", "https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/doc_fragments/connection_persistent.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network platform variables and enable mode

## Per-platform group vars
```yaml
# group_vars/ios.yml
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: cisco.ios.ios
ansible_user: netops
ansible_password: "{{ vault_netops_password }}"
ansible_become: true
ansible_become_method: enable
ansible_become_password: "{{ vault_enable_secret }}"
```
| Platform | ansible_network_os | Connections |
|---|---|---|
| Cisco IOS/IOS-XE | `cisco.ios.ios` | network_cli |
| Cisco NX-OS | `cisco.nxos.nxos` | network_cli, httpapi (NX-API) |
| Cisco IOS-XR | `cisco.iosxr.iosxr` | network_cli |
| Arista EOS | `arista.eos.eos` | network_cli, httpapi (eAPI) |
| Juniper Junos | `junipernetworks.junos.junos` | network_cli, netconf |
| VyOS | `vyos.vyos.vyos` | network_cli |

`ansible_network_os` selects the cliconf/terminal plugin that knows prompts, paging and errors; set it to the fully qualified collection name shown in the table.

## Enable mode
- `become: true` + `become_method: enable` enters privileged EXEC (`enable`, then the secret).
- Needed for config changes and many show commands on IOS; not used on platforms with role-based login (Junos, EOS with privileged user).
- `ansible_become_password` holds the enable secret, not the login password.

## Timeouts and options
```yaml
ansible_command_timeout: 60        # default 30; long show commands / commits
ansible_network_cli_ssh_type: libssh   # libssh, paramiko or auto (default)
```

`auto` uses ansible-pylibssh when installed and otherwise falls back to paramiko; the paramiko path is deprecated and slated for removal in a release after 2028-02-01, so install `ansible-pylibssh`.

## Gotchas
- Network devices do not run Python modules: use `gather_facts: false` and the platform facts modules (for example `cisco.ios.ios_facts`).
- Use the fully qualified names (`cisco.ios.ios`), not the short names used in old playbooks.

## Verify
```bash
ansible ios -m cisco.ios.ios_command -a "commands='show privilege'"     # Current privilege level is 15
```

## Checked

Checked 2026-10-26 against the Ansible network platform options page, the NX-OS and EOS platform pages and the ansible.netcommon `network_cli` plugin source (main). Confirmed: the `ansible_network_os` values and which connections each platform supports (the table lists network_cli only for IOS-XR, network_cli and httpapi for EOS and NX-OS, network_cli and netconf for Junos); `ansible_become_method: enable` in the platform examples; `ansible_command_timeout` default 30; `ssh_type` choices libssh, paramiko, auto with default auto and paramiko deprecated for removal after 2028-02-01. Removed unconfirmed claims (exact error text, AAA rate limiting, short-name deprecation, `ansible_connect_timeout`).

Method: documentation only; no commands were run.
