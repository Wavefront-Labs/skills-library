---
id: computing-software.cloud-infrastructure-engineering.ansible.debugging-the-variable-precedence-ladder
name: debugging-the-variable-precedence-ladder
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, variables-precedence, precedence-levels, variable-precedence, extra-vars]
level: advanced
status: docs-checked
description: "Work through Ansible's 22-level variable precedence ladder to explain why a value wins, with test plays that prove the order for role defaults, inventory, play and extra vars."
sources: ["Ansible variables guide, understanding variable precedence (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)", "Ansible inventory guide, how variables are merged (https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#how-variables-are-merged)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The variable precedence ladder

From lowest to highest (the Ansible variables guide's list; the last entry overrides all others):
1. command line values (e.g. `-u`; not variables)
2. role defaults (`roles/x/defaults/main.yml`)
3. inventory file or script group vars
4. inventory `group_vars/all`
5. playbook `group_vars/all`
6. inventory `group_vars/*`
7. playbook `group_vars/*`
8. inventory file or script host vars
9. inventory `host_vars/*`
10. playbook `host_vars/*`
11. host facts and cached `set_fact`
12. play `vars`
13. play `vars_prompt`
14. play `vars_files`
15. role vars (`roles/x/vars/main.yml`)
16. block vars (tasks in the block only)
17. task vars (the task only)
18. `include_vars`
19. registered vars and `set_fact`
20. role (and `include_role`) params
21. include params
22. extra vars (`-e`), which always win

Footnotes from the guide: tasks in a role see their own role's defaults, tasks outside a role see the last role's defaults; group_vars and host_vars include those added by vars plugins.

## Prove it with a probe play
```yaml
- hosts: web01
  gather_facts: false
  vars: {probe: play_vars}
  roles:
    - role: probe_role          # defaults: probe=role_default, vars: probe=role_vars
  tasks:
    - ansible.builtin.debug: {var: probe}
      vars: {probe: task_vars}
```
Add `probe` to group_vars/host_vars and move it between levels; run with and without `-e probe=extra`.

## Rules of thumb
- Overridable defaults go in role `defaults/`. Role `vars/` overrides inventory, so do not use it for values users should change.
- Environment differences go in inventory group_vars; host exceptions in host_vars.
- Emergency override: `-e`; nothing overrides extra vars, including `set_fact`.
- Inventory merge: child groups beat parent groups; groups at the same depth merge alphabetically (the last one wins) unless `ansible_group_priority` is set.
- Define each variable in one place; the guide recommends agreeing team guidelines to avoid precedence surprises.

## Gotchas
- Play `vars` (12) beat host_vars (9, 10): a play-level `vars: {port: 80}` silently ignores host-specific ports.
- `set_fact` with `cacheable: true` has level 19 during the run, but the cached copy has host-fact level (11) in later runs.
- `-e @file.yml` values are extra vars too; they override role logic that sets the same name with `set_fact`.
- Within one level, redefining a variable overrides the earlier definition; with `hash_behaviour` at its default (`replace`), dictionaries are replaced, not merged.

## Verify
- [ ] You can predict the probe output for each placement before running.

## Checked
Checked 2026-10-23 against the Ansible documentation source on GitHub (playbooks_variables.rst and intro_inventory.rst; latest ansible-core release v2.21.5): the 22-entry precedence list and its order, the footnotes, extra vars always winning, the guidance on defaults versus vars, inventory merge order and `ansible_group_priority`, and the cached `set_fact` precedence. Removed the unconfirmed phrase about the earlier list being from the "docs" and added the footnotes from the guide.
Method: documentation only; no commands were run.
