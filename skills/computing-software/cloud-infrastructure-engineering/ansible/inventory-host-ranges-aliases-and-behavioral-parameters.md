---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-host-ranges-aliases-and-behavioral-parameters
name: inventory-host-ranges-aliases-and-behavioral-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, inventory, static-inventory, host-ranges, numeric-ranges, alpha-ranges, host-alias, inventory-alias, behavioral-parameters, ansible-host, ansible-port, ansible-user, ansible-connection, ansible-python-interpreter, ini-inventory, yaml-inventory, non-standard-port]
level: practitioner
status: docs-checked
description: "Write compact static inventories: numeric/alpha host ranges, aliases mapped to ansible_host and non-standard ports, and per-host behavioral parameters."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/implicit_localhost.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/connection/winrm.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inventory host ranges, aliases and behavioral parameters

## 1. Ranges
The INI and YAML inventory plugins support ranges. Ranges are inclusive, and leading zeros are optional.
```ini
[web]
web[01:20].example.com        # web01 .. web20
web[1:20].example.com         # web1 .. web20
[db]
db-[a:f].example.com          # alphabetic range: db-a .. db-f
[cache]
cache[01:20:2].example.com    # stride of 2: cache01, cache03, ... cache19
```
YAML:
```yaml
web:
  hosts:
    web[01:20].example.com:
```
Ranges expand when the inventory is parsed; `ansible-inventory --graph` shows the expanded hosts. Hosts and groups are global: defining one again under another group or source adds to it or overwrites conflicting information with the latest definition.

## 2. Aliases and non-standard ports
```ini
[jump]
bastion  ansible_host=203.0.113.10 ansible_port=2222 ansible_user=ops
[vm]
app-prod ansible_host=10.1.2.3
app-test ansible_host=10.1.2.3 ansible_port=2200   # same machine, different port
```
`inventory_hostname` is the alias (`bastion`), used in patterns, `--limit`, `hostvars`, `delegate_to` and log lines; `ansible_host` is what Ansible connects to. A port can also be given after the host name (`badwolf.example.com:5309`), but `ansible_port` is easier to read.
Two aliases pointing at one machine are two hosts to Ansible; the documentation warns that tasks can run in parallel against them. Never set `ansible_host` to something that depends on `inventory_hostname`.

## 3. Behavioral parameters (set per host, per group, or in `group_vars`)
| Variable | Default / note |
|---|---|
| `ansible_host` | the resolvable name or IP to connect to, when different from the alias |
| `ansible_port` | 22 for ssh |
| `ansible_user` | the user to log in as |
| `ansible_password` | never store in plain text; use a vault |
| `ansible_connection` | `ssh` by default; any connection plugin name, for example `local`, `winrm`, `psrp`, `ansible.netcommon.network_cli`, `community.docker.docker` |
| `ansible_ssh_private_key_file` | key file when you use several keys and not the SSH agent |
| `ansible_ssh_common_args` | appended to the `sftp`, `scp` and `ssh` command lines, for example to configure a `ProxyCommand` |
| `ansible_python_interpreter` | `auto` discovery by default (`auto_silent` suppresses the fallback warning), or a path such as `/usr/local/bin/python` |
| `ansible_shell_type` | `sh`-style syntax by default; only change it together with `ansible_shell_executable`, for a `csh` or `fish` shell |
| `ansible_become`, `ansible_become_method`, `ansible_become_user`, `ansible_become_password` | privilege escalation |
```ini
[win]
dc01 ansible_host=10.2.0.5
[win:vars]
ansible_connection=winrm
ansible_winrm_transport=kerberos

[bsd]
freebsd_host ansible_python_interpreter=/usr/local/bin/python
```
Group `:vars` apply to every member. Precedence runs parent group, then child group, then host: a host line value overrides the group value and a child group overrides its parent; `host_vars/` files override values on the inventory host line.

## Gotchas
- A range with mismatched padding (`[1:20]` for hosts actually named `web01`) produces names that do not resolve; check `ansible-inventory --list` before blaming DNS.
- On an INI host line a value is parsed as a Python literal (string, number, tuple, list, dict, boolean or None); in a `:vars` section it is always a string. Use a filter (`| int`, `| bool`) where the type matters, or use a YAML inventory.
- `localhost` defined in inventory is an ordinary host: without `ansible_connection=local` Ansible connects to it like any other. Without a definition, Ansible creates an implicit localhost with `ansible_connection: local`.

## Verify
- [ ] `ansible-inventory --graph web` lists exactly the expanded range.
- [ ] `ansible-inventory --host app-test` shows `ansible_port: 2200` and `ansible_host: 10.1.2.3`.
- [ ] `ansible bastion -m ping -vvv` shows the host, port and user you set.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the How to build your inventory page (ranges, stride, inclusive ranges, aliases, `host:port`, INI literal versus `:vars` string typing, behavioral parameter descriptions and defaults, precedence of parent, child and host), the Implicit localhost page, `INTERPRETER_PYTHON` in `config/base.yml`, the winrm connection plugin (`ansible_winrm_transport`, `kerberos`), and the connection plugin listings of ansible-core, community.docker and ansible.netcommon. Removed unconfirmed stride version gate, multi-range IP example, `powershell` shell type, bogus-host INI behaviour and the `serial` remark.
Method: documentation only; no commands were run.
