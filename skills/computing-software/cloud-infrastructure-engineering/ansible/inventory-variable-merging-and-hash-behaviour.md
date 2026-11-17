---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-variable-merging-and-hash-behaviour
name: inventory-variable-merging-and-hash-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, inventory, inventory-variables, variable-merging, hash-behaviour, hash-behavior, ansible-group-priority, group-depth, parent-child-groups, variable-precedence, combine, merge-dicts, group-vars, deep-merge]
level: practitioner
status: docs-checked
description: "Predict which group's value wins (child beats parent, then alphabetical, then ansible_group_priority) and merge dicts with combine instead of hash_behaviour=merge."
sources: ["Ansible inventory guide, how variables are merged (https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#how-variables-are-merged)", "Ansible variables guide, variable precedence (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence)", "Ansible configuration reference, DEFAULT_HASH_BEHAVIOUR (https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-hash-behaviour)", "Ansible filters guide, combine (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inventory variable merging and hash_behaviour

## 1. The order Ansible flattens group variables
Before a play runs, Ansible merges and flattens variables to the specific host. For inventory entities the order, lowest to highest, is: the `all` group, parent groups, child groups, then the host. Groups at the same parent/child level merge in alphabetical order, so the last group loaded wins. `ansible_group_priority` overrides the alphabetical order for groups of the same level: the larger the number, the later the group merges and the higher its priority. It defaults to `1`.
```yaml
all:
  children:
    linux:
      vars: {ntp_server: ntp.corp}
      children:
        web:
          vars: {ntp_server: ntp.web}     # child of linux, wins over linux
        legacy:
          vars: {ntp_server: ntp.old, ansible_group_priority: 10}
```
A host in both `web` and `legacy` (same depth) would get `ntp.web` alphabetically (`web` after `legacy`), but `ansible_group_priority: 10` makes `legacy` win, giving `ntp.old`.

You can set `ansible_group_priority` only in an inventory source, not in `group_vars/`; Ansible reads it when it loads the `group_vars/` directory.

Inspect the result: `ansible-inventory --host web1` or `ansible web1 -m debug -a var=ntp_server`.

## 2. Several inventory sources
When you pass several sources, variables merge in the order you pass them: with `[all:vars]` `myvar = 1` in staging and `myvar = 2` in production, `-i staging -i production` gives 2 and `-i production -i staging` gives 1. Sources in one directory merge in alphabetical filename order, so prefixes such as `01-`, `02-` control load order.

## 3. Dicts are replaced, not merged
```yaml
# group_vars/all.yml
app: {port: 8080, workers: 4, log_level: info}
# group_vars/web.yml
app: {port: 80}
```
Result for a web host: `app == {port: 80}`; `workers` and `log_level` are gone. This is `hash_behaviour = replace`, the default. The `merge` setting still exists, but the configuration reference warns that changing it is fragile, makes content non-portable and is not recommended; the project advises avoiding `merge` for new projects and intends to deprecate and remove it eventually.

Merge deliberately instead:
```yaml
# group_vars/all.yml
app_defaults: {port: 8080, workers: 4, log_level: info}
# group_vars/web.yml
app_overrides: {port: 80}
# anywhere it is used
app: "{{ app_defaults | combine(app_overrides | default({}), recursive=true) }}"
```
Or flatten to scalar keys (`app_port`, `app_workers`) so normal precedence works per key.
`combine(..., recursive=true)` merges nested dicts and does not depend on `hash_behaviour`. `list_merge` accepts `replace` (default), `keep`, `append`, `prepend`, `append_rp` and `prepend_rp` for lists inside the hashes.

## 4. Lists
`hash_behaviour` does not affect lists. To accumulate (for example packages from several groups), name them per group and concatenate: `packages: "{{ base_packages + (web_packages | default([])) }}"`.

## Gotchas
- Alphabetical tie-break is a common surprise when a group is renamed; set `ansible_group_priority` whenever two same-level groups define the same key.
- `host_vars` override group vars, so an old `host_vars/web1.yml` can silently pin a value.
- Play `vars:` and `-e` rank above all inventory variables; extra vars always win.

## Verify
- [ ] `ansible-inventory --host <host>` shows the value you predicted from the group tree.
- [ ] Removing `ansible_group_priority` flips the value to the alphabetical winner.

## Checked
Checked 2026-10-23 against the Ansible documentation source and ansible-core config/base.yml on GitHub (intro_inventory.rst, playbooks_variables.rst, playbooks_filters.rst; latest ansible-core release v2.21.5): merge order, alphabetical rule, `ansible_group_priority` semantics and default, multiple-source ordering, `hash_behaviour` default and the status of `merge`, `combine` options (`recursive`, `list_merge` values). Wrong claims fixed: `ansible_group_priority` works only in an inventory source, not in `group_vars/` (the skill said it also worked there); `hash_behaviour = merge` was stated as deprecated in 2.10 and removed, but it is still a documented setting that is discouraged. Removed the unconfirmed group-under-two-parents and `constructed` compose claims and the `jq` check.
Method: documentation only; no commands were run.
