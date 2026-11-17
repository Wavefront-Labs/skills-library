---
id: computing-software.systems-network-administration.headscale.policy-recovery
name: policy-recovery
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, policy-get, policy-check, policy-set, recovery, database-mode]
level: advanced
status: docs-checked
description: "Recover when Headscale refuses to start because the policy stored in the database is invalid: dump, validate, fix, write back, then start."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recover an invalid database policy

Applies when the policy is stored in the database and Headscale refuses to start because of an invalid policy; it checks the policy at startup and the error message says which part is invalid.

```
headscale policy get --bypass-server-and-access-database-directly > policy.json
headscale policy check --file policy.json
headscale policy set --bypass-server-and-access-database-directly --file policy.json
```

1. Dump the stored policy to `policy.json`.
2. Edit it to fix the errors.
3. Run `policy check` until it passes.
4. Write it back with `policy set`.
5. Start Headscale normally.

## Requirements

The get and set commands need a complete server configuration file including database settings; a minimal config for controlling Headscale via remote CLI is not sufficient. Use `-c` to point to an alternative configuration file:

```
headscale -c /path/to/config.yaml policy get --bypass-server-and-access-database-directly
```

## Note

Storing the policy in the database is typically only required when a web interface is used (policy page, footnote).

## Checked

2026-11-04. Confirmed against the Headscale FAQ (recovery steps, full-configuration warning) and policy page (database storage footnote). Removed the Gotchas to stop the server first and back up SQLite before writing, which the FAQ does not state.

Method: documentation only; no commands were run.
