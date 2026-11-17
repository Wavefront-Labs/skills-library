---
id: computing-software.cloud-infrastructure-engineering.terraform.evaluating-expressions-with-console-stdin
name: evaluating-expressions-with-console-stdin
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, console-eval, console-stdin, console-pipe, terraform-console, expression-debugging, repl, scripting, state-query]
level: practitioner
status: verified
description: "Script terraform console by piping expressions on stdin: query state values, test functions and locals non-interactively, pass -var, and know what console can and cannot evaluate."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/console", "https://developer.hashicorp.com/terraform/language/functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating expressions with `console` on stdin

**Goal:** answer "what does this expression evaluate to against the real
state?" in one shell line, and embed that in scripts.

## 1. Interactive vs piped
```bash
terraform console                               # REPL; exit with Ctrl-D or `exit`
echo 'local.subnet_cidrs' | terraform console   # one expression, prints result, exits
terraform console <<'EOF'
cidrsubnet("10.0.0.0/16", 8, 3)
[for s in terraform_data.private : s.id]
EOF   # prints only the last result
```
Piped stdin is read line by line: each line is one expression, and only the
**last** line's result is printed (run: `cidrsubnet(...)` then `var.x` printed only
`"dflt"`). The first line that errors stops the run with exit status 1 and prints
nothing for the earlier lines. Run one expression per invocation, or `join`/wrap
several values into one final expression, e.g. `[a, b, c]`. A multi-line
expression piped on stdin fails (`Missing expression`, end of file), so keep
piped expressions on one line; interactive multi-line input arrived in 1.9.

## 2. What it sees
- Current **state** (it reads the backend, so it needs init and any backend
  credentials). There is no `-lock` flag (`flag provided but not defined: -lock`);
  `-state=PATH` is a legacy option for the local backend only.
- Variables: `-var`, `-var-file`, `TF_VAR_` and `*.auto.tfvars` are honoured (an
  `.auto.tfvars` value beat `TF_VAR_x`, the normal precedence). An unset required
  variable did not prompt on piped input: `var.req` printed `(known after apply)`
  with exit status 0.
- Resources and data sources not yet in state are not available to plain console.
  Data sources are **not** re-read; console uses their last stored values (a
  `local_file` data source returned the pre-change content). Use `-plan` to see
  planned values.
- Provider-defined functions need initialised providers (introduced in 1.8; see
  the 1.8 changelog).

## 3. Scripting recipes
```bash
# dump a map as JSON for other tools (console prints the JSON as a quoted string)
echo 'jsonencode(local.common_tags)' | terraform console | jq -r . | jq .
# check a validation expression before committing it
echo 'can(regex("^[a-z0-9-]{3,63}$", "My-Bucket"))' | terraform console
# type of a module output
echo 'type(local.subnets)' | terraform console
# which instance keys exist
echo 'keys(terraform_data.app)' | terraform console   # for_each instance keys
```
An erroring expression exits with status 1 (checked), so `set -e` works; stderr carries the diagnostic.

## 4. Options
`-var`, `-var-file`, `-state=PATH` (local backend only), `-plan` (1.7+: evaluate
against a fresh **plan**, so new resources are partly known and `count`/`for_each`
results are visible), `-scope=module.child` (1.16+, evaluate inside a module instance).

## Gotchas
- Console sees sensitive values as `(sensitive value)`; wrap with
  `nonsensitive(...)` to inspect (both checked).
- Multiple expressions in a heredoc do NOT each print: only the last result is shown
  and an error aborts the run.
- In HCL a regex backslash is
  written doubled: `regex("^arn:aws:iam::(\\d{12}):", s)` (a single `\d` is
  `Invalid escape sequence`).

## Verify
- [ ] `echo '1 + 1' | terraform console` prints `2`.
- [ ] `echo 'local.<name>' | terraform console` prints the value you expected for a non-trivial local.

## Checked
- Docs page (developer.hashicorp.com/terraform/cli/commands/console) confirms: exit with `exit`/Ctrl-C/Ctrl-D, only the final piped result prints unless an earlier command errors, console holds the state lock.
- Terraform 1.17.0, scratch dir with locals and a sensitive variable: `echo '1 + 1' | terraform console` prints `2`; a two-line stdin printed only the last result; an error line aborted with exit status 1 and nothing printed for earlier lines; a multi-line `{ ... }` on stdin failed with `Missing expression`; `console < file` with one expression worked; `-var`, `-state=PATH` accepted, `-lock=false` rejected (`flag provided but not defined`); `var.sec` printed `(sensitive value)` and `nonsensitive(var.sec)` the value; `jsonencode`, `type()`, grouping `...`, `cidrsubnets`, `flatten`, `try`, `can(regex())` ran; the regex line needs a doubled backslash (checked via a Python subprocess).
- Data sources: plain console returned the stale stored `local_file` content, `-plan` the new content.
- Changelogs (v1.7, v1.9, v1.16) for `-plan`, interactive multi-line input and `-scope`. Provider-defined functions: v1.8 changelog.
