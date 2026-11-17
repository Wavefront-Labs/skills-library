---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-pillar
name: targeting-pillar
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, pillar, pillar-cache, refresh-pillar]
level: practitioner
status: docs-checked
description: "Target Salt minions by pillar data with -I, the master-side pillar cache requirement and how to refresh it, plus nested key matching."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/pillar.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting by pillar

`-I` selects minions by pillar data.

```
salt -I 'somekey:specialvalue' test.version
```

Requirement: the master must hold a pillar data cache for each minion. Create it with:

```
salt '*' saltutil.refresh_pillar
salt '*' saltutil.sync_all
```

The cache is also filled during a highstate run. After pillar data changes, refresh the cache again or the targeting may not work correctly.

Globs work as in grain targeting. For nested values add a colon per level:

```
salt -I 'foo:bar:baz*' test.version
```

This matches minions whose pillar has a dict `foo` with key `bar` whose value begins with `baz`.

## Checked

2026-11-04: read the Salt pillar targeting page in full. Confirmed -I, the master-side pillar cache requirement, refresh_pillar and sync_all, the highstate note and nested matching. Nothing removed.

Method: documentation only; no commands were run.

