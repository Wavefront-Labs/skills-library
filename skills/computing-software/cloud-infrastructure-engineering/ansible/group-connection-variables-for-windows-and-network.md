---
id: computing-software.cloud-infrastructure-engineering.ansible.group-connection-variables-for-windows-and-network
name: group-connection-variables-for-windows-and-network
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, static-inventory, group-connection-vars, windows, network-automation]
level: practitioner
status: docs-checked
description: "Group hosts by connection type and set group-level connection variables for Windows (winrm/psrp/ssh) and network devices (network_cli, httpapi, netconf)."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/network/user_guide/platform_index.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/os_guide/windows_winrm.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/os_guide/windows_ssh.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/connection/winrm.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Group-level connection variables

Mixed estates fail when every host inherits SSH defaults. Make the connection type a group concern.

```yaml
# inventory/hosts.yml
all:
  children:
    linux:
      hosts: {web01: , db01: }
    windows:
      hosts: {win01: , win02: }
    ios:
      hosts: {core-sw1: , core-sw2: }
    eos:
      hosts: {leaf1: }
```
```yaml
# group_vars/windows.yml
ansible_connection: winrm          # or ansible.windows.psrp, or ssh with ansible_shell_type: powershell
ansible_port: 5986
ansible_winrm_transport: kerberos
ansible_winrm_server_cert_validation: validate
ansible_user: svc-ansible@CORP.EXAMPLE.COM
```
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
```yaml
# group_vars/eos.yml
ansible_connection: ansible.netcommon.httpapi
ansible_network_os: arista.eos.eos
ansible_httpapi_use_ssl: true
ansible_httpapi_validate_certs: true
```

## Play design
- Network plays: `gather_facts: false` and use the platform facts modules; switches do not run the Python `setup` module.
- Keep `ansible_python_interpreter` only on `linux` group.
- Use `ansible_network_os` in full FQCN form (`cisco.ios.ios`).

## Gotchas
- A host in both `linux` and `windows` (misgrouped) gets group variables merged in alphabetical group order, the last one winning; set `ansible_group_priority` or fix the grouping.
- `become: true` at play level on a mixed play also applies to Windows hosts, where `sudo` does not exist: scope become per play.

## Verify
```bash
ansible windows -m ansible.windows.win_ping
ansible ios -m cisco.ios.ios_command -a 'commands="show version"'
```

## Checked

Checked 2026-10-26 against the Ansible documentation repository (devel) and the `winrm` connection plugin source. Confirmed: WinRM through the `winrm` and `psrp` plugins, default port 5986, `server_cert_validation` default `validate`, and the `transport` option; Windows over SSH needs `ansible_connection: ssh` and `ansible_shell_type: powershell` or `cmd`; network connection settings and `ansible_network_os` values; `ansible_group_priority` overriding the alphabetical merge order of same-level groups; `ansible_httpapi_use_ssl` and `ansible_httpapi_validate_certs`. Removed the unconfirmed claims about short-name deprecation and `setup` failing on switches' exact behaviour.

Method: documentation only; no commands were run.
