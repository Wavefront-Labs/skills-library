---
id: computing-software.cloud-infrastructure-engineering.terraform.tf-cli-args-environment-variables
name: tf-cli-args-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tf-cli-args, tf-cli-args-plan, tf-cli-args-apply, environment-variables, ci, default-flags, var-file-injection, wrapper-scripts]
level: practitioner
status: verified
description: "Inject default flags with TF_CLI_ARGS and TF_CLI_ARGS_<command> (var files, parallelism, -no-color) in CI and wrappers; ordering rules, quoting, and the ways it bites."
sources: ["https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_cli_args-and-tf_cli_args_name", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `TF_CLI_ARGS` and `TF_CLI_ARGS_<name>`

**Goal:** apply the same flags to every Terraform invocation in a pipeline or
wrapper without editing each command line.

## 1. Semantics
```bash
export TF_CLI_ARGS="-no-color"                     # every command
export TF_CLI_ARGS_plan="-var-file=env/prod.tfvars -parallelism=20"
export TF_CLI_ARGS_apply="-var-file=env/prod.tfvars -parallelism=20"
export TF_CLI_ARGS_init="-input=false -backend-config=env/prod.tfbackend"
terraform plan -out=tfplan
# effective: terraform plan -no-color -var-file=env/prod.tfvars -parallelism=20 -out=tfplan
```
- Values are inserted **after** the subcommand and **before** explicit arguments;
  explicit arguments therefore override for flags where last-wins applies
  (`-var a=explicit` beat `TF_CLI_ARGS_console="-var a=env"`; `-var-file=f2` beat an
  env `-var-file=f1`), and accumulate for repeatable flags (`-var-file`).
  With both variables set, the final argv was `console -var a=sub -var a=g -var a=x`
  (the `_<name>` value first, then `TF_CLI_ARGS`, then your explicit flags), so the
  global `TF_CLI_ARGS` value won over the command-specific one.
- `TF_CLI_ARGS` applies to every command including `init`, `state`, `console`,
  `workspace`, `version` and `fmt`; a flag that a subcommand does not accept makes it
  **error** (`TF_CLI_ARGS=-parallelism=5` broke `terraform version` and `fmt` with
  `Failed to parse command-line flags`) — keep the global one to universally accepted
  flags (`-no-color` worked everywhere I tried, see gotchas).
- `TF_CLI_ARGS_<name>` uses the first word of the command: `plan`, `apply`,
  `destroy`, `init`, `validate`, `import`, `console`, `test`, `output`, `refresh`.
  Sub-sub-commands join the words with an underscore: `TF_CLI_ARGS_state_list`
  and `TF_CLI_ARGS_workspace_list` were read, while `TF_CLI_ARGS_state` and
  `TF_CLI_ARGS_workspace` were ignored for `state list` and `workspace list`.
- Parsing is shell-like: spaces split; quote values with spaces (`-var='a=x y'` and
  `-var "a=x y"` both gave `x y`).

## 2. Uses
- Per-environment var files in CI without touching the Makefile.
- `-lock-timeout=5m` on all `apply`/`destroy` jobs.
- `-compact-warnings` for quieter logs.
- Wrapper scripts that must pass extra flags to user-invoked
  commands.

## 3. Debugging "where did that flag come from"
```bash
env | grep ^TF_CLI_ARGS
TF_LOG=INFO terraform plan 2>&1 | grep "CLI"      # CLI args: (your argv), TF_CLI_ARGS_plan value, CLI command args: (final)
```

## Gotchas
- `TF_CLI_ARGS="-no-color"` did NOT break `version`, `fmt -check`, `providers`,
  `validate`, `output` or `state list` (Terraform 1.9.8 and 1.17.0). Flags that those
  commands lack (for example `-parallelism`) do break them, so prefer per-command
  variables for anything beyond `-no-color`.
- `TF_CLI_ARGS_apply="-auto-approve"` turns every apply, including a developer's,
  into an unprompted one if the variable leaks into their shell.
- A relative `-var-file` is resolved against the directory chosen with `-chdir` (checked
  with `-var-file=s.tfvars` on the command line and `-chdir=sub`).

## Verify
- [ ] `TF_LOG=INFO terraform plan 2>&1 | grep "CLI command args"` shows the injected flags in the expected position.
- [ ] `terraform version` still works with your global `TF_CLI_ARGS` set.

## Checked
- Terraform 1.17.0 and 1.9.8 with `hashicorp/local` and `hashicorp/random`: ran `TF_CLI_ARGS` and `TF_CLI_ARGS_<name>` with `-var`, `-var-file`, `-parallelism`, `-no-color`, quoting forms, `TF_CLI_ARGS_state`/`_state_list`/`_workspace_list`, `TF_LOG=INFO` (read the three log lines), `-chdir` with a relative `-var-file`, and unknown flags on `version`/`fmt`.
- Corrections: `-no-color` in `TF_CLI_ARGS` does not break `version`, `fmt` or `providers`; sub-sub-commands use `TF_CLI_ARGS_state_list` (not `_state`); the log line to grep is `CLI command args`; `-var-file` follows `-chdir`; the global `TF_CLI_ARGS` value beat the `_<name>` one. Removed unchecked HCP, Terragrunt and OpenTofu claims.
