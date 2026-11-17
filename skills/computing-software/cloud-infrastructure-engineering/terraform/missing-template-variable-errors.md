---
id: computing-software.cloud-infrastructure-engineering.terraform.missing-template-variable-errors
name: missing-template-variable-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, template-variable-error, templatefile, template-escaping, troubleshooting]
level: practitioner
status: verified
description: "Fix templatefile errors: vars map does not contain key, unescaped shell ${VAR}, Invalid template control keyword, and template files referencing undeclared values."
sources: ["https://developer.hashicorp.com/terraform/language/functions/templatefile", "https://developer.hashicorp.com/terraform/language/expressions/strings#escape-sequences"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# templatefile variable errors

## `vars map does not contain key`
```
Error: Invalid function argument
Invalid value for "vars" parameter: vars map does not contain key "region",
referenced at templates/app.conf.tftpl:1,8-14.
```
Every `${name}` in the template must be a key of the vars map. Templates cannot see
`var.*`, `local.*` or resources directly. Fix: add the key, or escape it if it was
meant literally.

## Shell variables in templates
Shell's `${HOME}` looks like a template interpolation:
```bash
echo "${HOME}"       # template error: vars map does not contain key "HOME"
echo "$${HOME}"      # renders as ${HOME}
echo "$HOME"         # fine: no braces, no interpolation
```
Same for `%{`: write `%%{` to emit a literal `%{`.

## `Invalid template control keyword`
A misspelled keyword (`%{ iff a }`) gives `Invalid template control keyword; "iff" is not a
valid template control keyword`. Other directive mistakes have their own messages:
`%{ for ... }` without `%{ endfor }` gives `Unexpected end of template; The for directive ...
is missing a corresponding endfor directive`, and `%{ else if b }` (not supported; nest
`%{ if }` instead) gives `Extra characters in else marker`. Spacing is allowed: `%{if a}1%{endif}`
renders fine.

## Type errors inside templates
`Invalid template interpolation value; Cannot include the given value in a string template:
string required, but have tuple.` A list or map was interpolated directly. Use `${join(",", items)}`, `${jsonencode(obj)}`, or iterate.

## Unknown values
If any var value is unknown at plan, the whole rendered string is
`(known after apply)`, which can force replacements (e.g. user_data). Pass only known
values where possible.

## Debug quickly
```bash
echo 'templatefile("templates/app.conf.tftpl", { region = "eu-west-1", ports = [80] })' | terraform console
```

## Gotchas
- `templatefile` reads the file at plan time; generated files created during apply
  cannot be templates (`no file exists at "templates/gen.tftpl"; this function works only
  with files that are distributed as part of the configuration source code`).
- Windows line endings in templates end up in output (CRLF in shell scripts breaks
  them); enforce LF with `.gitattributes`.

## Verify
- [ ] Console rendering of the template matches expectation for a test vars map.

## Checked
- Terraform 1.17.0 via `terraform console` and a plan: the missing-key error (quoted with the real `referenced at` position), `${HOME}` failing with `vars map does not contain key "HOME"`, `$${HOME}` rendering `${HOME}`, `$HOME` and `%%{` rendering literally, a missing `endfor`, `%{ else if }`, a misspelled keyword, a tuple interpolated directly, `join()`/`jsonencode()` rendering `list=a,b j={"a":1}`, an unknown `terraform_data.x.id` var making the whole rendered `input` `(known after apply)`, a template file produced by `local_file` failing with `no file exists at`, and CRLF line endings surviving into the output (`^M` shown by `cat -A`) all ran as quoted.
