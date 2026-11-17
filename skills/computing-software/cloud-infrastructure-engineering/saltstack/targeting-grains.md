---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-grains
name: targeting-grains
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, grains, nested-grains, security]
level: intro
status: docs-checked
description: "Target Salt minions by grain values with -G, including globs in values and nested dictionary grains with colon-separated keys."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/grains.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting by grains

`-G` selects minions by grain data instead of minion ID.

```
salt -G 'os:CentOS' test.version
salt -G 'cpuarch:x86_64' grains.item num_cpus
```

The second matches every 64-bit minion and returns its CPU core count.

Globs work in the value. For a grain nested in a dictionary, add a colon for each level:

```
salt -G 'ec2_tags:environment:*production*' test.version
```

This matches minions whose `ec2_tags` dict has an `environment` key containing "production".

The page does not cover `-P` regex grain matching (compound targeting offers `P@` for that).

Security: the page marks as important a pointer to the FAQ entry "Is Targeting using Grain Data Secure?"; read it before relying on grain targeting.

## Checked

2026-11-04: read the Salt grains targeting page in full. Confirmed -G examples, globs, nested colon matching and the security pointer. Removed the claim about why grains are insecure, which the page does not state.

Method: documentation only; no commands were run.

