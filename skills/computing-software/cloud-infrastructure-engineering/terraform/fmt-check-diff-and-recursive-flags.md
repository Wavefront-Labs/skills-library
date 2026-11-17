---
id: computing-software.cloud-infrastructure-engineering.terraform.fmt-check-diff-and-recursive-flags
name: fmt-check-diff-and-recursive-flags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, fmt-check, fmt-recursive, fmt-diff, fmt-list, terraform-fmt, formatting, ci-check, canonical-format]
level: intro
status: verified
description: "Run terraform fmt the right way in CI and locally: -check for a non-zero exit, -diff to show what is wrong, -recursive for modules, -list=false for quiet, and what fmt deliberately does not touch."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/fmt", "https://developer.hashicorp.com/terraform/language/style"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `fmt -check`, `-diff`, `-recursive`

**Goal:** a formatting gate that fails loudly with a useful diff and never
rewrites files in CI.

## 1. Flags
```bash
terraform fmt                       # rewrite .tf/.tfvars in the current dir, print changed file names
terraform fmt -recursive            # ...and every subdirectory (modules/, examples/)
terraform fmt -check                # exit 3 if any file would change; writes nothing
terraform fmt -check -diff          # ...and print a unified diff of what it would change
terraform fmt -list=false -write=false   # NOT silent: prints the formatted text of the files it processes; use -check instead
terraform fmt - < main.tf           # format stdin to stdout (editor integration)
terraform fmt modules/vpc           # a specific dir, or a single file
```
Exit codes with `-check` (checked on 1.9.8): 0 formatted, 3 needs formatting, and **2** when a file has a parse
error (not 1). Note **3**, not 1 — CI scripts that test `== 1` miss it. `-check -diff` prints a unified diff (`--- old/main.tf` / `+++ new/main.tf`) and still exits 3.

## 2. CI gate
```yaml
- run: terraform fmt -check -diff -recursive
```
Keep it a separate, fast job that does not need `init` (fmt is purely syntactic;
no providers, no backend; the tests here ran without `init`). Pin the Terraform version so the gate's output does not shift between releases.

## 3. What fmt does and does not do
Does (checked): two-space indentation, aligns `=` in consecutive attribute groups (`type    = string` / `default = "x"`), and converts `"${var.x}"` to
`var.x` where the interpolation is the whole string.
Does **not**: reorder attributes or blocks, wrap long lines, format inside heredocs
or `.tftpl` files, touch `.tf.json`, or enforce naming — that is tflint's job. A heredoc body
(`      keep   me`) was left untouched in a test.
Files with syntax errors are reported (exit 2); the other files in the run were still formatted.

## 4. Editor and pre-commit
- Editors can run `terraform fmt` on save through the HashiCorp Terraform language server extension; check your editor's docs.
- pre-commit: `antonbabenko/pre-commit-terraform` ships a `terraform_fmt` hook ("Rewrites all Terraform configuration files to a canonical format", per its hooks file).
- OpenTofu: `tofu fmt` is a separate binary; mixed teams should agree on one binary for the gate.

## Gotchas
- `-recursive` skipped `.terraform/` in a test (a tab-indented file under `.terraform/modules/x/` stayed unformatted and unlisted). Still, run from the module root, not `/`.
- A `.tfvars.json`/`.tf.json` file is ignored (not an error).
- `fmt` preserved CRLF line endings in a test (a CRLF file that needed formatting was fixed and kept `
`; a CRLF file already well formatted was not listed), so it will not normalise them for you. Set `.gitattributes` `*.tf text eol=lf` so Windows checkouts do not mix endings.
- `fmt -check` on a file with a parse error exits 2 and names the file; fix the
  syntax first.

## Verify
- [ ] `terraform fmt -check -recursive; echo $?` prints 0 on a clean tree and 3 after you indent a line with a tab.
- [ ] CI job fails on exit 3 and the log shows the `-diff` output.
