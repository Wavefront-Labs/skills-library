---
id: computing-software.devops-ci-cd.packer.required-version
name: required-version
category: computing-software
field: devops-ci-cd
product: packer
tags: [required-version, constraints, packer-block, block-packer]
level: intro
status: docs-checked
description: "Set required_version in the packer block to fail fast when the running Packer is too old or too new."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/packer/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`required_version` in the `packer` block holds a version constraint string for the Packer binary. If the running version does not match, Packer errors out before doing anything else.

```hcl
packer {
  required_version = ">= 1.2.0, < 2.0.0"
}
```

Constraint syntax is close to Bundler and npm: one or more conditions separated by commas, each an operator and a version number such as `1.2.0`.

Use it in shared repositories so everyone, including CI, runs a version with the behaviour the template relies on. The same string format is used for the `version` of a plugin in `required_plugins`.

Values in a `packer` block must be constants. They cannot reference named objects such as variables, and they cannot use built-in functions.

## Checked
2026-11-03. Confirmed against the packer block page: `required_version` constraint string, error and exit on mismatch, Bundler/npm-like syntax, constants only in a `packer` block. Removed the `min_packer_version` claim and a closing tip, which the page does not state.
Method: documentation only; no commands were run.
