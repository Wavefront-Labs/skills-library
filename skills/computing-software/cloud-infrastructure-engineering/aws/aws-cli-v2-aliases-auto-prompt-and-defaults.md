---
id: computing-software.cloud-infrastructure-engineering.aws.aws-cli-v2-aliases-auto-prompt-and-defaults
name: aws-cli-v2-aliases-auto-prompt-and-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-cli, cli-aliases, auto-prompt, cli-v2, cli-pager, cli-binary-format]
level: practitioner
status: docs-checked
description: "Work faster with AWS CLI v2: command aliases in the alias file, auto-prompt, pager and output settings, and the v1-to-v2 behaviour changes that break scripts."
sources: ["https://github.com/aws/aws-cli/blob/v2/awscli/alias.py", "https://github.com/aws/aws-cli/blob/v2/awscli/topics/config-vars.rst", "https://github.com/aws/aws-cli/blob/v2/awscli/clidriver.py", "https://github.com/aws/aws-cli/blob/v2/awscli/autoprompt/factory.py", "https://github.com/aws/aws-cli/blob/v2/awscli/data/cli.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS CLI v2: aliases, auto-prompt and defaults

## Aliases
File: `~/.aws/cli/alias` (create the `cli` directory if missing).
```ini
[toplevel]
whoami = sts get-caller-identity
running = ec2 describe-instances --filters Name=instance-state-name,Values=running --query 'Reservations[].Instances[].[InstanceId,InstanceType,Tags[?Key==`Name`]|[0].Value]' --output table
myip =
  !f() {
    curl -s https://checkip.amazonaws.com
  }; f
sg-allow-me =
  !f() {
    aws ec2 authorize-security-group-ingress --group-id "$1" --protocol tcp --port "${2:-22}" \
      --cidr "$(curl -s https://checkip.amazonaws.com)/32"
  }; f
```
- `aws whoami`, `aws running --profile prod`. Global options such as `--profile` are processed before the alias runs.
- Aliases starting with `!` are external commands run through the system shell (`shell=True`), so write them for the shell you use; the bash-style examples above will not run in cmd.exe.
- Service-level aliases go under a `[command ec2]` section; top-level ones under `[toplevel]`.

## Auto-prompt
```bash
aws --cli-auto-prompt          # interactive completion of commands, params, resource names
export AWS_CLI_AUTO_PROMPT=on-partial   # prompt only when the command is incomplete
```
Config: `cli_auto_prompt = on-partial` in a profile (values `on`, `on-partial`, `off`; `--cli-auto-prompt` and `--no-cli-auto-prompt` override per command). Key bindings in the prompt: F1 help panel, F3 documentation panel, F4 multi-column mode, F5 output panel, Ctrl+R history search.

## Defaults worth setting
```ini
[default]
region = eu-west-1
output = json
cli_pager =
cli_binary_format = raw-in-base64-out
```
- The CLI sends output through a pager (`less` on Linux/macOS, `more` on Windows). An empty `cli_pager` setting, `AWS_PAGER=""` or `--no-cli-pager` disables it, which keeps scripts from stopping at a pager. Precedence: `AWS_PAGER`, then `cli_pager`, then `PAGER`.
- `cli_binary_format`: the default `base64` expects binary values as base64 strings; `raw-in-base64-out` treats them literally, which is what blob parameters such as `aws lambda invoke --payload` usually need when you pass raw JSON.
- `output` accepts `json`, `table`, `text`, `yaml`, `yaml-stream` and `off`.

## v1 to v2 differences that bite
- Pager on by default; binary parameters default to base64; `aws ecr get-login` is not in v2 (use `get-login-password`).
- Wizards and helpers: `aws dynamodb wizard new-table`, `aws configure sso`, `aws configure export-credentials --format env`.

## Verify
- [ ] `aws --version` shows `aws-cli/2.x`; `aws whoami` works with each profile.
- [ ] A script runs non-interactively without hanging in a pager.

## Checked
Date: 2026-10-24. Sources: aws-cli v2 branch source (alias.py, clidriver.py, autoprompt/factory.py, data/cli.json, topics/config-vars.rst).
Confirmed: alias file ~/.aws/cli/alias with [toplevel] and [command <service>] sections, external aliases starting with ! run via the shell, --cli-auto-prompt/--no-cli-auto-prompt and cli_auto_prompt values on, on-partial, off, prompt key bindings F1/F3/F4/F5/Ctrl+R, pager precedence and the empty-value disable, cli_binary_format values and default, output formats including yaml-stream, aws configure export-credentials, the dynamodb new-table wizard, no ecr get-login in the v2 examples.
Removed as unconfirmed: Python-bundling and pip statements, S3 and region differences between v1 and v2, the exact failure text for unencoded payloads, a line-continuation in the alias file example.
Method: documentation only; no commands were run.
