---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-roots-and-top-file
name: pillar-roots-and-top-file
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, pillar-roots, top-file, ignore-missing, include]
level: practitioner
status: docs-checked
description: "Lay out Salt pillar data: pillar_roots, the pillar top.sls, __env__ mapping, ignore_missing and pillar includes with defaults and key."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/pillar/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pillar roots and top file

Pillar holds values compiled on the master; each minion sees only data targeted to it.

```yaml
pillar_roots:
  base:
    - /srv/pillar
```

- Pillar files must not live inside the state tree.
- An `__env__` entry in `pillar_roots` maps unlisted environments to that directory; the path may contain `__env__` (for example `/srv/__env__/pillar`, added in 3005).

`/srv/pillar/top.sls` has the same structure as the state top file and supports matchers such as `grain`:

```yaml
base:
  '*':
    - packages
  'web*':
    - vim
```

- `ignore_missing: True` suppresses errors for missing pillar files (default `False`).
- Define keys inside the pillar files, not as key/value pairs in `top.sls`.

Includes, plain or with defaults and a nesting key:

```yaml
include:
  - users:
      defaults:
        sudo: ['bob', 'paul']
      key: users
```

## Checked

2026-11-04: read the Salt pillar reference page in full. Confirmed pillar_roots, the state-tree restriction, __env__ mapping (path substitution added in 3005), the top file example, grain matching, ignore_missing default and pillar includes with defaults and key. Nothing removed.

Method: documentation only; no commands were run.

