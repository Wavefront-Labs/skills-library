---
id: computing-software.cloud-infrastructure-engineering.terraform.compact-warnings-and-no-color-output
name: compact-warnings-and-no-color-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, compact-warnings, no-color, ci-logs, terraform-plan, terraform-apply]
level: practitioner
status: verified
description: "Make plan/apply output readable in CI logs: -no-color to strip ANSI codes, -compact-warnings to collapse warning walls, and when to switch to -json instead."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://developer.hashicorp.com/terraform/internals/machine-readable-ui"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `-no-color` and `-compact-warnings`

## The flags
| Flag | Accepted by | Effect |
|---|---|---|
| `-no-color` | init, plan, apply, destroy, show, output, validate, console, refresh, import, test, fmt, providers, graph, get, and subcommands such as `state list` and `workspace list` | Drops ANSI escape codes. |
| `-compact-warnings` | init, plan, apply, destroy, show, output, validate, console, refresh, import, test, get (rejected by `fmt`, `providers`, `graph`) | Warnings print as a short list (summary line plus location), bodies are dropped; errors stay in full. |

(Flag acceptance was tested against Terraform 1.17.0; `terraform help <cmd>` lists the flags of your version.)

```bash
terraform plan -no-color -compact-warnings -out=tfplan | tee plan.txt
```

## When to use which
- **Log viewers or files that do not render ANSI escape sequences** (plain files, PR
  comments, Markdown summaries, grep pipelines): `-no-color`. Otherwise sequences like
  `ESC[0mESC[1m` appear in every line and break `grep`; Terraform emitted them even when
  stdout was redirected to a file. Keep colour only where your log viewer renders it.
- **Deprecation storms** after a provider upgrade (hundreds of `Warning: Argument is
  deprecated` blocks hiding the real diff): `-compact-warnings`. Fix the warnings
  later; do not let them bury the plan.
- **Anything a program parses**: neither. Use `-json` (machine-readable UI) or
  `terraform show -json tfplan`; human output is not a stable interface.

## Making it the default in automation
```bash
export TF_CLI_ARGS="-no-color"            # every command
export TF_CLI_ARGS_plan="-compact-warnings"
export TF_IN_AUTOMATION=1                 # drops the "terraform apply" next-step hints from plan output
```
`TF_CLI_ARGS` is appended to the command; a command that does not accept the flag
fails (`TF_CLI_ARGS="-compact-warnings" terraform fmt` printed the fmt usage text), so
scope with `TF_CLI_ARGS_<cmd>` when in doubt.

## Gotchas
- `-no-color` on `show` matters too: `terraform show -no-color tfplan > plan.txt`
  for an artifact people read.
- `-compact-warnings` hides warning *bodies*. Before a provider major upgrade, run
  once without it and read every deprecation.
- Colour codes in a saved text file make diffs between two plans useless; always
  save the `-no-color` form.

## Verify
- [ ] `grep -c $'\x1b\[' plan.txt` returns 0 (it returned 31 for the same plan saved without `-no-color`, even though the output was redirected to a file).
- [ ] Warnings appear as a short summary list in the CI log, errors still in full.
- [ ] Nothing in CI parses human plan text; parsers read `show -json`.

## Checked
- Terraform 1.17.0 on Windows: every flag-acceptance entry in the table was tested by running the command with the flag and looking for a flag error or usage text (`fmt`, `providers`, `graph` reject `-compact-warnings`; `import` and `output` accept it); with two failing `check` blocks, `apply -compact-warnings` printed a `Warnings:` list of two lines plus `To see the full warning notes, run Terraform without -compact-warnings.`; `plan -out` plus `TF_IN_AUTOMATION=1` removed the `terraform apply` hint (count 1 -> 0); `TF_CLI_ARGS="-no-color"` removed all escape codes; `TF_CLI_ARGS_plan="-compact-warnings"` applied only to plan; plain redirected output still contained escape codes (31 matches) until `-no-color` was passed; `plan -json` output was an NDJSON stream with `-compact-warnings` accepted.
- Claims about how particular CI log viewers render colour were removed rather than asserted.
