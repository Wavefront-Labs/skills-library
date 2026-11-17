---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-nodegroups
name: targeting-nodegroups
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, nodegroups, master-config, compound, top-file]
level: practitioner
status: docs-checked
description: "Define named Salt nodegroups in the master config as compound expressions and use them with -N, N@ and match: nodegroup, including syntax rules and caveats."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/nodegroups.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nodegroups

Define in the master config (typically `/etc/salt/master`); each value is a compound expression.

```yaml
nodegroups:
  group1: 'L@foo.domain.com,bar.domain.com,baz.domain.com or bl*.domain.com'
  group2: 'G@os:Debian and foo.domain.com'
  group3: 'G@os:Debian and N@group1'
  group4:
    - 'G@foo:bar'
    - 'or'
    - 'G@foo:baz'
```

Syntax:
- String values are split on whitespace; use the list form (each item tokenized as a whole) if a pattern contains a space.
- Nesting with `N@` is allowed; circular references are detected, the group is only partly expanded and an error is logged.
- Minion ID lists can be a plain YAML list since 2016.11.0; group names as dash list items since 2017.7.0.

Use:
- CLI: `salt -N group1 test.version`
- Compound or top file with `N@`: 2019.2.0 and later only.
- Top file: put `- match: nodegroup` directly after the group name.

```yaml
base:
  group1:
    - match: nodegroup
    - webserver
```

Restart the master after changing nodegroups so they are fully recognized (some functionality, such as -N on the command line, may work without a restart).

## Checked

2026-11-04: read the Salt node groups page in full. Confirmed the example config, whitespace tokenization, circular reference handling, version notes (2015.8.0, 2016.11.0, 2017.7.0, 2019.2.0), -N, the top file example and the restart note. Added the page's restart caveat.

Method: documentation only; no commands were run.

