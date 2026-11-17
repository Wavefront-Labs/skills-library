---
id: computing-software.devops-ci-cd.semaphore-ui.variable-groups
name: variable-groups
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [variable-groups, environment, extra-vars, secrets, tf-var, semaphore-ui]
level: practitioner
status: docs-checked
description: "Create variable groups of JSON extra vars and secrets, and pass them to Ansible and Terraform (TF_VAR_ prefix)."
sources:
  - https://semaphoreui.com/docs/user-guide/environment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Variable groups

Goal: store variables for task templates.

All task templates require a variable group, even an empty one: type `{}`.

Create: Variable Group tab, New Variable Group, name it, type or paste valid JSON variables.

```json
{ "app_version": "1.4.2", "region": "eu-west-1" }
```

Ansible receives the variables as extra variables from a temporary file in which every value containing a Jinja2 delimiter (`{{ }}`, `{% %}`, `{# #}`) is tagged `!unsafe`, so a Jinja2 expression in a value reaches the playbook literally. Values keep their JSON type: `"2026.08"` stays a string, `3` stays a number. Secrets of the group passed as variables travel in a separate file encrypted with Ansible Vault.

Terraform and OpenTofu: to use a stored variable or secret, prefix its name with `TF_VAR_`. Example: in the group's Secrets tab add `TF_VAR_hcloud_token`, declare `variable "hcloud_token"` in the code and read `var.hcloud_token`.

Edit with the pencil icon on the Variable Groups tab. Before deleting a group, remove all resources tied to it; selecting the group and clicking the trash can icon shows which resources use it, with links.

## Checked

2026-11-07. Read in full: the Variable Groups page (user-guide/environment.md in the semaphore-docs repository, including its Hetzner TF_VAR example code). Confirmed: JSON format, the empty-group requirement, create/edit/delete steps, the !unsafe and JSON-type behaviour, the Vault-encrypted secrets file, the TF_VAR_ prefix and the Secrets tab example. Removed: the TF_VAR table of invented names, "encrypted at rest and masked in the UI and logs", "called environments in the API", the gotcha that webhook values override group variables, the "server-wide variables belong in env_vars" gotcha, the claim that Terraform variables are injected as environment variables (the page only states the TF_VAR_ prefix rule), and the invented Verify step.
Method: documentation only; no commands were run.
