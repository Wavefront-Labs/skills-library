---
id: computing-software.devops-ci-cd.packer.fmt-command
name: fmt-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [fmt, format, hcl2, ci, cmd-fmt]
level: intro
status: docs-checked
description: "packer fmt rewrites HCL2 files into canonical style; -check, -diff, -recursive and stdin usage."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/fmt/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer fmt` formats HCL2 configuration files to the canonical style, applying a subset of HCL conventions. JSON files are not modified. It prints the names of files that need formatting and writes the result back to them.

```bash
packer fmt -check .
packer fmt my-template.pkr.hcl my-varfile.pkrvars.hcl
cat my-template.pkr.hcl | packer fmt -
```

Options:

- `-check` reports whether input is formatted; exit status 0 means everything is formatted, non-zero otherwise. It never writes.
- `-diff` shows diffs of formatting changes.
- `-write=false` stops it writing to source files (always off with `-check`).
- `-` reads from stdin and writes to stdout.
- `-recursive` also processes subdirectories; by default only the given directory (or the current one) is processed.

## Checked
2026-11-03. Confirmed against the packer fmt command page: scope, JSON untouched, the examples and every option. Removed unsourced CI advice.
Method: documentation only; no commands were run.
