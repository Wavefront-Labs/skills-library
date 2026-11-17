---
id: computing-software.cloud-infrastructure-engineering.ansible.connection-defaults-in-ansible-cfg
name: connection-defaults-in-ansible-cfg
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-cfg, remote-user-default, private-key-file, inventory]
level: intro
status: docs-checked
description: "Set connection defaults in ansible.cfg (inventory, remote_user, private_key_file, timeout, host_key_checking) and know which inventory vars override them."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html", "https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connection defaults in ansible.cfg

```ini
[defaults]
inventory = ./inventory
remote_user = automation          # default SSH user
private_key_file = ~/.ssh/automation_ed25519
timeout = 30                      # connection timeout in seconds (default 10)
host_key_checking = True          # keep True in prod; disable only for throwaway labs
forks = 20                         # default 5

[privilege_escalation]
become = False                    # opt in per play
become_method = sudo
become_user = root
become_ask_pass = False
```

## Precedence (lowest to highest)
Documented precedence categories, lowest to highest: configuration settings (ansible.cfg, then environment variables) → command-line options (`-u`) → playbook keywords (play, then block/role, then task `remote_user:`) → variables (inventory or play vars such as `ansible_user`) → direct assignment. `ansible_user` beats every `remote_user:` keyword, including the task-level one, and `-e ansible_user=x` beats inventory values. So `ansible_user` in group_vars overrides `remote_user:` in the play, a common surprise.

| cfg key | env | inventory var | CLI |
|---|---|---|---|
| remote_user | ANSIBLE_REMOTE_USER | ansible_user | -u |
| private_key_file | ANSIBLE_PRIVATE_KEY_FILE | ansible_ssh_private_key_file | --private-key |
| timeout | ANSIBLE_TIMEOUT | ansible_ssh_timeout | -T |
| inventory | ANSIBLE_INVENTORY | n/a | -i |

## Gotchas
- With no `remote_user` set, the connection plugin's default applies, normally the user running Ansible.
- `inventory` takes a comma-separated list of sources (default `/etc/ansible/hosts`): `inventory = inv/prod,inv/shared`.
- The first `ansible.cfg` found wins (`ANSIBLE_CONFIG`, then `./ansible.cfg`, then `~/.ansible.cfg`, then `/etc/ansible/ansible.cfg`); files are not merged.

## Verify
- [ ] `ansible all -m ansible.builtin.ping -vvv` prints an "ESTABLISH SSH CONNECTION FOR USER" line with the expected user.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) reference_appendices/general_precedence.rst and the ansible-core devel `config/base.yml`, `cli/arguments/option_helpers.py` and `plugins/connection/ssh.py`. Confirmed: config keys and environment names, defaults (timeout 10, forks 5, host_key_checking true, inventory list), the CLI flags, the inventory variable names for the ssh plugin, the corrected precedence order (variables above keywords) and the config-file search order. Removed unconfirmed claims about `~/.ssh/config` interplay.
Method: documentation only; no commands were run.
