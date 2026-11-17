---
id: computing-software.devops-ci-cd.packer.fix-command
name: fix-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [fix, json-templates, upgrade, migration, cmd-fix]
level: intro
status: docs-checked
description: "packer fix updates old JSON templates for the current Packer version; it does not handle HCL2."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/fix/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer fix` finds backward-incompatible parts of a template and rewrites them so the template works with the latest Packer. It is a JSON-template-only command; it cannot update HCL2 templates.

```bash
packer fix old.json > new.json
packer fix -validate=false old.json > new.json
```

Behaviour:

- The fixed template goes to standard output, so redirect it to save it.
- Errors go to standard error, so they show even when stdout is redirected, and the exit status is non-zero on failure.
- Even when nothing needed fixing the template is printed, with key order and indentation possibly changed. The output is pretty-printed.
- `-validate=false` disables validation of the fixed template (validation is on by default).
- `packer fix -h` lists every fix the command performs.

The docs say to run it after you update to a new Packer release. `packer hcl2_upgrade` converts JSON templates to HCL2.

## Checked
2026-11-03. Confirmed against the packer fix command page (JSON-only, stdout, stderr, exit status, `-validate=false`, `packer fix -h`) and the hcl2_upgrade page. Removed the claim about JSON templates and new core features.
Method: documentation only; no commands were run.
