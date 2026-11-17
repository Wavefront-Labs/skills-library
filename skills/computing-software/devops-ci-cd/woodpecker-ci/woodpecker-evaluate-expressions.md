---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-evaluate-expressions
name: woodpecker-evaluate-expressions
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [evaluate, expr, expressions]
level: advanced
status: docs-checked
description: "Gate Woodpecker steps with evaluate expressions over CI_ variables."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker `evaluate` expressions

`evaluate` runs a step only if the expression is true. Built-in `CI_` variables and custom variables can be used. The syntax is that of the expr-lang library.

```yaml
when:
  - evaluate: 'CI_PIPELINE_EVENT == "push" && CI_REPO == "owner/repo" && CI_COMMIT_BRANCH == CI_REPO_DEFAULT_BRANCH'
```

More documented examples:

```yaml
# commits by a given author
- evaluate: 'CI_COMMIT_AUTHOR == "woodpecker-ci"'
# skip commits containing text
- evaluate: 'not (CI_COMMIT_MESSAGE contains "please ignore me")'
# pull requests carrying a label
- evaluate: 'CI_COMMIT_PULL_REQUEST_LABELS contains "deploy"'
# skip only if SKIP=true, run when undefined
- evaluate: 'SKIP != "true"'
```

Use `evaluate` to narrow `release` events, since the release event has no dedicated filter; the variables `CI_PIPELINE_RELEASE_TITLE` and `CI_PIPELINE_RELEASE_PRE` carry release data.

Treat commit messages, authors and labels as untrusted input. String substitution places forge values into the YAML text before it is parsed, and Woodpecker quotes values containing line breaks so they cannot add YAML structure.

## Checked

2026-11-03. Read the Woodpecker workflow syntax page and confirmed the evaluate expression behaviour and examples. Nothing removed. 

Method: documentation only; no commands were run.
