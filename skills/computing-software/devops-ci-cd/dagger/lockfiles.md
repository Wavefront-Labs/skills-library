---
id: computing-software.devops-ci-cd.dagger.lockfiles
name: lockfiles
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, lockfile, lock-modes, reproducibility, dagger-lock, ci]
level: practitioner
status: docs-checked
description: "Choose a Dagger lock mode (disabled, live, pinned, frozen) and policy (pin, float), and refresh entries with dagger lock update."
sources: [https://docs.dagger.io/0.21/reference/cli/lockfiles]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger lockfiles: modes, policies, updates

Goal: make lookups (image digests, git refs) reproducible, and refresh them on purpose. Dagger 0.21 docs.

## Method

Two separate concepts:

- Lock mode: chosen per run, `dagger --lock=pinned call ...`.
- Lock policy: stored on each lock entry.

| Mode | Behaviour |
| --- | --- |
| `disabled` | ignore lockfile completely |
| `live` | resolve everything live and record |
| `pinned` | reuse pinned entries, resolve the rest live, record |
| `frozen` | resolve only from lockfile; fail on misses |

Recommended uses per the page: `disabled` to opt out; `live` to bootstrap or deliberately refresh; `pinned` for day-to-day development and most CI; `frozen` for reproducible, hermetic or offline runs.

Policies: `pin` prefers the recorded value; `float` prefers live resolution. Interaction:

- Entry with policy pin: disabled ignores it; live resolves and rewrites; pinned and frozen reuse it.
- Entry with policy float: disabled ignores; live and pinned resolve live and rewrite; frozen reuses the recorded value.
- Missing entry: disabled resolves live without writing; live and pinned resolve and write; frozen fails.

Lock-aware operations and default policy: `container.from` (inputs imageRef, platform) pin; `git.head` (remoteURL) float; `git.branch` float; `git.tag` pin; `git.ref` pin for tags else float. `git.commit` is already pinned by its input and creates no entries.

Updating:

```bash
dagger lock update                       # refresh entries already in .dagger/lock
dagger --lock=live call release          # refresh/discover entries a command touches
dagger --lock=live query --doc query.graphql
```

## Gotchas

- Run updates in an environment that can authenticate to any private registries or repositories the lookups need; that is your responsibility.
- `dagger lock update` uses the current environment's ambient authentication.
- Related: computing-software.devops-ci-cd.dagger.cli-running-functions.

## Checked

2026-11-07

Read reference/cli/lockfiles.mdx in full (slug /reference/cli/lockfiles matches the cited source URL). Confirmed the mode and policy tables, the typical-use list, the pin and float interaction lists, the missing-entry behaviour, dagger lock update and the --lock=live commands, the authentication note, and the lock-aware operations table with default policies and the git.commit remark. Removed the '(default)' label on disabled: the page does not state a default mode.

Method: documentation only; no commands were run.
