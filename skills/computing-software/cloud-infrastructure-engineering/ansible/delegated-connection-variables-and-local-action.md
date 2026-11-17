---
id: computing-software.cloud-infrastructure-engineering.ansible.delegated-connection-variables-and-local-action
name: delegated-connection-variables-and-local-action
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, delegation, delegate-connection, local-action-syntax, local-action]
level: practitioner
status: docs-checked
description: "Know which connection variables apply when delegating, and when to use local_action, delegate_to localhost or connection local, including interpreter and become pitfalls."
sources: ["Controlling where tasks run: delegation and local actions (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_delegation.html)", "Implicit localhost (https://docs.ansible.com/ansible/latest/inventory_guide/implicit_localhost.html)", "Special variables (https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)", "ansible-lint rule deprecated-local-action (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/deprecated_local_action.md)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Delegated connection variables and local_action

## Which vars apply to a delegated task?
For `delegate_to: lb01` the connection variables such as `ansible_host` describe the delegated host, not `inventory_hostname`, and the execution interpreter, `connection`, `become` and `shell` plugin options are templated using values from the delegated-to host. `inventory_hostname` remains that of the **current** host, and the delegated host does not inherit variables from the host that delegates.

Traps:
- Keep connection settings in inventory (host or group vars of the delegated host), where the delegated host's own values are found.
- Delegating to a host **not** in inventory does not add it to inventory; such a host inherits variables from the `all` group only and "might cause issues" per the docs. If you must, use `add_host` first.
- Facts gathered by a delegated task are assigned to the current host unless you set `delegate_facts: true`.

## Three ways to run on the controller
```yaml
- name: Delegate to localhost
  ansible.builtin.command: ./scripts/register.sh {{ inventory_hostname }}
  delegate_to: localhost

- name: local_action shorthand (legacy)
  local_action:
    module: ansible.builtin.command
    cmd: ./scripts/register.sh {{ inventory_hostname }}

- hosts: localhost
  connection: local
  gather_facts: false
  tasks: [...]
```
Prefer `delegate_to: localhost` over `local_action`: ansible-lint flags `local_action` with its `deprecated-local-action` rule.

## Implicit vs explicit localhost
- Not in inventory: Ansible creates an implicit localhost with `ansible_connection: local` and `ansible_python_interpreter: "{{ ansible_playbook_python }}"`. It is not targetable by group, but uses `host_vars` and the `all` group's vars, and does not appear in `hostvars` unless requested.
- A `localhost` entry in inventory overrides the implicit one: all implicit behaviour is ignored and it is treated like any other host, so set `ansible_connection: local` and `ansible_python_interpreter: "{{ ansible_playbook_python }}"` yourself. With `connection: local` and no `ansible_python_interpreter`, modules run under `/usr/bin/python`, not `ansible_playbook_python`.

## become
Under delegation the `become` plugin options are templated from the delegated-to host. If a play-level `become: true` should not escalate on the controller, set `become: false` on the local tasks.

## Verify
```bash
ansible-playbook p.yml -vvv | grep -E 'ESTABLISH (LOCAL|SSH) CONNECTION'
```

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21).
- Confirmed in the delegation page: connection variables and the interpreter, connection, become and shell plugin options come from the delegated-to host; the delegated host does not inherit variables from the delegating host; a non-inventory delegate inherits only `all` group vars and is not added to inventory; `delegate_facts`; the `connection: local` interpreter caveat.
- Confirmed in the implicit localhost page: the implicit host's variables, that it is not targetable by group, and that an inventory entry overrides it.
- Removed: `ansible_delegated_vars` (not documented anywhere in the special variables page) and the claim that play vars leak into delegated connections (not documented).

Method: documentation only; no commands were run.
