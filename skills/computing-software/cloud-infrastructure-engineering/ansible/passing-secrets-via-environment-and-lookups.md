---
id: computing-software.cloud-infrastructure-engineering.ansible.passing-secrets-via-environment-and-lookups
name: passing-secrets-via-environment-and-lookups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, secrets, env-secrets, extra-vars-secrets, env-lookup, hashi-vault, no-log, ci-secrets]
level: practitioner
status: docs-checked
description: "Feed secrets to playbooks through the env, file and HashiCorp Vault lookups and the task environment keyword, instead of -e extra vars, and use no_log on tasks that expose them."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/env_lookup.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_lookup.html", "https://docs.ansible.com/ansible/latest/collections/community/hashi_vault/vault_kv2_get_lookup.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_environment.html", "https://docs.ansible.com/ansible/latest/reference_appendices/logging.html", "https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passing secrets via environment and lookups (not extra vars)

Goal: secrets reach tasks without being typed on the `ansible-playbook` command line.

## Why not `-e db_password=...`
- A value on the command line is part of the command you launched; anything that records commands (shell history, CI step logs) can capture it.
- Extra vars (`-e`) are a variable, and the precedence page says they override every other source, so one stray `-e` silently beats the value your inventory or lookup supplies.

## Pattern 1: env var plus the env lookup
```yaml
vars:
  db_password: "{{ lookup('ansible.builtin.env', 'DB_PASSWORD', default=undef()) }}"
```
- `ansible.builtin.env` ships with ansible-core and reads the environment of the controller process that invoked Ansible. Its term is the variable name (or a list of names).
- `default` (added in ansible-core 2.13) is what an undefined variable returns; the default is the empty string. Passing `default=undef()` forces an undefined-variable error instead, which is the page's own "fail if not defined" example.
- Before 2.13 the page shows `| default('World', True)` on the lookup result.

## Pattern 2: read from HashiCorp Vault at run time
`community.hashi_vault` is a separate collection, not part of ansible-core.
```yaml
vars:
  db_secret: "{{ lookup('community.hashi_vault.vault_kv2_get', 'apps/orders/db', url='https://vault.example.com:8200') }}"
# then: {{ db_secret.secret.password }}
```
- The term is the KV path relative to `engine_mount_point`, so leave the mount out of it. `engine_mount_point` defaults to `secret`; the page's example says the 4.0.0+ API path for `hello` is `secret/data/hello`.
- `auth_method` defaults to `token`; other choices include `userpass`, `ldap`, `approle`, `aws_iam`, `azure`, `jwt`, `cert`, `gcp` and `none`.
- `url` falls back to the `VAULT_ADDR` environment variable and raises an error if neither is set.
- Return values: `secret` (the key/value data), `metadata`, `data` and `raw`. The lookup also accepts several paths in one call with a single Vault login (`*paths`) and a `version` for a specific secret version.
- The collection's index also lists `vault_kv1_get`, `vault_read` and other lookups; they were not opened.

## Pattern 3: read a file on the controller
`"{{ lookup('ansible.builtin.file', '/path/to/secret_file') }}"` returns the contents of a file on the controller. It strips trailing whitespace by default (`rstrip` true) and leading whitespace is kept (`lstrip` false). It does not glob; use `fileglob` for that.

## Handing the secret to a remote process
```yaml
- name: Run migration
  ansible.builtin.command: /opt/app/bin/migrate
  environment:
    DB_PASSWORD: "{{ db_password }}"
  no_log: true
```
- The `environment` keyword (play, block or task level) sets variables for the action on the remote host. It does not affect Ansible itself or its configuration.
- `no_log: true` keeps the task's output out of logs, but the page warns it does not affect debugging output, so do not debug playbooks in production.

## Verify
- [ ] The command line of the run contains no secret.
- [ ] Task output with the secret is hidden (`no_log`), and a missing source variable fails the run rather than defaulting to empty.

## Checked
Date: 2026-11-07. Read: the env lookup page, the file lookup page (terms and lstrip/rstrip), the vault_kv2_get lookup page (terms, auth_method, engine_mount_point, url, examples and return values; the full list of auth options and their sub-options was not read), the Setting the remote environment page, the no_log section of the logging page, and the precedence page. The community.hashi_vault collection index was only skimmed for its lookup names.
Corrected: the original used `lookup(...).secret.password` with `engine_mount_point='kv'`; the documented default mount is `secret`, and the docs example reads `response.secret.password` from a variable.
Removed as not on a cited page: `ps`/`/proc/<pid>/cmdline` visibility claims, the GitHub Actions snippet, the "lookups are lazy" claim, `amazon.aws.aws_secret`, `azure_keyvault_secret` and `community.general.onepassword` equivalents, controller credential injector and survey claims, the `stdin:` advice, and the fact-cache and `ANSIBLE_DEBUG` gotchas.
Method: documentation only; no commands were run.
