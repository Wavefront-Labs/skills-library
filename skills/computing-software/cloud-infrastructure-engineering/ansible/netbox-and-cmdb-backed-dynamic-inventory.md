---
id: computing-software.cloud-infrastructure-engineering.ansible.netbox-and-cmdb-backed-dynamic-inventory
name: netbox-and-cmdb-backed-dynamic-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, netbox-inventory, cmdb-inventory, nb-inventory, netbox, source-of-truth, inventory-plugin, servicenow-inventory, keyed-groups]
level: practitioner
status: docs-checked
description: "Use NetBox (netbox.netbox.nb_inventory) or a CMDB such as ServiceNow as the inventory source of truth: filters, grouping, config contexts, caching and safe fallbacks."
sources:
  - "https://github.com/netbox-community/ansible_modules/blob/devel/plugins/inventory/nb_inventory.py"
  - "https://github.com/ansible-collections/servicenow.itsm/blob/main/plugins/inventory/now.py"
  - "https://github.com/ansible-collections/servicenow.itsm/blob/main/plugins/doc_fragments/instance.py"
  - "https://docs.ansible.com/ansible/latest/plugins/inventory.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetBox and CMDB-backed dynamic inventory

Goal: hosts, groups and per-host data come from the source of truth (NetBox, ServiceNow CMDB), so
nobody edits a static `hosts` file and drift between CMDB and automation disappears.

## NetBox
```bash
ansible-galaxy collection install netbox.netbox
export NETBOX_API=https://netbox.example NETBOX_TOKEN=<NETBOX_TOKEN>
```
The plugin source imports `pytz` and `packaging` and talks to the NetBox REST API; install them in the environment that runs the inventory. `api_endpoint` is required (it can come from `NETBOX_API`), and the token comes from `NETBOX_TOKEN` (also `NETBOX_API_KEY`).

Inventory source file, for example `netbox_inventory.yml` (the plugin documentation uses this name):
```yaml
plugin: netbox.netbox.nb_inventory
validate_certs: true
config_context: true            # adds config context to host vars (default false)
interfaces: false               # default false; interfaces also fetch IP addresses
virtual_chassis_name: true      # use the virtual chassis name as the inventory hostname
group_by: [sites, device_roles, platforms, tags, tenants]
query_filters:
  - status: active
device_query_filters:
  - has_primary_ip: 'true'      # filters out patch panels and other passive devices
vm_query_filters:
  - cluster: prod-vmware
compose:
  ansible_network_os: platform.slug
keyed_groups:
  - {key: custom_fields.patch_window, prefix: patch, separator: "_"}
cache: true
cache_plugin: ansible.builtin.jsonfile
cache_connection: ~/.cache/ansible-netbox
cache_timeout: 900
```
- `group_by` defaults to an empty list, so no groups appear until you set it. Group names are `<grouping>_<value>`; `group_names_raw: true` drops the prefix. A boolean grouping such as `is_virtual` becomes a group named `is_virtual`.
- `query_filters` apply to both devices and VMs, `device_query_filters` to devices only and `vm_query_filters` to VMs only; entries are passed to NetBox as query-string parameters, and the plugin docs comment says `query_filters` work as a logical OR. Adding `__n` to a field negates it (`tenant__n: internal`); custom fields are prefixed `cf_`. Filtering in NetBox is cheaper than filtering in Ansible.
- `ansible_host` is the device's primary IP; set `dns_name: true` and `ansible_host_dns_name: true` to use the primary IP's DNS name instead.
- `compose` and `keyed_groups` come from the constructed fragment, and the cache options from the inventory_cache fragment (both named in the plugin's `extends_documentation_fragment`).
- `flatten_config_context: true` adds config context variables directly to the host rather than under `config_context`.

## ServiceNow CMDB
```yaml
plugin: servicenow.itsm.now
instance:
  host: https://example.service-now.com
  username: svc_ansible
  password: "{{ lookup('env','SN_PASSWORD') }}"
table: cmdb_ci_linux_server
sysparm_query: "nameSTARTSWITHDatabase^nameENDSWITH1"    # example from the plugin docs
columns: [name, ip_address, os, sys_class_name, location]
inventory_hostname_source: name
keyed_groups: [{key: location, prefix: loc}]
```
- `table` defaults to `cmdb_ci_server`; `columns` defaults to `name, host_name, fqdn, ip_address`; `inventory_hostname_source` defaults to `name`; `sysparm_limit` defaults to 1000. The `ip_address` column is used for the Ansible host.
- `instance` takes `host`, `username`, `password` (each with an `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` environment fallback) and OAuth options such as `grant_type` and `client_id`.
- `query` is a list of per-field filters and separate list entries produce OR conditions, so two `query` entries on different fields do not mean AND. For AND conditions use `sysparm_query` with ServiceNow encoded query syntax (`^` separates AND conditions). The two options are mutually exclusive.
- `enhanced: true` builds groups from CMDB relationships.

## Generic CMDB with only an HTTP API
No plugin? Write a small inventory plugin rather than a legacy script; inventory plugins can use the constructed and cache fragments for `compose`, `keyed_groups` and caching.

## Gotchas
- In AWX/controller, the plugin docs say the NetBox credential type needs to expose `NETBOX_API` and `NETBOX_TOKEN` as environment variables.
- Check `ansible-inventory -i netbox_inventory.yml --graph` and `--host <name>` against what you expect before writing `hosts:` patterns.

## Verify
- [ ] `ansible-inventory -i netbox_inventory.yml --list` host count equals the device and VM count in NetBox with the same filters.
- [ ] A host's `config_context` values appear under `ansible-inventory --host <name>`.

## Checked

2026-11-09. Checked against the nb_inventory plugin documentation and source (options, defaults, env variables, group naming, filter examples, AWX credential note), the servicenow.itsm `now` inventory plugin documentation (table, columns, query versus sysparm_query semantics, defaults) and the servicenow.itsm instance doc fragment.

Corrected: the ServiceNow example combined two conditions as separate `query` entries and implied AND; the plugin docs say separate entries are OR, so the example now uses `sysparm_query`. The NetBox filter semantics were stated as OR within a key and AND across keys; the docs only say OR.

Removed as unsupported: the filename-suffix rule, the `pynetbox` dependency, the per-device API call cost note, the empty-inventory-on-missing-permission claim, group-name sanitising, config-context weight merging, `--flush-cache` advice and the `compose: ansible_host` line (the plugin already uses `ip_address`).

Method: documentation only; no commands were run.
