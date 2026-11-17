---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-linter
name: woodpecker-linter
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [linter, lint, bad-habits]
level: intro
status: docs-checked
description: "Lint Woodpecker workflow files for errors, deprecations and bad habits."
sources: ["https://woodpecker-ci.org/docs/usage/linter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker linter

Woodpecker lints workflow files automatically and shows errors and warnings in the UI for every pipeline. Run it by hand with:

```shell
woodpecker-cli lint <workflow files>
```

Bad habit warning: every item in a `when` block should have an `event` filter so no step runs on all events. If new events are added later, your steps probably should not run on them.

Incorrect:

```yaml
when:
  - branch: main
  - event: tag
```

The first item has no `event`.

Correct:

```yaml
when:
  - branch: main
    event: push
  - event: tag
```

Step-level too: `when: branch: main` alone triggers the warning; use `event: [tag, push]` or add `event` to each item.

## Checked

2026-11-03. Confirmed against: linter (automatic linting, woodpecker-cli lint, event filter bad habit and examples). Removed: a CLI image tag and a claim about commands/settings lint rules that the linter page does not state.

Method: documentation only; no commands were run.
