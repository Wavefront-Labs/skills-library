---
id: computing-software.devops-ci-cd.nomad.vault-block
name: vault-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, vault-block, vault, vault-token, change-mode, allow-token-expiration, vault-namespace, disable-file, secrets, workload-identity, hcl]
level: practitioner
status: docs-checked
description: "Give Nomad tasks a Vault token with the vault block, covering role, change_mode, env, disable_file, allow_token_expiration, namespace and the private-token template pattern."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/vault.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad vault block

`vault` (job, group or task; merged with task beating group beating job) makes the client fetch and renew a Vault token for the task. The token is written to `secrets/vault_token` and exported as `VAULT_TOKEN` (plus `VAULT_NAMESPACE` when the cluster uses Vault namespaces). `template` blocks can then read Vault secrets.

```hcl
vault {
  role        = "prod"
  change_mode = "signal"
  change_signal = "SIGUSR1"
}
```

## Parameters (defaults)
- `role` - Vault role used with JWT and workload identity; falls back to the client's `create_from_role`.
- `cluster` (`"default"`) - Enterprise only (ignored in Community Edition); matches the agent `vault.name`.
- `namespace` - Enterprise only; scope the token to a Vault namespace such as `engineering/frontend`.
- `change_mode` (`"restart"`) - when the token changes: `noop`, `restart`, `signal` (needs `change_signal`).
- `env` (`true`) - set `VAULT_TOKEN` and `VAULT_NAMESPACE`.
- `disable_file` (`false`) - skip writing `secrets/vault_token`. Warning: the `secrets` path is not shared with `image`-isolated tasks but is accessible to `chroot` and `none` isolation.
- `allow_token_expiration` (`false`) - stop renewing the token. Use only for one-shot reads at task start or a short-lived prestart task. A long-running task with `template` secrets must not set it: the token expires and the template runner keeps failing until its `vault_retry` attempts run out, then the task fails. With Workload Identity the client detects non-renewable tokens (for example batch tokens) and sets it implicitly; the legacy auth workflow cannot.

If renewal fails (Vault outage), the client tries to get a new token, rewrites the file, then applies `change_mode`.

## Private token pattern
Keep a powerful token away from the task and let templates issue narrower secrets:
```hcl
vault {
  role         = "prod"
  change_mode  = "noop"
  env          = false
  disable_file = true
}
template {
  data        = <<-EOH
{{with secret "auth/token/create/nomad-job" "policies=examplepolicy"}}{{.Auth.ClientToken}}{{ end }}
EOH
  destination = "${NOMAD_SECRETS_DIR}/examplepolicy.token"
  change_mode = "noop"
  perms       = "600"
}
```
With `change_mode = "noop"` on that template the workload must detect file changes itself; a certificate template with the default `restart` makes Nomad restart the task on reissue.

## Checked

2026-11-03. Confirmed against the vault job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
