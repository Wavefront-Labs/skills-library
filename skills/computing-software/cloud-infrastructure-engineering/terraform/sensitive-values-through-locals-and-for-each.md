---
id: computing-software.cloud-infrastructure-engineering.terraform.sensitive-values-through-locals-and-for-each
name: sensitive-values-through-locals-and-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, sensitive-local, sensitive-locals, for-each-sensitive, nonsensitive, sensitive-propagation]
level: advanced
status: docs-checked
description: "Trace how sensitivity propagates to derived values, avoid sensitive values in for_each with a for expression, and use nonsensitive() only where it is safe."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#suppressing-values-in-cli-output", "https://developer.hashicorp.com/terraform/language/functions/nonsensitive", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitivity through locals and `for_each`

## Propagation
- Terraform tracks when an expression derives a new value from a sensitive value, so the result is
  also marked sensitive. Example from the docs: `jsondecode(var.mixed_content_json)` in a local, and
  `local.mixed_content["password"]`, are both sensitive when the variable is.
- Most functions return a sensitive result when given an argument with any sensitive content.
- In `terraform console` such values print as `(sensitive value)`.
- Mark a variable `sensitive = true` to keep it out of CLI output. Terraform still stores the values
  of sensitive variables in state; the `ephemeral` argument omits a variable from state and plan
  files, with restrictions on the values you can assign it.
- Sensitive outputs are also stored in state; `terraform output` with `-json` or `-raw` shows them in plain text.

## for_each and sensitive values
You cannot use sensitive values (sensitive input variables, sensitive outputs, sensitive resource
attributes) as `for_each` arguments. Terraform uses the `for_each` value to identify the instance
and always discloses it in UI output, and returns an error if you try. A value derived from
sensitive data is usually sensitive too.

Workaround from the docs: when the keys are not sensitive but the values are, build the
`for_each` value with a `for` expression instead of `keys()`:
```hcl
for_each = toset([for k, v in local.map : k])
```
where `local.map` is an object with sensitive values but non-sensitive keys.

Other `for_each` rules on the same page: keys or set members must be known values (otherwise
an error about dependencies that cannot be determined before apply, with a `-target` hint);
keys cannot rely on impure functions such as `uuid`, `bcrypt` or `timestamp`; lists and tuples are not
implicitly converted to sets, so use `toset()`.

## nonsensitive()
Available in Terraform v0.15 and later. It removes the sensitive marking from a value and
therefore exposes it.
- Use only when you derived a value from a sensitive one in a way that eliminates the sensitive
  parts, for example a SHA256 hash judged safe by your threat model, or a non-secret
  fragment such as a username from a mixed JSON document:
```hcl
username_from_json = nonsensitive(local.mixed_content["username"])
```
- It is your responsibility that the argument contains no sensitive content; an inappropriate call is
  a bug in your module. Passing the whole variable or the password discloses it.
- On a value that is not sensitive it errors (`Invalid function argument`: "the given value is not
  sensitive, so this call is redundant" in the page's console example).
- Put a comment next to each call explaining why it is safe and which invariants to preserve.

## Gotchas
- Variable definition files containing sensitive values should be ignored in your VCS.

## Checked
Date: 2026-11-07. Read in full: the `for_each` meta-argument page (limitations on values, expressions, referring to instances), the `nonsensitive` function page and the "Use input variables" page (Sensitive values in variables). Also read the Sensitive values in outputs section of the outputs page. Confirmed: derived-value propagation, sensitive/ephemeral wording, for_each prohibition and reason, the `toset([for k,v ...])` workaround, nonsensitive availability, warnings, examples and the redundant-call error. Corrections: the draft's `toset(nonsensitive(keys(var.db_users)))` pattern was not on the pages and its claim that a sensitive map is not wholly sensitive was removed; replaced with the page's `for` expression approach. Trims: the quoted `Invalid for_each argument` text, `merge`/`jsonencode`/`templatefile` claims, "older versions error" note, `Output refers to sensitive values`, module-input and `count = length(...)` gotchas, the split-variable advice and the grep Verify steps.
Method: documentation only; no commands were run.
