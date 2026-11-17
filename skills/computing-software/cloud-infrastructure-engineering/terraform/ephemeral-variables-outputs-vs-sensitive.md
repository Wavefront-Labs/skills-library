---
id: computing-software.cloud-infrastructure-engineering.terraform.ephemeral-variables-outputs-vs-sensitive
name: ephemeral-variables-outputs-vs-sensitive
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ephemeral-variable, ephemeral-input, ephemeral-output, ephemeral-vs-sensitive, sensitive, secrets]
level: advanced
status: verified
description: "Mark variables and module outputs ephemeral (Terraform 1.10+) so values never reach state or plan files, and choose between ephemeral and sensitive."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#exclude-values-from-state", "https://developer.hashicorp.com/terraform/language/values/outputs#ephemeral-avoid-storing-values-in-state-or-plan-files", "https://developer.hashicorp.com/terraform/language/block/ephemeral"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral variables and outputs vs `sensitive`

## sensitive vs ephemeral
| | `sensitive = true` | `ephemeral = true` |
|---|---|---|
| Shown in plan output | as `(sensitive value)` | cannot reach a stored attribute; provisioner output is replaced by `(output suppressed due to ephemeral value in config)` |
| Stored in state | **yes, plaintext** | no |
| Stored in saved plan file (`show -json`) | yes (before/after values are in the JSON) | no |
| Usable anywhere | yes | only in ephemeral contexts |
Sensitive is redaction; ephemeral is non-persistence.

## Ephemeral input variable
```hcl
variable "db_password" {
  type      = string
  ephemeral = true
}
```
Allowed uses: provider configuration, `locals`, other ephemeral variables/outputs,
ephemeral resources, **write-only arguments** (`password_wo`), provisioner/connection
blocks. Using it in a normal resource argument errors:
`Invalid use of ephemeral value` ("... because it is not a write-only attribute and must
be persisted to state"); passing it to a child-module variable that is not declared
`ephemeral = true` errors `Ephemeral value not allowed`. `nonsensitive()` does not remove
the ephemeral mark.

Saved plans: values for ephemeral variables are not stored, so they must be
supplied again at `terraform apply tfplan` (`-var`/`TF_VAR_`); without them apply fails
with `No value for required variable` ("The ephemeral input variable "pw" was set during
the plan phase, and so must be set again during apply").

## Ephemeral output (child modules only)
```hcl
# modules/creds/outputs.tf
ephemeral "random_password" "api" { length = 16 }
output "token" {
  value     = ephemeral.random_password.api.result
  ephemeral = true
}
```
(A secret-store ephemeral resource such as `ephemeral.vault_kv_secret_v2.api.data["token"]`
works the same way.) Root-module outputs cannot be ephemeral: `Error: Ephemeral output not
allowed ... in context of a root module`. Consumers of `module.creds.token` inherit
ephemerality: a non-ephemeral output that reads it fails with `Ephemeral value not allowed`
("This output value is not declared as returning an ephemeral value").

## Choosing
- Secret only feeds a provider (API token, Vault token): **ephemeral**.
- Secret sets a resource password and the provider has a `_wo` argument: ephemeral +
  write-only.
- Secret must be readable later from state (e.g. by `terraform output`): sensitive
  (and protect state).
- `terraform.workspace`/IDs etc.: neither.

## Gotchas
- Requires Terraform >= 1.10 (Terraform 1.10 changelog; OpenTofu 1.11.0 changelog for
  OpenTofu); older versions reject the argument.
- `ephemeralasnull(x)` turns an ephemeral value into null for places that must not
  be ephemeral (see ephemeral-resources skill); on an object it nulls only the
  ephemeral attributes, and a non-ephemeral attribute of the same object
  (`local.obj.id`) is usable directly.
- An ephemeral value used in `nonsensitive()` is still ephemeral.

## Verify
- [ ] `terraform state pull | grep -c <secret>` returns 0 (it printed 0 for an ephemeral variable and for an ephemeral output; a sensitive variable was present in state).
- [ ] `terraform show -json tfplan | grep -c <secret>` returns 0.

## Checked
- Terraform 1.17.0 (random 3.9.1, tls): an `ephemeral = true` variable used in a provisioner, in `ephemeralasnull()` and in `private_key_pem_wo` applied cleanly and the secret was absent from `terraform state pull`, `terraform show -json` of a saved plan and the binary plan (zip entries searched); `apply p.plan` without `-var` failed with `No value for required variable` quoted above and succeeded with it; a sensitive variable's value was in the state (`grep -c` returned 2); child-module ephemeral output built from `ephemeral.random_password` was usable in a provisioner (output shown as `(output suppressed due to ephemeral value in config)`); root `ephemeral = true` output, module input without `ephemeral` and non-ephemeral output of an ephemeral value produced the errors quoted.
- Version gates: Terraform 1.10 changelog (ephemeral resources, ephemeral variables and outputs, `ephemeralasnull`), 1.11 (write-only attributes), OpenTofu 1.11.0 changelog (ephemeral values).
