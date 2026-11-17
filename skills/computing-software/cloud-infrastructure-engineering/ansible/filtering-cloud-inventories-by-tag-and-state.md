---
id: computing-software.cloud-infrastructure-engineering.ansible.filtering-cloud-inventories-by-tag-and-state
name: filtering-cloud-inventories-by-tag-and-state
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, inventory-filters, ec2-filters, aws-ec2-inventory, azure-rm-inventory, gcp-compute-inventory, instance-state, tag-filters, include-filters, exclude-filters, hostnames, inventory-scope, blast-radius]
level: practitioner
status: docs-checked
description: "Scope aws_ec2, azure_rm and gcp_compute inventories to running, tag-owned instances with filters, include/exclude filters and readable hostnames."
sources: ["https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html", "https://docs.ansible.com/ansible/latest/collections/azure/azcollection/azure_rm_inventory.html", "https://docs.ansible.com/ansible/latest/collections/google/cloud/gcp_compute_inventory.html", "https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html", "https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Filtering cloud inventories by tag and state

**Goal:** the inventory contains only the running instances owned by this automation, so
`hosts: all` in a playbook cannot reach a stopped box or another team's VM.

All three plugins live in collections that are not part of ansible-core. Their config files must end with
`aws_ec2.yml|yaml` (AWS) or `gcp_compute.yml|yaml` / `gcp.yml|yaml` (GCP).

## 1. AWS (amazon.aws.aws_ec2)
```yaml
# prod.aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions: [eu-west-1, eu-central-1]
filters:
  instance-state-name: running
  tag:ManagedBy: ansible
  tag:Environment: [prod, qa]      # a list means any of these values
include_filters:                   # an instance matching at least one entry is included
  - tag:Role: [web, api]
exclude_filters:                   # excluded; takes priority over include_filters and filters
  - tag:Maintenance: ["true"]
hostnames:                         # in order of precedence
  - tag:Name
  - private-ip-address
compose:
  ansible_host: private_ip_address
keyed_groups:
  - key: ec2_tags.Role
    prefix: role
strict: false
```
- `filters` is a dict of filter/value pairs using the filter names of the EC2 `describe-instances` options (the plugin page links the AWS list; the examples there use `instance-state-name`, `tag:<Key>`, `instance.group-id`).
- Every entry in `include_filters` and in `exclude_filters` triggers its own search query, so the docs advise keeping both lists short.
- `hostnames` is an ordered list: by default the first name that matches is used for each instance; `allow_duplicated_hosts: true` keeps every matching name instead. `tag:Name` uses the value of the Name tag. A list item may be a dict with `name`, `prefix` and `separator` (default `_`).
- `compose: ansible_host: private_ip_address` is the docs' own example of connecting by private IP; `hostnames` sets `inventory_hostname` only.
- Tag values are exposed as `ec2_tags` (added in amazon.aws 11.2.0). The older `tags` host variable is deprecated and slated for removal in a release after 2026-12-01 (`use_deprecated_tags: false` switches it off), so use `ec2_tags`.
- `strict: false` is the default: invalid entries are skipped; `true` makes them fatal. `strict_permissions` defaults to true (a 403 fails the plugin).
- `regions` empty means all regions except possibly restricted ones.

Check it: `ansible-inventory -i prod.aws_ec2.yml --graph` (also `--list`).

## 2. Azure (azure.azcollection.azure_rm)
```yaml
# prod.azure_rm.yml
plugin: azure.azcollection.azure_rm
include_vm_resource_groups: [rg-prod-web, rg-prod-db]
exclude_host_filters:
  - tags['ManagedBy'] is not defined or tags['ManagedBy'] != 'ansible'
hostnames:
  - tags.vm_name
  - default
conditional_groups:
  db_hosts: "'db' in name"
keyed_groups:
  - prefix: env
    key: tags.Environment | default('none')
```
- `exclude_host_filters` expressions exclude a host when true; `include_host_filters` includes hosts when an expression is true (default `[true]`).
- `default_host_filters` already excludes `powerstate != "running"` and `provisioning_state != "succeeded"` hosts (its default); setting it replaces that default.
- `include_vm_resource_groups` defaults to all (`'*'`); the docs list explicit names and `'*'`. VMSS, Azure Stack HCI and Arc resource groups need their own `include_*_resource_groups` options (default empty).
- `tags` is a dictionary host variable; `fail_on_template_errors` defaults to true, so guard against missing tags as above.
- `hostnames` default generates hashed globally unique names; `plain_host_names: true` uses the old script-style names, which can conflict.

## 3. GCP (google.cloud.gcp_compute)
```yaml
# prod.gcp_compute.yml
plugin: google.cloud.gcp_compute
auth_kind: serviceaccount
service_account_file: /path/to/service_account.json
projects: [my-prod-project]
zones: [europe-west1-b, europe-west1-c]
filters:
  - status = RUNNING
hostnames: [name]
compose:
  ansible_host: networkInterfaces[0].networkIP
keyed_groups:
  - prefix: gcp
    key: labels
```
- `auth_kind` is required (`application`, `serviceaccount`, `machineaccount`, `accesstoken`).
- Each additional entry in `filters` is added as an AND condition; the filter syntax is the Compute API's (the plugin page links its reference). The page's own examples are `status = RUNNING` and `scheduling.automaticRestart = true AND status = RUNNING`.
- `hostnames` default is `public_ip`, `private_ip`, `name`; also supported `hostname` and `labels.vm_name`. `zones` defaults to all zones. The page's example comment says `networkInterfaces[0].networkIP` is the private-IP form.

## 4. Enforce the scope in the playbook
```yaml
- hosts: role_web
  pre_tasks:
    - ansible.builtin.assert:
        that: ec2_tags.ManagedBy | default('') == 'ansible'
```
Group patterns such as `role_web:&role_api` (intersection) and `all:!host1` (exclusion) are documented on the Patterns page. The assert catches a misconfigured inventory file; `that` takes a list of expressions like `when`.

## Gotchas
- Two instances with the same `tag:Name` collide when it is the only hostname: add a second `hostnames` entry or a `prefix`/`separator` dict.
- Tag values are strings, so quote boolean-looking values (`"true"`).
- Caching (`cache: true`) serves stale data until `cache_timeout` (default 3600 seconds); `ansible-inventory --flush-cache` clears the fact cache for inventory hosts.
- `strict: true` makes invalid entries fatal: good for prod, painful during a migration.

## Verify
- [ ] `ansible-inventory -i prod.aws_ec2.yml --graph` shows no stopped instances (stop one, clear the cache, confirm it disappears).

## Checked
Date: 2026-11-07. Read in full: the amazon.aws.aws_ec2 and google.cloud.gcp_compute inventory pages and the examples block of the azure.azcollection.azure_rm inventory page (its parameter table was read only for the options named above, not every row), the ansible-inventory CLI page, the assert module page and the Patterns page (searched for the `:&`/`:!` operators, not read in full). Not opened: the AWS describe-instances and Compute API filter references that the plugin pages link to, so those filter names are only the ones that appear in the plugin examples.
Corrected: GCP `filters` entries are ANDed (the skill said ORed) and `auth_kind` is required; `exclude_filters` is not a cheap client-side step, each entry triggers a query; the `tags` host variable is deprecated (use `ec2_tags`); duplicate hostnames keep the first match unless `allow_duplicated_hosts`, not "keep one and warn"; the Azure expression `tags.ManagedBy != 'ansible'` would error on VMs without the tag; `powerstate != 'running'` is already in the Azure default filters.
Removed as not on a cited page: `rg-prod-*` wildcard group names, GCP `labels.managed_by = ansible` filter syntax, the `placement.availability_zone` keyed group, the `jq` verify commands, the hostnames example with `instance-id`, and the `instance-type`/`vpc-id`/`tag-key` filter names.
Method: documentation only; no commands were run.
