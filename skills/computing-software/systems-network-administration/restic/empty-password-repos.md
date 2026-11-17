---
id: computing-software.systems-network-administration.restic.empty-password-repos
name: empty-password-repos
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, insecure-no-password, empty-password, repository]
level: advanced
status: docs-checked
description: "Use repositories with an empty password through the explicit --insecure-no-password flag family, including copy, key add and key passwd."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repositories with an empty password

Restic refuses to create or operate on repositories with an empty password unless you say so explicitly (since restic 0.17.0). The flag is `--insecure-no-password`, and it must always be given when operating on such a repository. With the flag, restic does not prompt for a password.

```
restic init --insecure-no-password --repo /path/to/repo
restic backup --insecure-no-password --repo /path/to/repo /path/to/data
```

## Related flags

- `init` and `copy` accept `--from-insecure-no-password` for the source repository.
- `key add` and `key passwd` accept `--new-insecure-no-password` to set an empty password on a key.

## Rules

- Giving `--insecure-no-password` while also passing a password via a CLI option or environment variable is an error.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (Repositories with empty password) and the restic command reference (`--insecure-no-password` help text): default refusal, the 0.17.0 version, no prompt, the error when combined with a password, `init`/`copy` `--from-insecure-no-password`, `key add`/`key passwd` `--new-insecure-no-password`. Removed: the claim that omitting the flag silently treats the repository as password-protected, the unlisted password-variable list, the encryption-strength commentary and the scripting advice (not in the docs).

Method: documentation only; no commands were run.
