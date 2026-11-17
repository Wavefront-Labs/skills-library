---
id: computing-software.devops-ci-cd.renovate.config-validator
name: config-validator
category: computing-software
field: devops-ci-cd
product: renovate
tags: [config-validator, renovate-config-validator, validation, renovate]
level: practitioner
status: docs-checked
description: "Check Renovate configuration locally or in CI with renovate-config-validator and strict mode."
sources:
  - https://docs.renovatebot.com/config-validation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Every Renovate distribution ships a standalone program `renovate-config-validator`. With no arguments it checks all default config locations that exist, plus the file named in the `RENOVATE_CONFIG_FILE` environment variable.

```console
npx --yes --package renovate -- renovate-config-validator
```

A good result logs `Config validated successfully`.

- By default it exits non-zero on validation warnings or errors.
- `--strict` also fails when the config needs migration, for example `config:base` renamed to `config:recommended`. The output shows the old and new config.
- Pass filenames as arguments to check non-default names, such as preset repositories: `renovate-config-validator first_config.json`.
- When you pass a file name, the validator treats it as global self-hosted config rather than repository config. For a shared preset or non-standard filename, add `--no-global`: `renovate-config-validator --no-global go-presets.json`.

To validate automatically, use a pre-commit hook (the renovatebot/pre-commit-hooks repository), or push a branch named `{{branchPrefix}}reconfigure` (`renovate/reconfigure` with the default prefix) to the source repository: on its next run Renovate adds a passing or failing status and comments on an open PR with validation errors.

## Checked

2026-11-03. Confirmed against the Renovate Config Validation page (default behaviour, `RENOVATE_CONFIG_FILE`, `--strict`, filename arguments, `--no-global`, pre-commit hook, reconfigure branch). Removed the unsupported claims about what validation catches and the `dryRun` advice.

Method: documentation only; no commands were run.
