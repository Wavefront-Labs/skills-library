---
id: computing-software.devops-ci-cd.semaphore-ui.inventory-types-and-dynamic
name: inventory-types-and-dynamic
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [inventory, static-inventory, dynamic-inventory, netbox, consul, semaphore-ui]
level: practitioner
status: docs-checked
description: "Pick the inventory type (static, static-yaml, file, workspace) and use dynamic inventory with NetBox or Consul."
sources:
  - https://semaphoreui.com/docs/user-guide/inventory
  - https://semaphoreui.com/docs/user-guide/inventory/consul-dynamic-inventory
  - https://semaphoreui.com/docs/user-guide/inventory/netbox-dynamic-inventory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inventories

Goal: tell Ansible which hosts to target.

An inventory can be INI, YAML, JSON or TOML. Semaphore reads one from a file or stores a static one edited in the UI. Every inventory needs a user credential (username/password or SSH key from the Key Store) and optionally a sudo credential.

Types:

| Type | Meaning |
|---|---|
| `static` | INI text edited in the UI. |
| `static-yaml` | YAML text; use for plugin inventories such as NetBox or Consul. |
| `file` | A path. Relative means inside the template's repository; absolute means a file on the server. Optionally pick a separate inventory repository. |
| `terraform-workspace`, `tofu-workspace`, `terragrunt-workspace` | Not Ansible inventories; a workspace for Terraform, OpenTofu or Terragrunt templates. |

Dynamic inventory:
- NetBox: use the `netbox.netbox.nb_inventory` plugin in a `static-yaml` inventory (the plugin settings are `plugin`, `api_endpoint` and `token`, with `validate_certs` and `config_context` optional in the docs example; replace the URL and token with your own).
- Consul: commit a Python inventory script (for example `inventory/consul_inventory.py`) that queries the Consul catalog; the host or runner needs Python 3 and a Consul ACL token if ACLs are on. Create a `file` inventory with the path relative to the repository root; Semaphore runs the script when the playbook runs. The docs script reads `CONSUL_HTTP_ADDR` and `CONSUL_HTTP_TOKEN` from a Variable Group.

Gotchas:
- Deleting an inventory requires first removing the resources tied to it.

Verify: run an Ansible template with the inventory and check the task log shows the expected hosts.

## Checked

2026-11-04: checked against the inventory, Consul and NetBox pages. Added the documented NetBox plugin keys and Consul variables; removed unconfirmed gotchas and the ansible-inventory verify step.

Method: documentation only; no commands were run.
