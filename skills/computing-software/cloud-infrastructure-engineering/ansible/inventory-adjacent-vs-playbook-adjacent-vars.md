---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-adjacent-vs-playbook-adjacent-vars
name: inventory-adjacent-vs-playbook-adjacent-vars
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, group-vars, host-vars, playbook-adjacent-vars, inventory-adjacent-vars, variable-precedence, playbook-dir]
level: practitioner
status: docs-checked
description: "Decide where group_vars and host_vars live: next to the inventory or next to the playbook, how their precedence differs, and how ad hoc commands and ansible-inventory see them."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_variables.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/vars/host_group_vars.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inventory-adjacent vs playbook-adjacent vars

The `host_group_vars` plugin searches for `group_vars/` and `host_vars/` in two places:
1. Next to each **inventory source** (`inventories/prod/group_vars/`).
2. Next to the **playbook** being run (`playbooks/group_vars/`). Commands without a playbook (`ansible`, `ansible-console`, `ansible-inventory`) use the `--playbook-dir` option instead.

## Precedence (from the official list, lowest to highest, inventory-related entries)
1. Inventory file or script group vars
2. Inventory `group_vars/all`
3. Playbook `group_vars/all`
4. Inventory `group_vars/*`
5. Playbook `group_vars/*`
6. Inventory file or script host vars
7. Inventory `host_vars/*`
8. Playbook `host_vars/*`

(Role defaults rank below these; host facts, play vars, role vars, task vars, `include_vars`, registered vars, and finally extra vars rank above them.) So playbook-adjacent beats inventory-adjacent at the same level, and `group_vars/<group>` beats `group_vars/all`. Within the inventory, `all` is overridden by a parent group, a parent by its child, and a group by a host. Matching groups at the same level merge alphabetically (the last one wins) unless `ansible_group_priority` (set in the inventory source, not in `group_vars/`; default 1) says otherwise.

## Which to use
- **Inventory-adjacent**: data that describes the environment: IPs, sizes, credentials, per-environment endpoints. One inventory directory per environment keeps production values away from staging by construction.
- **Playbook-adjacent**: behaviour shared across every environment for that playbook set. Keep it small, because it silently overrides inventory values of the same name.

Typical layout:
```
inventories/
  prod/{hosts.yml,group_vars/,host_vars/}
  stage/{hosts.yml,group_vars/,host_vars/}
playbooks/
  site.yml
  group_vars/all/defaults.yml   # rarely needed; prefer role defaults
```

## Ad hoc and inventory tooling
`ansible` and `ansible-inventory` do not know your playbook, so they miss playbook-adjacent vars unless told:
```bash
ansible-inventory -i inventories/prod --playbook-dir playbooks --host web1
ansible web -i inventories/prod --playbook-dir playbooks -m debug -a var=pkg_list
```
Set `playbook_dir` under `[defaults]` in `ansible.cfg` (or `ANSIBLE_PLAYBOOK_DIR`) to make it the default for these commands.

## Gotchas
- The plugin looks relative to the playbook file you run, so a playbook in a subdirectory (`playbooks/app/deploy.yml`) uses `playbooks/app/group_vars`.
- A key defined in both places: the playbook-adjacent copy wins even for the production inventory, so a value meant for staging can reach production. Keep one definition per key.

## Verify
- [ ] `ansible-inventory --playbook-dir ... --host X` shows the value you expect; without `--playbook-dir` it shows the inventory value.
- [ ] No variable is defined in both trees.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed against the "Understanding variable precedence" list in Using variables, the inventory guide ("Organizing host and group variables", `ansible_group_priority`, parent/child merge), the `host_group_vars` plugin and `PLAYBOOK_DIR` in `config/base.yml`. Removed the numbered precedence labels (the official list is not numbered that way), the AWX remark and the claim about imported playbooks, none of which the documentation confirms.
Method: documentation only; no commands were run.
