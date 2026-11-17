---
id: computing-software.cloud-infrastructure-engineering.ansible.per-host-connection-variables
name: per-host-connection-variables
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, connection-plugins, ansible-ssh-private-key-file, behavioral-parameters, inventory-variables]
level: intro
status: docs-checked
description: "Set per-host and per-group connection variables: ansible_host, ansible_user, ansible_ssh_private_key_file, ansible_port, ansible_connection and password vars."
sources: ["Connecting to hosts: behavioral inventory parameters (https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters)", "Controlling how Ansible behaves: precedence rules (https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html)", "Tips and tricks, keeping vaulted variables visible (https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)", "FAQ, ProxyCommand through a gateway (https://docs.ansible.com/ansible/latest/reference_appendices/faq.html)", "community.docker connection plugin source (https://github.com/ansible-collections/community.docker/blob/main/plugins/connection/docker.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-host connection variables

```yaml
# inventory/hosts.yml
all:
  children:
    legacy:
      hosts:
        old-db01:
          ansible_host: 10.0.4.17
          ansible_port: 2222
          ansible_user: admin
          ansible_ssh_private_key_file: ~/.ssh/legacy_rsa
    containers:
      hosts:
        build01:
          ansible_connection: community.docker.docker
          ansible_docker_extra_args: ''
```
```yaml
# group_vars/legacy.yml
ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q user@gateway.example.com"'
```

## Common variables
| Variable | Purpose |
|---|---|
| `ansible_host` | resolvable name or IP to connect to when it differs from the inventory alias; never make it depend on `inventory_hostname` |
| `ansible_port` | SSH port |
| `ansible_user` | login user |
| `ansible_ssh_private_key_file` | private key file for the ssh plugin (useful with several keys when you do not want the agent) |
| `ansible_ssh_common_args` | appended to the default `ssh`, `scp` and `sftp` command lines (for example a `ProxyCommand`) |
| `ansible_password` | password to authenticate to the host (always vault it; the ssh plugin uses `sshpass` for password auth) |
| `ansible_connection` | name of any connection plugin: `ssh` (default), `paramiko`, `local`, `winrm`, `psrp`, `community.docker.docker`, `network_cli` ... |
| `ansible_become_password` | sudo password (vault it) |
| `ansible_python_interpreter` | target Python |

## Precedence
From lowest to highest: configuration settings, command-line options, playbook keywords (such as `remote_user`), variables (including these inventory variables), and direct assignment. Extra vars (`-e ansible_user=x`) are variables that beat every other source, which is useful for break-glass runs. Command-line options such as `-u` therefore do **not** override `ansible_user` set in inventory.

## Secrets
Put `ansible_password`/`ansible_become_password` in `group_vars/<group>/vault.yml` encrypted, referenced from `vars.yml`: `ansible_become_password: "{{ vault_become_password }}"`.

## Gotchas
- Ansible cannot pass an ssh key passphrase interactively with the ssh plugin; the docs recommend `ssh-agent` for passphrase-protected keys.
- The docs recommend vaulting `ansible_password` and `ansible_become_password`.

## Verify
```bash
ansible-inventory --host old-db01            # shows merged vars
ansible old-db01 -m ansible.builtin.ping -vvv   # the output shows the connection actually used
```

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and community.docker main.
- Confirmed in the behavioral parameters page: `ansible_connection` (any connection plugin, default `ssh`), `ansible_host`, `ansible_port`, `ansible_user`, `ansible_password`, `ansible_ssh_private_key_file`, `ansible_ssh_common_args`, `ansible_become_password`; the ProxyCommand form of `ansible_ssh_common_args` from the FAQ; `ansible_docker_extra_args` is the variable for the community.docker connection option `docker_extra_args`.
- Confirmed in the precedence page: configuration, then CLI options, then keywords, then variables, then direct assignment; extra vars override all.
- Removed as unconfirmed: the legacy-RSA ssh option example, the Python 3.9 interpreter path, key-path expansion remarks and the IdentitiesOnly advice.

Method: documentation only; no commands were run.
