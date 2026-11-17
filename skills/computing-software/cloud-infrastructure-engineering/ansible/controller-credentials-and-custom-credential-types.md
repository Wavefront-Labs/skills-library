---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-credentials-and-custom-credential-types
name: controller-credentials-and-custom-credential-types
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, credentials, credential-types, machine-credential, custom-credential-type, vault-credential, source-control-credential, galaxy-credential, cloud-credentials, injectors, inputs, external-secret-lookup, hashicorp-vault-credential, cyberark, azure-key-vault, aws-secrets-manager-credential, credential-plugins, container-registry-credential]
level: practitioner
status: docs-checked
description: "Manage AWX/controller credentials: credential types, custom types with inputs and injectors (env, extra_vars, files), assignment rules and API behaviour."
sources: ["https://github.com/ansible/awx/blob/devel/docs/credentials/custom_credential_types.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller credentials and custom credential types

**Goal:** no secret is typed into a playbook or survey; jobs get exactly the
credentials their template was given, injected at runtime.

## 1. Credential types
- A `Credential Type` has a kind (`ssh`, `vault`, `scm`, `network`, `cloud`), `inputs` (the form fields) and `injectors` (how values reach the job). `GET /api/v2/credential_types` lists them, including the read-only built-ins (SSH/machine, Vault, SCM, Network, Amazon Web Services and others). Built-in types cannot be edited or deleted.
- A job template can have several credentials as long as their **types are unique**: for example one SSH, one Vault, one EC2 and one GCE credential, but not two OpenStack credentials. With `ask_credential_on_launch` true, credentials can be given in the launch payload.
- SCM inventory sources can use a credential, so third-party secrets can be used while the inventory loads.
- Attach to a template through `GET/POST /api/v2/job_templates/N/credentials/` with `id` plus `associate` or `disassociate`.
- `GET /api/v2/credentials/N` returns secret inputs as `$encrypted$`.
- Where credentials sit in your release (organization-level Galaxy/hub credentials, container registry credentials, external secret lookups), check the controller documentation for your version: those pages could not be read in this review.

## 2. Custom credential types
Only superusers can create, change or delete custom types (`POST /api/v2/credential_types/`).
```yaml
# inputs
fields:
  - {id: api_url, type: string, label: API URL}
  - {id: api_token, type: string, label: API token, secret: true}
required: [api_url, api_token]
# injectors
env:
  APP_API_URL: "{{ api_url }}"
  APP_API_TOKEN: "{{ api_token }}"
extra_vars:
  app_api_url: "{{ api_url }}"
```
- Input field keys: `id` and `label` (required, unique), `help_text`, `type` (`string` default or `boolean`), `format: ssh_private_key`, `secret` (stored encrypted), `multiline`, `default`, `choices` (strings). `required` lists mandatory field ids.
- Injectors use Jinja: `env`, `extra_vars` and `file`. A single file is `file: {template: "..."}` referenced as `{{ tower.filename }}`. Several files use `template.<name>` keys referenced as `tower.filename.<name>`:
```yaml
file:
  template.cert: "{{ cert }}"
  template.key: "{{ key }}"
env:
  MY_CERT: "{{ tower.filename.cert }}"
  MY_KEY: "{{ tower.filename.key }}"
```
- The single-file and multi-file syntax cannot be mixed in one type.
- Once credentials use a type, the fields in its `inputs` are read-only: create a new type and migrate instead.
- Prefer `env` injection; `extra_vars` values become visible in job variables and output, so pair secrets with `no_log` in the playbook.

## Gotchas
- Two attached credentials injecting the same environment variable: use distinct names so neither overrides the other.
- Create credentials with the right `credential_type` primary key: the inputs accepted are dictated by that type.

## Verify
- [ ] Launch a job that reads the injected environment variable and confirm the value arrives; add `no_log` where a token could print.
- [ ] `GET /api/v2/credentials/<id>/` shows `$encrypted$` for secret inputs.

## Checked
2026-10-28. Confirmed in the AWX custom credential types document: kinds, inputs schema keys, injector forms and the single versus multi-file rule, uniqueness of credential types per template, `ask_credential_on_launch`, API endpoints, `$encrypted$`, read-only inputs once in use, superuser-only creation. Removed because not confirmed: the built-in type table details, machine/vault attachment limits, `SECRET_KEY` and 0600 file mode claims, external secret plugin steps and auth methods, the claim that injectors can be edited in some cases,, the Galaxy credential ordering notes and the `infra.aap_configuration` automation example.
Method: documentation only; no commands were run.
