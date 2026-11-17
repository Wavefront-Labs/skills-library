---
id: computing-software.devops-ci-cd.packer.validate-command
name: validate-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [validate, syntax, ci, evaluate-datasources, cmd-validate]
level: practitioner
status: docs-checked
description: "packer validate checks template syntax and configuration, with flags for syntax-only, datasources and var files."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/validate/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer validate` checks the syntax and configuration of a template. It exits zero on success, non-zero on failure, and prints the errors.

```bash
packer validate my-template.pkr.hcl
packer validate -var-file=prod.pkrvars.hcl .
```

Options:

- `-syntax-only` checks syntax only, without validating the configuration.
- `-evaluate-datasources` evaluates data sources (HCL2 only). Data sources may call external services that bill per operation, so validation can cost money.
- `-only` and `-except` select builds by name, as for `build`.
- `-no-warn-undeclared-var` silences the warning shown when a var file assigns variables that have no `variable` block. `validate` warns by default; `build` does not.
- `-machine-readable` makes stdout machine-readable while logging stays on stderr.
- `-var` and `-var-file` set variables.

A representative error: `Either a path or inline script must be specified.` for a shell provisioner with neither.

## Checked
2026-11-03. Confirmed against the packer validate command page: exit status, every listed option and the example error. Removed unsourced pipeline advice.
Method: documentation only; no commands were run.
