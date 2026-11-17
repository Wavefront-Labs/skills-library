---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-cli-options
name: salt-cli-options
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-cli, async, static, verbose, subset, return, hide-timeout]
level: intro
status: docs-checked
description: "Use common salt command options: --async, -v, -s/--static, --hide-timeout, --subset, --return, batch flags and target flags -E -G -C."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/cli/salt.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt command options

- `--async`: print only the job ID and exit without waiting for minions.
- `-v`, `--verbose`: extra output such as the job ID.
- `-s`, `--static`: return all data at once (after all minions reply or a hard timeout) instead of streaming. Without it JSON output is not valid as a whole; `--out=json` is often paired with `--static`.
- `-b`, `--batch-size`: progressive set of minions, count or percent; related `--batch-wait`, `--batch-safe-limit`, `--batch-safe-size`.
- `--hide-timeout`: show only minions that could be reached.
- `--subset=N`: run on a random subset of targeted minions after checking they have the function.
- `--return=RETURNER`: send results to a returner (`mysql`, `redis`, ...).
- Targets: `-E` regex, `-G` grains, `-C` compound.

The timeout option defaults to 5 seconds.

## Checked

2026-11-09. Read against the salt command reference source (doc/ref/cli/salt.rst); options, the 5 second timeout default and the --static JSON note were confirmed there. Removed the -S, -I and -N target flags (not on the page, which includes them from other files).
Method: documentation only; no commands were run.
