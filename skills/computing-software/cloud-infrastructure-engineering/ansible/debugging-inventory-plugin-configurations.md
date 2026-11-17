---
id: computing-software.cloud-infrastructure-engineering.ansible.debugging-inventory-plugin-configurations
name: debugging-inventory-plugin-configurations
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, inventory-plugin-debug, inventory-plugins, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug inventory plugins that return nothing: plugin enablement, file naming, auth, -vvvv parse errors, cache staleness and unparsed source failures."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/inventory/auto.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging inventory plugin configs

Symptom: `[WARNING]: Unable to parse ... as an inventory source` or `No inventory was parsed, only implicit localhost is available`.

## Step 1: see why each plugin rejected the file
```bash
ansible-inventory -i inventory/aws_ec2.yml --graph -vvv
```
At `-vvv` ansible-core reports, for each enabled plugin, whether it parsed the source or declined it. Typical lines:
- `Parsed <source> inventory source with <plugin> plugin`: success; this is the plugin that handled the file.
- `<plugin> declined parsing <source> as it did not pass its verify_file() method`: the plugin does not accept this file, usually because of the **file name** or extension.
- `auto` raising `no root 'plugin' key found` (file has no top-level `plugin:`), `specifies unknown plugin` (the plugin is not installed or the name is wrong) or `could not be verified by inventory plugin` (the named plugin rejected the file name).
- `Failed to parse inventory with '<plugin>' plugin.` followed by the plugin's own error (credentials, permissions, missing SDK, bad options). These errors are shown as warnings only when no plugin could parse the source.

## Step 2: check common causes
| Cause | Fix |
|---|---|
| File name suffix | each plugin documents its own; for `amazon.aws.aws_ec2` the file must end in `aws_ec2.yml` or `aws_ec2.yaml` (for example `my_inventory.aws_ec2.yml`) |
| Plugin not enabled | `[inventory] enable_plugins = host_list, script, auto, yaml, ini, toml` is the default; `auto` loads the plugin named by `plugin:` |
| Collection or SDK missing | `ansible-galaxy collection list amazon.aws`; install the Python SDK named in `ansible-doc -t inventory <plugin>` into the **same** Python that Ansible uses (`ansible --version`) |
| Stale cache | `--flush-cache` (an inventory option) or delete the cache directory |
| Filters too strict | temporarily remove the plugin's `filters:` and `include_filters:` |

## Step 3: fail loudly in CI
```ini
[inventory]
unparsed_is_failed = true        # fatal when no source at all could be parsed
any_unparsed_is_failed = true    # fatal when any single source cannot be parsed
```
`any_unparsed_is_failed` has existed since ansible-core 2.7. Environment variables: `ANSIBLE_INVENTORY_UNPARSED_FAILED` and `ANSIBLE_INVENTORY_ANY_UNPARSED_FAILED`.

## Inspect what came back
```bash
ansible-inventory -i inventory/aws_ec2.yml --list
ansible-inventory -i inventory/aws_ec2.yml --host i-0abc     # the variables available to compose expressions
```

## Gotchas
- `compose`, `groups` and `keyed_groups` values are Jinja expressions written without `{{ }}`; check each plugin's documentation before assuming other options are templated.

## Verify
- [ ] `ansible-inventory --graph` shows the expected groups with a non-zero number of hosts.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5). Confirmed in `lib/ansible/inventory/manager.py` (messages and verbosity), the `auto` inventory plugin (error texts), `config/base.yml` (`INVENTORY_ENABLED`, both unparsed settings, `any_unparsed_is_failed` since 2.7), `cli/arguments/option_helpers.py` (`--flush-cache` among inventory options), and the amazon.aws `aws_ec2` plugin documentation (suffix). Corrected: `any_unparsed_is_failed` dates from 2.7, not 2.15; the plugin lines appear at `-vvv`. Removed the `jq` pipelines, the suffix list for other plugins, the Python-import one-liner and the execution-environment remark.
Method: documentation only; no commands were run.
