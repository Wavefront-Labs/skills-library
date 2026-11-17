---
id: computing-software.systems-network-administration.kopia.kopia-policies-and-retention
name: kopia-policies-and-retention
category: computing-software
field: systems-network-administration
product: kopia
tags: [policy, retention, keep-latest, inheritance, policy-set, policy-import]
level: practitioner
status: docs-checked
description: "How Kopia policies inherit from global to path level, default retention counts and how to set, show, export and import them."
sources: ["https://kopia.io/docs/getting-started/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies can be set at four levels: global, per host (`@host`), per user (`user@host`) and per path (`user@host:/path`). New policies inherit from the more general ones, and a more specific setting wins. If `foo@bar:/path` does not define setting `xyz`, the user policy `foo@bar` sets `xyz=1` and global sets `xyz=2`, the effective value is 1. Note that `user@host` and `@host` mean the policy for that user or host only, not every policy beneath it.

## Defaults

`kopia policy show --global` on a fresh repository shows these retention counts: latest 10, hourly 48, daily 14, weekly 25, monthly 24, annual 3, and ignore rules read from `.kopiaignore` files.

## Commands

```console
kopia policy show --global
kopia policy set --keep-weekly 30 .
kopia policy set --add-ignore node_modules/ .
kopia policy show .
kopia policy list
kopia policy export --to-file export.json
kopia policy import --from-file import.json
```

`policy show` annotates each value as defined for the target or inherited from another level. Export and import use a JSON map from policy identifier (for example `(global)` or `user@host:/path`) to policy, with a `retention` object containing keys such as `keepLatest` and `keepHourly`. A snapshot frequency set in a policy makes Kopia take snapshots automatically; without one you must run snapshots manually.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Getting Started (four policy levels, inheritance and priority, @host note, global policy defaults, policy set/show/import/export, keepLatest JSON, snapshot frequency). Removed or corrected: the unconfirmed 'while a server or KopiaUI is running' qualifier and the closing paragraph about several repositories.
Method: documentation only; no commands were run.
