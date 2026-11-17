---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-tutorial-first-pillar
name: pillar-tutorial-first-pillar
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, tutorial, refresh-pillar, state-apply, security]
level: intro
status: docs-checked
description: "Build a first Salt pillar: /srv/pillar top.sls and data.sls, refresh and verify with pillar.items, use it in states, pass pillar on the CLI, and heed the security caveats."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/pillar.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First pillar

Pillar is tree-structured data created on the master and sent only to targeted minions: secrets, minion config, per-minion variables.

Steps:
1. `salt '*' pillar.items` to see the default.
2. `mkdir /srv/pillar`, then write `top.sls` mapping `'*'` to a `data` SLS, and `data.sls` with a key such as `info`.
3. `salt '*' saltutil.refresh_pillar`, then verify the key in `pillar.items`.
4. Structured data (for example `users/init.sls` mapping usernames to UIDs) can drive a Jinja loop in a state.
5. A pillar file can map package names per OS family using grains; states read them with `pillar.get` and a default.

CLI pillar:

```
salt '*' state.apply pillar='{"foo": "bar"}'
salt '*' state.sls my_sls_file pillar='{"foo": {"bar": "baz"}}'
```

Caveats:
- CLI values overwrite the whole existing key instead of merging.
- CLI pillar is broadcast to all minions, so never use it for secrets.
- `pillar_opts` can expose the master config; avoid it if that holds secrets.
- Pillar files must not be under `file_roots`, or minions can bypass targeting.

## Checked

2026-11-04: read the Salt pillar walkthrough in full. Confirmed the /srv/pillar steps, refresh_pillar, the users and package-name examples, CLI pillar examples, the overwrite note, the all-minions broadcast warning, pillar_opts and the file_roots caveat. Nothing removed.

Method: documentation only; no commands were run.

