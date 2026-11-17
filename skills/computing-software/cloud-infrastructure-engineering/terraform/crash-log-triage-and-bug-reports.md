---
id: computing-software.cloud-infrastructure-engineering.terraform.crash-log-triage-and-bug-reports
name: crash-log-triage-and-bug-reports
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, crash-log-triage, bug-report, panic, crash-log, provider-crash, core-crash, github-issue, stack-trace, redaction]
level: practitioner
status: docs-checked
description: "Triage a Terraform crash or provider panic: tell a core crash from a plugin crash, capture logs with TF_LOG variables, redact them, and file an issue the maintainers can act on."
sources: ["https://developer.hashicorp.com/terraform/internals/debugging", "https://developer.hashicorp.com/terraform/cli/config/environment-variables", "https://developer.hashicorp.com/terraform/cli/commands/version", "https://raw.githubusercontent.com/hashicorp/terraform/main/internal/logging/panic.go", "https://github.com/hashicorp/terraform/blob/main/.github/CONTRIBUTING.md", "https://github.com/hashicorp/terraform-provider-aws/blob/main/.github/ISSUE_TEMPLATE/00_bug_report.yml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform crash triage and bug reports

## 1. Core crash or plugin crash
Terraform's panic handler (`internal/logging/panic.go`) distinguishes the two:
- **Core crash**: stderr shows a banner `TERRAFORM CRASH` with "Terraform crashed! This is always indicative of a bug within Terraform", then `panic: <value>` and a Go stack trace. The process exits with code 11. The banner asks you to report it at github.com/hashicorp/terraform/issues with your Terraform version and the stack trace.
- **Plugin (provider) crash**: Terraform prints "Stack trace from the <name> plugin:" followed by the recorded lines, then "Error: The <name> plugin crashed!" and says it is always a bug within the plugin and should be reported to the plugin's maintainers. Only a limited number of stack lines is recorded for the output, so capture a full log for the report.
- Provider issue templates ask you to consider the Terraform Core repository instead for configuration language or resource ordering problems, state and state backend issues, provisioner issues, registry issues, and issues spanning resources across multiple providers.

## 2. Capture a log
- `TF_LOG` accepts `TRACE`, `DEBUG`, `INFO`, `WARN` or `ERROR` (decreasing verbosity); logs go to stderr. `TF_LOG=JSON` writes TRACE-level logs in JSON, an encoding the docs call not a stable interface.
- `TF_LOG_CORE` and `TF_LOG_PROVIDER` enable logging separately for Terraform itself and the provider plugins, taking the same levels as `TF_LOG`.
- `TF_LOG_PATH` appends the log to a file, but `TF_LOG` must also be set for any logging to be enabled.
```bash
TF_LOG=TRACE TF_LOG_PATH=./trace.log terraform apply
```
The debugging page asks you to include the detailed log with a bug report via a service such as gist.

## 3. File the issue
Search existing issues and pull requests first. Terraform's CONTRIBUTING page asks you to open an issue with the most appropriate template and fill in everything it requests. The AWS provider bug template asks for:
- Terraform and provider versions (`terraform --version`; `terraform version` prints the Terraform version, platform and installed providers, `-json` for JSON).
- Affected resources or data sources, expected behaviour, actual behaviour.
- The error or panic output snippet, plus debug logging if possible, including any panic.
- A sample configuration that applies with minimal modifications and does not rely on external modules; reports without a functional, standalone sample may be closed without investigation.
- Steps to reproduce, atypical situations (air-gapped environments, special partitions), and whether you would implement a fix.
That template attaches files under 25MB directly and asks for larger files to be uploaded elsewhere and linked. Other repositories use other templates; read the one for your target.

## Redaction
Logs and configuration can contain account identifiers, hostnames and secret values. Review and remove them yourself before posting; the pages read here do not describe automatic redaction.

## Checked
Date: 2026-11-07. Read in full: the "Enable Terraform logs" page, the CLI environment variables page (TF_LOG, TF_LOG_PATH), the `terraform version` page, `internal/logging/panic.go` from the Terraform repository (crash banner, exit code 11, plugin crash text), and the AWS provider bug report template. The Terraform CONTRIBUTING page was read only from its introduction and searched for crash/log wording (it is about pull requests and says to use issue templates). Removed as unsupported or contradicted: every mention of a `crash.log` file (current core code prints the panic to stderr; no such file is written there), the invented decision table, the "provider stderr section" and `(*GRPCProvider)` error strings, the `grep` recipes, the Windows and OpenTofu notes, the `-parallelism` advice, and the Verify list.
Method: documentation only; no commands were run.
