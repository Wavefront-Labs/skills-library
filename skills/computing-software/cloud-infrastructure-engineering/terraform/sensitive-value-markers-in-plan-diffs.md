---
id: computing-software.cloud-infrastructure-engineering.terraform.sensitive-value-markers-in-plan-diffs
name: sensitive-value-markers-in-plan-diffs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, sensitive-plan-diff, sensitive-values, plan-output, plan-review]
level: practitioner
status: verified
description: "Review plans when attributes show (sensitive value): what triggers redaction, how to tell whether a sensitive field actually changed, and safe ways to inspect it."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output", "https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/language/functions/nonsensitive"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `(sensitive value)` in plan diffs

## What triggers it
- Attribute marked `Sensitive` in the provider schema (passwords, private keys).
- Any expression derived from a `sensitive = true` variable, output, or local.
- A whole nested block whose schema contains sensitive attributes shows `# At least one
  attribute in this block is (or was) sensitive, so its contents will not be displayed.`
  (wording from Terraform's `jsonformat` renderer source).

```
  # terraform_data.db will be updated in-place
  ~ resource "terraform_data" "db" {
      ~ input  = {
          ~ env      = "dev" -> "prod"
          ~ password = (sensitive value)
        }
        # ... (other attributes)
    }
```
(Terraform 1.17.0 output for a map whose `password` value came from a sensitive variable. On a
provider-marked sensitive attribute such as a database password the line has the same form.)

## Did it actually change?
The human plan shows `~ password = (sensitive value)` when the value differs (old != new);
when old and new are equal the attribute stays under `# (N unchanged attributes hidden)`
(tested: same password, only `env` changed, no password line). The line can also appear when only
the **sensitivity marking** changed; Terraform then adds a warning above it:
```
# Warning: this attribute value will be marked as sensitive and will not
# display in UI output after applying this change. The value is unchanged.
```
so read the warning before assuming a rotation.

Check without printing the secret:
```bash
terraform show -json tfplan | jq '.resource_changes[]
  | select(.address=="terraform_data.db")
  | {before_sensitive: .change.before_sensitive.input.password,
     after_sensitive: .change.after_sensitive.input.password,
     same: (.change.before.input.password == .change.after.input.password)}'
```
(For a top-level attribute use `.change.before_sensitive.<attr>`; for the `terraform_data`
example the path is under `input`.)
The JSON contains the real values (the plan file is a secret too). `same: true` with
a diff line means only the sensitivity marking changed; applying is a no-op on the
object.

## Common surprises
- **Whole value redacted:** a map or object keeps per-element marks (`tomap`, `merge` and a
  `for` expression with one sensitive element all printed `~ b = (sensitive value)` next to
  clear siblings), but `jsonencode()` of such a map becomes one `(sensitive value)` string, and
  an attribute the provider marks sensitive is redacted as a whole. Fix the source with
  `nonsensitive()` only when you are certain the value is not secret.
- **`terraform_data.output` leaked:** with a sensitive `input`, Terraform 1.17.0 still printed
  the old value of the computed `output` attribute in clear (`~ output = "one" -> (known after
  apply)`); `before_sensitive` marked only `input`. Do not rely on redaction for values copied
  through `terraform_data`.
- **for_each over sensitive values** errors outright (`Sensitive values, or values
  derived from sensitive values, cannot be used as for_each arguments`); use
  non-sensitive keys.
- **Perpetual diff on a sensitive attribute**: provider normalises the value
  (e.g. trailing newline in a key). Compare the raw JSON values without printing them:
  `jq '.resource_changes[].change.before.x | @base64'` (jq's `@base64` is encoding, not hashing).

## Rules
- Plan JSON and binary plan files contain the clear text; protect them like state.
- Never `nonsensitive()` a real secret just to read a diff.

## Verify
- [ ] Every `(sensitive value)` diff is either an intended rotation or confirmed sensitivity-only.
- [ ] Plan artifacts with secrets are access-restricted and expire.

## Checked
- Terraform 1.17.0, `terraform_data` with a sensitive variable: a map/object element, `tomap`, `merge`, and a `for` expression all gave per-element `(sensitive value)`, `jsonencode` gave a fully redacted string; changing only `env` hid the unchanged password; making an existing variable `sensitive = true` gave the `Warning: this attribute value will be marked as sensitive ... The value is unchanged.` line with `~ input = (sensitive value)`; `toset([var.sec])` in `for_each` failed with `Sensitive values, or values derived from sensitive values, cannot be used as for_each arguments`; `terraform show -json` held the real values with `before_sensitive`/`after_sensitive` flags and the jq recipe ran (`same` was false for a changed value); `nonsensitive()` on one element removed the redaction for it; the `terraform_data.output` leak above was observed in the plan text.
- Source: the block-redaction sentence and the warning texts are from `internal/command/jsonformat/computed/renderers/sensitive_block.go` and `sensitive.go` in hashicorp/terraform.
