---
id: computing-software.cloud-infrastructure-engineering.saltstack.grains-precedence
name: grains-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, grains, precedence, core-grains, minion-config]
level: advanced
status: docs-checked
description: "Know which Salt grain source wins when the same grain is defined in several places: core, /etc/salt/grains, minion config, custom _grains modules."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/grains/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grain precedence

When the same grain is defined in more than one place, the order from lowest to highest priority is:

1. Core grains
2. `/etc/salt/grains`
3. `/etc/salt/minion`
4. Custom grain modules in `_grains`

So a custom module overrides a static grain of the same name, and the minion config overrides `/etc/salt/grains`.

Use this to explain surprising values: if a static grain you set keeps being replaced, look for a `_grains` module returning the same key. Check what a minion really reports with `salt-call --local grains.items` (masterless) or `salt 'minion' grains.items`.

Note: this order covers grains only.

## Checked

2026-11-09. Read against the grains source (doc/topics/grains/index.rst); the precedence order and the listing commands were confirmed there. Removed the claim about pillar merging (not on that page).
Method: documentation only; no commands were run.
