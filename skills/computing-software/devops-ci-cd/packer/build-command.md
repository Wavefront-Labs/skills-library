---
id: computing-software.devops-ci-cd.packer.build-command
name: build-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [build, cli, artifacts, parallel, cmd-build]
level: practitioner
status: docs-checked
description: "packer build runs every build in a template in parallel and prints the artifacts; lists its flags and what each one does."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer build` takes a template (a file or a directory of `.pkr.hcl` files) and runs all the builds in it to generate a set of artifacts. The builds execute in parallel unless told otherwise, and the artifacts are printed at the end.

```bash
packer build .
packer build -var-file=prod.pkrvars.hcl -only='*.second-example' ./folder
```

Flags documented on the command page:

- `-color=false` disables colorized output.
- `-debug` disables parallelization and turns on builder debug mode.
- `-except` and `-only` take comma-separated build names.
- `-force` makes a builder run when artifacts from a previous build would block it.
- `-on-error=cleanup|abort|ask|run-cleanup-provisioner` picks failure behaviour (default `cleanup`).
- `-parallel-builds=N` caps concurrent builds; `0` means no limit and is the default.
- `-timestamp-ui` prefixes each UI line with an RFC3339 timestamp.
- `-var` (repeatable) and `-var-file` set template variables.
- `-warn-on-undeclared-var` warns when a variables file assigns a variable with no `variable` block (off by default).
- `-skip-enforcement` skips injection of HCP Packer enforced provisioners.

The exact effect of `-debug` and `-force` is left to each builder.

## Checked
2026-11-03. Confirmed against the packer build command page: parallel execution, every listed flag and its default, the `-on-error` values and the HCL2 naming of builds. Removed the advice to run `packer validate` first.
Method: documentation only; no commands were run.
