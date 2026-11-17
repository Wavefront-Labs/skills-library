---
id: computing-software.cloud-infrastructure-engineering.ansible.enabling-inventory-plugins-and-the-auto-plugin
name: enabling-inventory-plugins-and-the-auto-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, inventory-plugins, enable-plugins, auto-plugin, inventory-enabled, plugin-order, yaml-inventory, ini-inventory, host-list, toml-inventory, inventory-ignore, unable-to-parse, plugin-filename-suffix]
level: practitioner
status: docs-checked
description: "Control which inventory plugins parse a source (enable_plugins order), how auto dispatches YAML by plugin key and file suffix, and fix 'Unable to parse' warnings."
sources: ["https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/inventory/manager.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/inventory/auto.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/base.yml", "https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling inventory plugins and the auto plugin

## 1. The enabled list and its order
```ini
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
```
That list is the default (`INVENTORY_ENABLED`; environment variable `ANSIBLE_INVENTORY_ENABLED`), and it also sets the order in which plugins are tried. For every `-i` source Ansible offers it to each enabled plugin **in this order**; the first plugin whose `verify_file()` accepts it parses it:
- `host_list` accepts a comma-containing string that is not an existing path (`'a,b,'`).
- `script` accepts executable files.
- `auto` accepts files ending in `.yml` or `.yaml`, reads the `plugin:` key and hands the file to the plugin it names.
- `yaml` accepts files with no extension or a configured YAML extension; `ini` accepts files other than `.toml`; `toml` accepts `.toml` files.

To use a plugin without `auto`, add its name to the list: `enable_plugins = amazon.aws.aws_ec2, yaml, ini`. Restricting the list to what you use avoids surprise parsing.

## 2. How auto dispatches
```yaml
# inventories/prod/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions: [eu-west-1]
```
`auto` loads the plugin named by `plugin:` (an unknown name fails with "specifies unknown plugin"), then asks that plugin's `verify_file()` whether it accepts the file (otherwise: "could not be verified by inventory plugin"). A file with no root `plugin:` key fails with "no root 'plugin' key found". Most cloud plugins also require a file-name suffix: for `amazon.aws.aws_ec2` the file must end in `aws_ec2.yml` or `aws_ec2.yaml` (for example `my_inventory.aws_ec2.yml`). Check each plugin's documentation (`ansible-doc -t inventory <fqcn>`) for its required suffix.

## 3. Reading the messages
Run `ansible-inventory -i inventories/prod --graph -vvv` and read the plugin lines.
| Message | Meaning |
|---|---|
| `Parsed <source> inventory source with <name> plugin` (-vvv) | the plugin that accepted the source |
| `<name> declined parsing <source> as it did not pass its verify_file() method` (-vvv) | normal for non-matching plugins; a problem only if every plugin declines |
| `Failed to parse inventory with '<name>' plugin.` (warning, followed by the plugin's error) | a plugin accepted the file but raised (bad credentials, missing SDK, bad options). Shown only when no plugin parsed the source |
| `Unable to parse <source> as an inventory source` (warning) | no plugin parsed it |
| `No inventory was parsed, only implicit localhost is available` (warning) | nothing was parsed; the `-i` path may be wrong |

Two settings make failures fatal: `unparsed_is_failed = true` (`[inventory]`, env `ANSIBLE_INVENTORY_UNPARSED_FAILED`) makes it fatal when **no** source at all could be parsed; `any_unparsed_is_failed = true` (env `ANSIBLE_INVENTORY_ANY_UNPARSED_IS_FAILED`) makes it fatal when **any** source cannot be parsed ("Completely failed to parse inventory source").
A missing SDK appears as an import error inside the plugin's failure message; install it into the Python that runs Ansible (`ansible --version` shows it).

## 4. Quick plugin facts
```bash
ansible-doc -t inventory -l                       # installed inventory plugins
ansible-doc -t inventory amazon.aws.aws_ec2       # options, suffixes, examples
```

## Gotchas
- A static YAML file with a top-level `plugin:` key (for example a group named `plugin`) is picked up by `auto`; rename the group.
- `enable_plugins` replaces the default list: leave out `yaml` or `ini` and your static files are "unable to parse".
- The `INVENTORY_UNPARSED_WARNING` setting (default true) controls the warning about falling back to an implicit localhost-only inventory.

## Verify
- [ ] `ansible-inventory -i <plugin-config> --list -vvv` shows `Parsed ... inventory source with ... plugin` and the expected hosts.
- [ ] Renaming the config to a non-matching suffix makes the plugin decline or fail, and renaming it back fixes it.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5). Confirmed in `lib/ansible/inventory/manager.py` (message texts, verbosity levels, `unparsed_is_failed` versus `any_unparsed_is_failed`), the `auto`, `host_list`, `script`, `yaml`, `ini` and `toml` plugin `verify_file()` code, `INVENTORY_ENABLED`, `INVENTORY_UNPARSED_IS_FAILED`, `INVENTORY_ANY_UNPARSED_IS_FAILED` and `INVENTORY_UNPARSED_WARNING` in `config/base.yml`, and the amazon.aws `aws_ec2` plugin (suffix `aws_ec2.yml` or `aws_ec2.yaml`). Removed the other plugins' suffix list (not confirmed) and a grep pipeline.
Method: documentation only; no commands were run.
