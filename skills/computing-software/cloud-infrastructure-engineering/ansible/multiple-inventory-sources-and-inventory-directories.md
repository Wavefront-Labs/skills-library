---
id: computing-software.cloud-infrastructure-engineering.ansible.multiple-inventory-sources-and-inventory-directories
name: multiple-inventory-sources-and-inventory-directories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, inventory, static-inventory, multiple-inventories, inventory-directory, inventory-sources, inventory-ignore-extensions, mixed-static-dynamic, inventory-merge, source-order, per-environment-inventory, inventory-layout]
level: practitioner
status: docs-checked
description: "Combine inventories: several -i sources, a directory mixing static files and plugin configs, load order and precedence, and keeping stray files from being parsed."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/constants.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple inventory sources and inventory directories

## 1. Several -i flags
```bash
ansible-playbook site.yml -i inventories/static.ini -i inventories/aws_ec2.yml -i 'extra.example.com,'
```
Ansible loads the sources in the order you pass them and defines hosts, groups and variables as it meets them: hosts and groups are global, so a host or group defined in two sources is one entity whose data is added to, and for a variable defined several times **the last definition wins**. With `-i staging -i production`, a variable set in both ends up with the production value; reverse the order and it flips. A source containing a comma is an inline host list (the trailing comma makes a single host valid). In `ansible.cfg`, `inventory` takes a comma-separated list (`inventory = inventories/static.ini, inventories/aws_ec2.yml`; environment variable `ANSIBLE_INVENTORY`).

## 2. A directory as the inventory
```
inventories/prod/
  01-static.yml          # hand-maintained hosts
  02-aws_ec2.yml         # plugin config (ends in aws_ec2.yml so the plugin accepts it)
  03-constructed.yml     # derived groups from the above
  group_vars/
  host_vars/
```
`-i inventories/prod` loads every file in the directory in alphabetical order (the code sorts the directory listing and recurses into subdirectories), then applies `group_vars/` and `host_vars/` next to the directory. Prefix file names with numbers: the `constructed` plugin only sees hosts and variables that earlier sources loaded, so it must sort last. Parent/child groups must also exist when a plugin expects them; the YAML and INI plugins discard empty groups at the end of each source.

Always skipped inside an inventory directory: hidden files and the `group_vars`, `host_vars` and `vars_plugins` directories, files whose name ends with an extension in `inventory_ignore_extensions`, and names matching `inventory_ignore_patterns`. The default extension list is `.pyc`, `.pyo`, `.swp`, `.bak`, `~`, `.rpm`, `.md`, `.txt`, `.rst`, `.orig`, `.cfg` and `.retry`; `.ini` is not on it. To change the lists:
```ini
[inventory]
ignore_extensions = ~, .orig, .bak, .retry, .pyc, .pyo
ignore_patterns = README.*
```
(`ignore_extensions` replaces the default list, so include everything you still want skipped; `ignore_patterns` entries are regular expressions. Environment variables: `ANSIBLE_INVENTORY_IGNORE` and `ANSIBLE_INVENTORY_IGNORE_REGEX`.)

## 3. Per-environment layout
```
inventories/
  dev/   hosts.yml  group_vars/  host_vars/
  stage/ hosts.yml  group_vars/
  prod/  hosts.yml  group_vars/
```
`-i inventories/prod`. Variables found next to the playbook override those found next to the inventory, so keep shared defaults in the playbook directory only when you want them to win, and environment values in `inventories/<env>/group_vars`.

## 4. See what was merged
```bash
ansible-inventory -i inventories/prod --graph
ansible-inventory -i inventories/prod --list --yaml
ansible-inventory -i inventories/prod --host web1     # merged vars for one host
ansible-playbook site.yml -i inventories/prod -vvv    # shows "Parsed <source> inventory source with <plugin> plugin"
```
A source that no plugin can parse gives `[WARNING]: Unable to parse <source> as an inventory source`. Set `[inventory] any_unparsed_is_failed = true` to make any such source fatal, or `unparsed_is_failed = true` to make it fatal only when nothing at all could be parsed.

## Gotchas
- `group_vars/` and `host_vars/` are looked up next to the inventory source: for `-i inventories/prod/hosts.yml` that is `inventories/prod/`.
- A YAML file without a `plugin:` key is not handled by `auto`; it falls through to the static `yaml` plugin, and plugin-style keys inside it would be read as inventory data.
- `.ini` files are **not** skipped in an inventory directory by default; `.md`, `.txt` and `.rst` files are, so documentation files there are safe.

## Verify
- [ ] `ansible-inventory -i inventories/prod --graph` shows hosts from both the static file and the plugin, and the constructed groups.
- [ ] `ansible-playbook -vvv` lists every intended file as parsed and shows no "Unable to parse" warning.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the inventory guide (multiple `-i`, last definition wins, directory load order, global hosts and groups, empty-group note) and in `inventory/manager.py` (sorted directory walk, always-ignored names), `config/base.yml` (`INVENTORY_IGNORE_EXTS` = reject list plus `.orig`, `.cfg`, `.retry`; `INVENTORY_IGNORE_PATTERNS`; `DEFAULT_HOST_LIST`; the two unparsed settings, `any_unparsed_is_failed` since 2.7) and `constants.py` (`REJECT_EXTS`). Corrected: `.ini` is not ignored by default; `unparsed_is_failed` is not fatal for a single failed source. Removed the grep pipeline.
Method: documentation only; no commands were run.
