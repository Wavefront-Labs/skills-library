---
id: computing-software.devops-ci-cd.forgejo.actions-variables-and-naming-rules
name: actions-variables-and-naming-rules
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-variables, vars-context, variable-names, variable-precedence]
level: practitioner
status: docs-checked
description: "Create non-secret workflow variables, obey the name constraints and know that owner-level values win."
sources:
  - https://forgejo.org/docs/latest/user/actions/basic-concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables are key/value pairs stored in the database and used as `${{ vars.KEY }}`. Unlike secrets, a variable's value can be modified later. Define them at:

- `/org/{org}/settings/actions/variables`
- `/user/settings/actions/variables`
- `/{owner}/{repo}/settings/actions/variables`

Name constraints:

- Only alphanumeric characters and underscores; no spaces.
- Must not start with `FORGEJO_`, `GITHUB_` or `GITEA_`.
- Must not start with a number.
- Case-insensitive.
- Unique at the level where they are created.
- Must not be `CI`.

Precedence: a variable defined in the settings of the repository's owner (organization or user) takes precedence over the same variable defined in the repository itself.

Compare with secrets, which are stored encrypted and whose value cannot be changed or displayed after creation. Organization or user level variables are available in every repository of that owner.

## Checked

2026-11-04. Confirmed against the Forgejo Actions basic concepts page (Custom variables, Name constraints, Precedence): the three settings paths, the vars.KEY syntax, all six name rules and the owner-over-repository precedence. Removed: the word unencrypted and the advice that credentials belong in secrets, which the page does not state in those terms.

Method: documentation only; no commands were run.
