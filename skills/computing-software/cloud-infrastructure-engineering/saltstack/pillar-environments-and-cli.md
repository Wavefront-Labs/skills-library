---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-environments-and-cli
name: pillar-environments-and-cli
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, pillarenv, pillar-opts, pillar-safe-render-error, cli]
level: advanced
status: docs-checked
description: "Limit Salt pillar to one environment with pillarenv, pass pillar on the command line, expose master config via pillar_opts and reveal render errors."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/pillar/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pillar environments and CLI

- Minion option `pillarenv: base` limits pillar to one environment.
- Override per run:

```
salt '*' state.apply mystates pillarenv=testing
```

- `pillarenv_from_saltenv: True` (minion, 2017.7.0+) ties pillarenv to saltenv; a CLI `pillarenv` overrides it.

Pass pillar inline:

```
salt '*' state.apply pillar='{"cheese": "spam"}'
```

Data sent this way reaches all minions, not only those targeted.

`pillar_opts: True` exposes master configuration in pillar; disabled by default. The reference page sets it in the minion config; the pillar tutorial sets it in the master config and then for the appropriate minions.

Render errors on the minion are hidden by default. To see details on the master:

```yaml
pillar_safe_render_error: False
```

## Checked

2026-11-04: read the Salt pillar reference page and pillar walkthrough in full. Confirmed pillarenv, the CLI override, pillarenv_from_saltenv (2017.7.0), CLI pillar reaching all minions, pillar_opts default and pillar_safe_render_error. Reconciled where pillar_opts is set, since the two pages differ.

Method: documentation only; no commands were run.

