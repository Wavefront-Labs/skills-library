---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-group-vars-sections-and-vars-blocks
name: inventory-group-vars-sections-and-vars-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, static-inventory, group-vars-section, inventory-vars-block, ini-inventory, yaml-inventory]
level: intro
status: docs-checked
description: "Define variables inside inventory files with INI [group:vars] sections and YAML vars blocks, including typing rules and when to move them to group_vars."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/inventory_guide/intro_inventory.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_variables.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/filter/core.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables inside inventory files

## INI
```ini
[web]
web01 http_port=8080
web02

[db]
db01

[app:children]
web
db

[web:vars]
ntp_server=ntp.example.com
max_clients=200
enable_tls=true

[all:vars]
ansible_user=automation
```

## YAML equivalent
```yaml
all:
  vars:
    ansible_user: automation
  children:
    app:
      children:
        web:
          hosts:
            web01: {http_port: 8080}
            web02:
          vars:
            ntp_server: ntp.example.com
            max_clients: 200
            enable_tls: true
        db:
          hosts:
            db01:
```

## Typing rules (the INI trap)
- A value on an INI **host line** (`web01 http_port=8080`) is interpreted as a Python literal (string, number, tuple, list, dict, boolean or None), so `8080` is an int and `True` is a boolean. Quote values that contain spaces.
- A value in a `[group:vars]` section is always a **string**: `max_clients=200` is `"200"`, and the documentation's example is that `var=FALSE` creates the string `'FALSE'`. A `:vars` section accepts one entry per line, and everything after the first `=` is the value.
- So `when: enable_tls == true` fails for a `:vars` value. Convert with a filter (`| bool`, `| int`) in the task, or use a YAML inventory, where the YAML plugin processes values consistently and keeps real types. The documentation advises not to rely on types set in INI inventories.

## When to move vars out
Inventory-file vars are fine for a handful of connection settings. Larger sets belong in `group_vars/<group>` and `host_vars/<host>` files beside the inventory: diffable, vault-able, one file per scope (and, unlike the inventory file, they can hold lists and hashes). In the precedence list, inventory-file group vars rank below `group_vars/all` files, which rank below `group_vars/<group>` files; inventory-file host vars rank below `host_vars/` files.

## Verify
```bash
ansible web01 -i hosts.ini -m ansible.builtin.debug -a 'msg={{ max_clients | type_debug }}'
```
For a `[web:vars]` value the type name is a string type, not an integer.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed on the inventory guide ("Defining variables in INI format", group variables for INI and YAML, `group_vars` files hold lists and hashes) and the variable precedence list in Using variables; the `type_debug` filter exists in `filters/core.py`. Removed the `jq` check and the remark that `when: enable_tls` "works by luck".
Method: documentation only; no commands were run.
