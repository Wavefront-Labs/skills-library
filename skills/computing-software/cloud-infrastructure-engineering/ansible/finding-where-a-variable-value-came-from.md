---
id: computing-software.cloud-infrastructure-engineering.ansible.finding-where-a-variable-value-came-from
name: finding-where-a-variable-value-came-from
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, group-host-vars, variable-origin, variable-precedence, debugging]
level: practitioner
status: docs-checked
description: "Trace which inventory file, group_vars, role default or extra var set a variable's effective value, using ansible-inventory, debug and verbosity."
sources: ["Ansible variables guide, variable precedence (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)", "ansible-inventory CLI (https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html)", "Ansible inventory guide, how variables are merged (https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#how-variables-are-merged)", "ansible.builtin.debug (https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Where did this variable value come from?

Narrow it down layer by layer, using the precedence list as the map.

## 1. Inventory layer (inventory files, group_vars, host_vars)
```bash
ansible-inventory -i inventory --host web01
ansible-inventory -i inventory --graph --vars       # --vars is honoured only together with --graph
```
`--graph --vars` prints vars under the group or host that defines them, so you can see whether `all`, a group or the host set the value. To find the defining file, search the tree:
```bash
grep -rn 'ntp_server:' inventory/ group_vars/ host_vars/ playbooks/group_vars/
```

## 2. Play and role layer
```bash
grep -rn 'ntp_server' roles/*/defaults roles/*/vars playbooks/ --include='*.yml'
```
Role `vars/main.yml` overrides inventory vars; role `defaults/main.yml` is lower than every inventory source and play-level variable.

## 3. Runtime value
```yaml
- ansible.builtin.debug:
    var: ntp_server
- ansible.builtin.debug:
    msg: "{{ hostvars[inventory_hostname]['ntp_server'] }}"
```
Place the `debug` at several points in the play. If the value changes between two tasks, something between them changed it: `set_fact`, a registered variable or `include_vars` (levels 18 and 19). Extra vars (`-e`) rank above everything, so a value that equals your `-e` probe means no higher layer exists.

## 4. Group merge order
Same variable in two groups at the same depth: groups merge alphabetically and the last wins unless `ansible_group_priority` is set (inventory source only); child groups beat parents.

## Debug checklist
| Suspect | Check |
|---|---|
| host alias mismatch | the `host_vars/` file name must match the inventory host name |
| playbook-adjacent group_vars | the `group_vars` directory next to the playbook (levels 5, 7, 10) |
| role vars | `roles/*/vars/main.yml` |
| include_vars / set_fact | search the tasks for the variable name |
| extra vars in CI | the CI job's `-e` arguments |

## Verify
- [ ] You can name the exact file and precedence level that wins for the variable.

## Checked
Checked 2026-10-23 against the Ansible documentation source and ansible-core source on GitHub (playbooks_variables.rst, intro_inventory.rst, cli/inventory.py; latest ansible-core release v2.21.5): the precedence levels cited, `ansible-inventory --host`, `--graph` and the `--vars` flag (ignored unless used with `--graph`), the group merge order and `ansible_group_priority` location. Wrong claim fixed: the skill said a value still differing under `-e` pointed to `set_fact`, but extra vars rank above `set_fact`. Removed the unconfirmed statement that Ansible has no way to show variable origin, the `jq` pipeline, `ls $(dirname ...)` shell trick and the colon in the `grep -B3` pipe.
Method: documentation only; no commands were run.
