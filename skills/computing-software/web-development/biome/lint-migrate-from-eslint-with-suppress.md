---
id: computing-software.web-development.biome.lint-migrate-from-eslint-with-suppress
name: lint-migrate-from-eslint-with-suppress
category: computing-software
field: web-development
product: biome
tags: [biome, migrate-eslint, lint-suppress, suppress-reason, rules-sources, eslint-migration, biome-migrate]
level: practitioner
status: docs-checked
description: "Port ESLint rules with biome migrate eslint, then silence new violations with biome lint --suppress --reason to clear CI."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many Biome rules are inspired by other linters. To find equivalents for ESLint or typescript-eslint, see the rules sources page; for ESLint there is also a dedicated migration guide.

Two steps from the docs:

1. Port the rules from your ESLint configuration into `biome.json`:

```shell
biome migrate eslint
```

2. Suppress the violations Biome newly catches, so the linter stops erroring:

```shell
biome lint --suppress --reason "suppressed due to migration"
```

The command suppresses all linting violations Biome finds, using the reason "suppressed due to migration". The linter should then no longer error, and the suppression comments can be removed at a later stage.

Biome provides no rules that check code formatting; the Biome formatter is intended to handle all formatting decisions.

## Checked

2026-11-08. Read the linter index page in full. Unchanged: the two-step migrate then suppress procedure and commands. Removed: the "why this order" rationale, the claim that suppression comments require a reason, and a note about other migrations, none of which the page states; kept only the statement that Biome has no formatting rules.

Method: documentation only; no commands were run.
