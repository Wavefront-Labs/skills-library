---
id: computing-software.cloud-infrastructure-engineering.saltstack.mine-get-and-ssh
name: mine-get-and-ssh
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, mine, mine-get, salt-ssh, jinja, targeting, haproxy]
level: practitioner
status: docs-checked
description: "Read Salt Mine data with mine.get in Jinja, target by id/grain/pillar/compound, and know how salt-ssh finds mine_functions (roster, pillar, master config)."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/mine/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading the Mine

Workflow from the page:
1. Put `mine_functions` (e.g. `network.ip_addrs: [eth0]`) in a pillar file.
2. `saltutil.refresh_pillar`, then verify with `pillar.items`.
3. `mine.update` to force collection, or wait for the interval.
4. In a template (for example an HAProxy config) call `salt['mine.get'](...)` to build the list of web server addresses.

Targeting in `mine.get`: minion ID (glob or regex), grains, pillar, or compound. Pillar targeting requires pillar data cached on the master.

Salt-SSH (supports `mine.get` since 2015.5.0): minions cannot supply their own `mine_functions`, so Salt looks in this order: roster data, pillar, master config. It is slower because a separate wrapper call runs against each minion.

## Checked

2026-11-04: read the Salt Mine page in full. Confirmed the HAProxy example workflow, mine.get targeting methods, the pillar cache note and the salt-ssh behaviour (2015.5.0, roster then pillar then master config). Nothing removed.

Method: documentation only; no commands were run.

