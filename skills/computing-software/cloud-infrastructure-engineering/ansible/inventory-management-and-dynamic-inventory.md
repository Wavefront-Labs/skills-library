---
id: computing-software.cloud-infrastructure-engineering.ansible.inventory-management-and-dynamic-inventory
name: inventory-management-and-dynamic-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, inventory, dynamic-inventory, inventory-plugins, aws-ec2-inventory, amazon-aws, azure-rm-inventory, gcp-compute-inventory, constructed, keyed-groups, compose, group-vars, host-vars, host-patterns, limit, ansible-inventory, inventory-cache, yaml-inventory, ini-inventory, children-groups, ansible-host]
level: practitioner
status: docs-checked
description: "Build Ansible inventory that tracks reality: YAML groups/children, group_vars layout, aws_ec2 and azure_rm plugins with keyed_groups and compose, constructed, caching."
sources: ["https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html", "https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html", "https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/constructed_inventory.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ansible inventory management and dynamic inventory — groups that match the fleet

**Goal:** an inventory per environment where hosts appear and disappear automatically
with the cloud, are grouped by role/region/environment from tags, and carry their
variables from a predictable `group_vars` tree.

## 1. Static inventory (YAML)
```yaml
# inventories/prod/hosts.yml
all:
  children:
    webservers:
      hosts:
        web01.example.internal:
        web02.example.internal: { ansible_host: 10.0.1.12 }
    dbservers:
      hosts:
        db01.example.internal: { ansible_user: admin }
    eu_west:
      children: { webservers: {}, dbservers: {} }
```
- Groups by **function** (`webservers`) and by **dimension** (`eu_west`, `prod`) — a
  host belongs to several; `children` composes them.
- Variables live in files beside the inventory, not inline, using the `host_group_vars`
  plugin: `group_vars/webservers.yml`, `group_vars/all/`, `host_vars/web01.example.internal.yml`.
  Files must be YAML with extension `.yml`, `.yaml`, `.json` or none.

## 2. Dynamic inventory with plugins
Use inventory plugins. The `aws_ec2` source file name must end with `aws_ec2.yml` or
`aws_ec2.yaml`; the `azure_rm` plugin requires `azure_rm.yml` or `azure_rm.yaml`:
```yaml
# inventories/prod/prod.aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions: [eu-west-1]
filters:
  tag:Environment: prod
hostnames:
  - tag:Name
  - private-ip-address
compose:
  ansible_host: private_ip_address
keyed_groups:
  - key: placement.region
    prefix: aws_region
  - key: ec2_tags['Role']
    prefix: role
```
- `hostnames` sets `inventory_hostname`; to change `ansible_host` without changing
  `inventory_hostname`, use `compose`. By default the first name matching an entry of the
  `hostnames` list is returned; `allow_duplicated_hosts: true` returns all matches.
- Azure uses plugin `azure.azcollection.azure_rm` with `keyed_groups` and `compose` too.
- Point `-i` at a **directory**: Ansible merges the sources in it in alphabetical order of
  file name; prefix file names to control load order.
- Keep credentials out of inventory files; the aws_ec2 plugin documents `profile` and other
  authentication options.

## 3. `constructed` for derived groups
The `constructed` plugin builds groups and variables from existing host variables:
```yaml
# inventories/prod/zz-constructed.yml   (sources load alphabetically)
plugin: ansible.builtin.constructed
strict: false
keyed_groups:
  - key: ansible_distribution | lower
    prefix: os
groups:
  needs_reboot: reboot_required | default(false)
```
With `strict: false`, failed expressions (for example missing variables) are ignored.

## 4. Caching
Inventory plugins that support caching accept `cache`, `cache_plugin`, `cache_timeout`
(default 3600 seconds) and `cache_connection`:
```yaml
cache: true
cache_plugin: ansible.builtin.jsonfile
cache_connection: <cache-directory>
cache_timeout: 300
```

## 5. Targeting
- `--limit 'webservers:&staging'` (intersection), `'webservers:!atlanta'` (exclusion),
  `--limit @retry_hosts.txt` (hosts from a file).
- Keep `hosts:` in plays to functional groups; narrow with `--limit` at run time.

## Gotchas
- Groups of the same level merge in alphabetical order, and variables from the last group
  loaded win. Set `ansible_group_priority` (default 1; higher merges later) in an inventory
  source, not in `group_vars/`, to change that.
- `host_vars` filenames must match the **inventory hostname**, which with a dynamic inventory
  is whatever `hostnames:` produced.
- Filters that exclude instances make them silently disappear from runs; check expected host counts.

## Verify
- [ ] `ansible-inventory -i inventories/prod --graph` shows the expected groups and host counts.
- [ ] `ansible-inventory -i inventories/prod --host <HOST>` shows merged vars from the right `group_vars`.
- [ ] Launching a tagged test instance makes it appear after the cache expires; terminating it removes it.
- [ ] No credentials in any inventory file.

## Checked
2026-11-09. Confirmed in the Ansible inventory guide, patterns guide, the aws_ec2 plugin
documentation (file suffix, filters, hostnames, allow_duplicated_hosts, keyed_groups, compose),
azure_rm plugin source (name and suffix), the constructed plugin and the inventory cache doc
fragment (cache options, 3600 default). Removed as unconfirmed: the gcp_compute plugin and its
suffix, the instance-state-name filter, tag-derived group naming examples, group-name
sanitisation claim, the enable_plugins advice, the ansible-inventory flush-cache command,
the "public DNS" hostnames warning, and the duplicate-hostnames uncertainty note.
Method: documentation only; no commands were run.
