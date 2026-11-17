---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-and-callback-overhead-tuning
name: inventory-and-callback-overhead-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, performance-tuning, inventory-performance, callbacks-enabled, profile-tasks]
level: advanced
status: docs-checked
description: "Cut startup and per-task overhead from large inventories (caching, YAML vs scripts, vars plugins) and from enabled callbacks, and measure with profile and timer callbacks."
sources: ["https://docs.ansible.com/ansible/latest/reference_appendices/config.html", "https://docs.ansible.com/ansible/latest/plugins/inventory.html#using-inventory-plugins", "https://docs.ansible.com/ansible/latest/plugins/callback.html", "https://github.com/ansible/ansible/blob/stable-2.22/lib/ansible/plugins/doc_fragments/inventory_cache.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inventory and callback overhead

## Measure first
```bash
time ansible-inventory -i inventories/prod --list > /dev/null       # inventory build time alone
ANSIBLE_CALLBACKS_ENABLED=ansible.posix.profile_tasks,ansible.posix.timer ansible-playbook site.yml
```

## Inventory
| Cost driver | Fix |
|---|---|
| cloud plugin API calls every run | `cache: true` (default off), `cache_plugin: ansible.builtin.jsonfile` (default `memory`), `cache_timeout` (default 3600), `cache_connection: ~/.cache/ansible-inv` |
| too many enabled plugins | `[inventory] enable_plugins = yaml, ini, amazon.aws.aws_ec2, constructed` (only what you use) |
| legacy inventory scripts called per host (`--host`) | return `_meta.hostvars` in `--list` |


## Callbacks
- Enable only the callbacks you read: `callbacks_enabled = ansible.posix.profile_tasks` in development, and leave it out of production runs.
- Core ansible-core 2.22 ships the callbacks default, junit, minimal, oneline and tree; the `oneline` and `tree` ones are deprecated.

## Other startup costs
- `collections_scan_sys_path` (`ANSIBLE_COLLECTIONS_SCAN_SYS_PATH`, default true) controls scanning `sys.path` for installed collections.

## Verify
- [ ] Inventory build time and per-task overhead (timer callback total minus task time) drop after changes.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in plugins/doc_fragments/inventory_cache.py (stable-2.22): cache default no (env ANSIBLE_INVENTORY_CACHE), cache_plugin default memory, cache_timeout default 3600, cache_connection, cache_prefix; core cache plugins are jsonfile and memory; in config/base.yml: INVENTORY_ENABLED default list, CALLBACKS_ENABLED (ini callbacks_enabled, env ANSIBLE_CALLBACKS_ENABLED), COLLECTIONS_SCAN_SYS_PATH; in docs developing_inventory.rst: `_meta` avoids a `--host` call per host.
- Removed unconfirmed claims: per-source and group_vars cost rows, hostvars compose and vars-plugin advice, callback memory and redis remarks, roles_path cost, the ANSIBLE_DEBUG timing recipe.

Method: documentation only; no commands were run.
