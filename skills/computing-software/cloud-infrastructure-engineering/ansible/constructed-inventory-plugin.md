---
id: computing-software.cloud-infrastructure-engineering.ansible.constructed-inventory-plugin
name: constructed-inventory-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, constructed-plugin, constructed-groups, keyed-groups, compose]
level: advanced
status: docs-checked
description: "Layer the constructed inventory plugin over static and cloud sources to build groups from vars and facts with groups, keyed_groups, compose and strict."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/inventory/constructed.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/doc_fragments/constructed.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The constructed inventory plugin

`ansible.builtin.constructed` adds no hosts; it builds variables and groups from the hosts and variables that earlier inventory sources already loaded. Sources in an inventory directory are processed in alphabetical order, so name the file to sort last.

```
inventory/
  01-hosts.yml          # static or cloud plugin config
  02-aws_ec2.yml
  zz-constructed.yml    # runs last
```
```yaml
# inventory/zz-constructed.yml
plugin: ansible.builtin.constructed
strict: false
compose:
  ansible_host: private_ip_address | default(ansible_host)
  env: tags.Environment | default('dev') | lower
groups:
  prod_web: inventory_hostname.startswith('web') and env == 'prod'
  needs_patch: kernel_version is defined and kernel_version is version('5.14', '<')
keyed_groups:
  - key: env
    prefix: env
  - key: ansible_distribution | default('unknown')
    prefix: os
    separator: "_"
```
The config file needs a valid YAML extension (or `.config`, or no extension).

## Facts as input
Only variables already available from previous inventory sources or the fact cache can be used in the expressions. Facts are therefore available only if a fact cache holds them at parse time:
```ini
[defaults]
fact_caching = jsonfile
fact_caching_connection = ~/.ansible/facts
```
Run a fact-gathering play first, then later runs see `ansible_distribution` during the inventory build. Extra vars (`-e`) are available to `compose` and `groups` only when `use_extra_vars` is true:
```ini
[inventory_plugins]
use_extra_vars = true     # or ANSIBLE_INVENTORY_USE_EXTRA_VARS=true
```
`use_vars_plugins: true` in the plugin file also makes `group_vars/` and `host_vars/` values available to the expressions; implicit groups such as `all` and `ungrouped` must be defined explicitly in an earlier source for their `group_vars` to apply.

## strict
- `strict: false` (default): expressions that fail, for example on a missing variable, are skipped without an error.
- `strict: true`: an invalid entry is a fatal error; use it while developing to catch typos.

## keyed_groups options
`key`, `prefix` (default empty), `separator` (default `_`), `parent_group`, `default_value`, `trailing_separator` and `leading_separator`. With no prefix the group name starts with the separator unless `leading_separator: false`.

## Gotchas
- Group expressions are Jinja expressions **without** `{{ }}`.
- The plugin documentation warns that inventories are not finalised during construction: the automatically populated `all` and `ungrouped` groups reflect only what earlier sources added, and runtime magic variables such as `groups` and `hostvars` do not exist yet.
- Generated group names that contain invalid characters follow `TRANSFORM_INVALID_GROUP_CHARS` (`force_valid_group_names` in `[defaults]`): the default `never` keeps the name and warns, and `always` replaces invalid characters with `_`.

## Verify
```bash
ansible-inventory -i inventory --graph prod_web
ansible-inventory -i inventory --host web01
```
The second command prints the merged variables for the host; look for `env`.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5). Confirmed in the `constructed` inventory plugin and its `constructed` doc fragment (alphabetical processing, `strict` default no, `use_extra_vars` ini section `inventory_plugins` and env var, `use_vars_plugins`, keyed_groups suboptions, the notes on magic variables), `TRANSFORM_INVALID_GROUP_CHARS`, `CACHE_PLUGIN` and `CACHE_PLUGIN_CONNECTION` in `config/base.yml`. Corrected the `use_extra_vars` section name and the group-name sanitising claim; removed the AAP remark and the `group_names` example, which the plugin notes say is not available.
Method: documentation only; no commands were run.
