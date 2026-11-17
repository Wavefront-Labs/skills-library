---
id: computing-software.cloud-infrastructure-engineering.ansible.host-and-group-variables-in-controller-inventories
name: host-and-group-variables-in-controller-inventories
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-projects-inventories, controller-host-vars, awx-inventories, group-vars]
level: practitioner
status: docs-checked
description: "Set host and group variables in controller inventories as code, and how overwrite and overwrite_vars treat them when syncing from a source."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-inv-variable-management.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-inventory-import.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-extra-variables.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/inventory_source.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/host.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/group.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Host and group variables in controller inventories

## Guidance from the docs
Keep variable data with the host and group definitions (the inventory editor) rather than in
`group_vars/` and `host_vars/` files. With dynamic inventory sources, the controller synchronises
such variables into its database while the **Overwrite Variables** option is not set.

## As code
```yaml
- ansible.controller.inventory:
    name: Production
    organization: Platform
    variables: {ntp_server: ntp.corp.example.com}
- ansible.controller.group:
    name: web
    inventory: Production
    variables: {http_port: 8080}
- ansible.controller.host:
    name: web01.corp.example.com
    inventory: Production
    variables: {ansible_host: 10.0.0.11}
```
The `inventory`, `group` and `host` modules each take `variables` as a dict.

## Overwrite options
The `inventory_source` module and `awx-manage inventory_import` share two switches:
- `overwrite`: delete child groups and hosts not found in the source. The CLI describes it as using only the external data.
- `overwrite_vars`: override vars in child groups and hosts with those from the external source. On the CLI, existing hosts then get variable data exclusively from the source.
Default behaviour: new variables from the source are added, keys that already exist are overwritten, and variables that did not come from the source are preserved. Edits and additions to host variables persist across syncs as long as `overwrite_vars` is not set.
Choose deliberately: leave `overwrite_vars` off to keep hand-added vars, turn it on if the source must be the only truth.

## Precedence reminder
Passing extra variables to a job template (including survey answers) can override variables from the inventory and project. To protect a variable, redefine it in the survey. Extra variables can also be defined at inventory, group and host level.

## Verify
- [ ] After a sync, a variable added by hand on a host is still present (overwrite_vars off) or gone (on), as intended.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (inventory variable management, inventory import, extra variables), ansible/awx devel modules inventory_source, host, group.
- Confirmed: guidance to keep vars with host and group definitions, sync with Overwrite Variables unset, default merge behaviour, overwrite and overwrite_vars meanings, persistence note, module `variables` dict parameters, extra vars overriding inventory vars.
- Removed unconfirmed claims: inventory sources importing `group_vars/` and `host_vars/` from a project, project-adjacent group_vars applying at runtime and beating inventory vars, the merge-drift and "enable both" recommendation, vault-encrypted values needing a job template credential, large host variable blobs slowing the UI, the `awx hosts get` jq verify command.

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
