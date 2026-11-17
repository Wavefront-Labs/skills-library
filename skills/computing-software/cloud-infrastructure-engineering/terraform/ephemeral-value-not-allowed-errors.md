---
id: computing-software.cloud-infrastructure-engineering.terraform.ephemeral-value-not-allowed-errors
name: ephemeral-value-not-allowed-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ephemeral-not-allowed, ephemeral-values, write-only-argument, troubleshooting]
level: practitioner
status: verified
description: "Fix Ephemeral value not allowed errors: where ephemeral values may flow, marking variables and outputs ephemeral, write-only arguments, and ephemeralasnull workarounds."
sources: ["https://developer.hashicorp.com/terraform/language/manage-sensitive-data/ephemeral", "https://developer.hashicorp.com/terraform/language/resources/ephemeral#referencing-ephemeral-resources", "https://developer.hashicorp.com/terraform/language/functions/ephemeralasnull"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Ephemeral value not allowed"

The title depends on where the value lands (Terraform 1.17.0):

```
Error: Invalid use of ephemeral value
  on main.tf line 6, in resource "tls_cert_request" "bad":
   6:   private_key_pem = ephemeral.tls_private_key.k.private_key_pem
Ephemeral values are not valid for "private_key_pem", because it is not a
write-only attribute and must be persisted to state.
```
```
Error: Ephemeral value not allowed        # module input not declared ephemeral
This input variable is not declared as accepting a ephemeral values, so it
cannot be set to a result derived from an ephemeral value.

Error: Ephemeral value not allowed        # non-ephemeral output of a child module
This output value is not declared as returning an ephemeral value, so it
cannot be set to a result derived from an ephemeral value.

Error: Ephemeral output not allowed       # ephemeral = true on a root output
Ephemeral outputs are not allowed in context of a root module

Error: Invalid count argument             # count derived from an ephemeral value
The given "count" is derived from an ephemeral value, which means that
Terraform cannot persist it between plan/apply rounds.
```

## Allowed destinations
- `provider` block arguments.
- **Write-only** resource arguments (`*_wo`, e.g. `password_wo`).
- Other `ephemeral` resources' arguments.
- `locals` (become ephemeral automatically).
- `variable` and `output` blocks declared `ephemeral = true` (outputs only in child modules).
- `provisioner` and `connection` blocks.

## Fixes by case
| Case | Fix |
|---|---|
| Normal resource argument (`private_key_pem`, `password`) | switch to the write-only variant (`private_key_pem_wo` + `private_key_pem_wo_version`, `password_wo` + `password_wo_version`) if the provider has it |
| Passing into a module | declare the module variable `ephemeral = true` |
| Returning from a module | `output { ephemeral = true }` (not allowed in root module outputs) |
| Using in `count`/`for_each`, resource names, tags | not possible (`Invalid count argument`, `Invalid use of ephemeral value`); use a non-secret value |
| Need a non-secret attribute of an ephemeral object (e.g. an ID) | `ephemeralasnull()` on an object returns it with the ephemeral parts nulled; a non-ephemeral attribute of a mixed object (`local.obj.id` where only `local.obj.secret` is ephemeral) can also be used directly; or read the value from a normal data source |

## Write-only arguments
```hcl
resource "aws_db_instance" "main" {
  password_wo         = ephemeral.random_password.db.result
  password_wo_version = 2         # change to push a new value
}
```
Runnable local equivalent (tls provider): `private_key_pem_wo = ephemeral.tls_private_key.k.private_key_pem`
with `private_key_pem_wo_version = 1` on `tls_cert_request`. Write-only values are sent to the
provider but never stored; Terraform cannot detect drift on them, hence the version attribute.

## Gotchas
- Requires Terraform >= 1.10 (ephemeral values and resources) / 1.11 (write-only arguments) and
  provider support (both per the Terraform changelogs).
- `nonsensitive()` does not help: `input = nonsensitive(var.pw)` with an ephemeral `var.pw`
  is still `Invalid use of ephemeral value`.
- OpenTofu added ephemeral support in 1.11 (OpenTofu 1.11.0 changelog).

## Verify
- [ ] `terraform validate` passes; plan shows `(write-only attribute)` for the argument; `terraform state pull` contains neither the secret nor the key PEM.

## Checked
- Terraform 1.17.0 with random 3.9.1 and tls (ephemeral `tls_private_key`, `random_password`): every error title and body quoted above was produced by a real config (resource argument, module input, child output, root ephemeral output, count); provisioner `command` and a `local` built from an ephemeral value were accepted; `private_key_pem_wo` plus `private_key_pem_wo_version` planned as `(write-only attribute)` and the state contained neither the key nor an ephemeral variable's value; `ephemeralasnull(var.pw) == null` was `true` and a mixed object output showed `secret = null`; `nonsensitive()` on an ephemeral variable was still rejected.
- Provider schemas (`terraform providers schema -json`) show `*_wo` attributes on `tls_cert_request` and `tls_self_signed_cert`; `password_wo`/`password_wo_version` on `aws_db_instance` were found in the AWS provider docs source. The version gates were read in the Terraform changelogs (1.10 ephemeral values, 1.11 write-only) and the OpenTofu 1.11.0 changelog.
- The allowed-destination list (provider block, write-only arguments, other ephemeral resources, ephemeral variables, provisioner and connection blocks, child-module ephemeral outputs) matches the Terraform `variable` and `output` block reference pages; locals were confirmed by running one.
