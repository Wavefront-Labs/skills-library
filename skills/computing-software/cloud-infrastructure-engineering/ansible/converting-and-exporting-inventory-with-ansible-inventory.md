---
id: computing-software.cloud-infrastructure-engineering.ansible.converting-and-exporting-inventory-with-ansible-inventory
name: converting-and-exporting-inventory-with-ansible-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, static-inventory, ini-to-yaml, inventory-export, inventory-validation, ansible-inventory]
level: practitioner
status: docs-checked
description: "Convert INI inventory to YAML, flatten and export merged inventory with ansible-inventory --list --export -y, and validate it in CI."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/cli/inventory.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting and exporting inventory

## INI to YAML
```bash
ansible-inventory -i hosts.ini --list -y --export > hosts.yml
```
- `-y` (`--yaml`) selects YAML output instead of the default JSON (ignored for `--graph`).
- `--export`, used with `--list`, represents the inventory in a way "optimized for export, not as an accurate representation of how Ansible has processed it": in the code, host entries then carry only the variables defined directly on the host and group variables are placed under their groups. Without `--export`, variables are flattened onto every host: good for debugging, bad as a source file. The `[inventory] export` setting (`ANSIBLE_INVENTORY_EXPORT`) makes export the default.
- `--toml` writes TOML; it needs the `tomli-w` Python library on the control node.
- `--output FILE` (with `--list`) writes to a file instead of the screen.
Review the result before committing: it is generated data, so comments from the original file are not carried over, and variables loaded from `group_vars/` and `host_vars/` files (vars plugins are always loaded) appear in the output; move them out or strip them before you commit a converted file.

## Validate in CI
```bash
ansible-inventory -i inventories/prod --list > /dev/null      # parse and dump
ansible-inventory -i inventories/prod --graph                 # tree of groups
ansible-inventory -i inventories/prod --host web01            # merged vars for one host
ANSIBLE_INVENTORY_ANY_UNPARSED_FAILED=true ansible-inventory -i inventories/prod --list > /dev/null
```
A source that no plugin can parse is only a warning ("Unable to parse ... as an inventory source") by default. `any_unparsed_is_failed = true` (`[inventory]`, env `ANSIBLE_INVENTORY_ANY_UNPARSED_FAILED`) makes any unparsable source fatal; `unparsed_is_failed = true` (env `ANSIBLE_INVENTORY_UNPARSED_FAILED`) is fatal only when no source at all could be parsed. Set one in CI so a typo does not silently produce an empty inventory.

## Useful flags
One action is required: `--list`, `--host HOST` or `--graph [GROUP]`.
| Flag | Use |
|---|---|
| `--graph [GROUP] --vars` | tree, including variables (`--vars` only works with `--graph`) |
| `--playbook-dir DIR` | resolve playbook-adjacent `group_vars/` and `host_vars/` |
| `--vault-id`, `--ask-vault-pass` and the other vault options | supply vault credentials for vaulted variables |
| `--output FILE` | write `--list` output to a file |
| `--limit PATTERN` | restrict `--list` output; the CLI help says `--host` and `--graph` ignore it |

## Gotchas
- Dynamic inventory plugins are queried live; capture a snapshot with `--list --export -y` when you need a reproducible diff.

## Verify
- [ ] The `--graph` output of the converted YAML file matches the `--graph` output of the original INI file.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5). Confirmed in `lib/ansible/cli/inventory.py` (options and help text, `--export` behaviour, `tomli-w` requirement, vault options, `--limit` notes) and `config/base.yml` (`INVENTORY_EXPORT`, `INVENTORY_UNPARSED_IS_FAILED`, `INVENTORY_ANY_UNPARSED_IS_FAILED`) and `inventory/manager.py` (warning text). Corrected: `--toml` needs `tomli-w` (not `toml`); the unparsed settings differ as above; the "core 2.13+" limit gate is removed because the source shows `--limit` is applied for `--list`.
Method: documentation only; no commands were run.
