---
id: computing-software.cloud-infrastructure-engineering.saltstack.beacons-configuration
name: beacons-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, beacons, minion-config, interval, disable-during-state-run, events]
level: practitioner
status: docs-checked
description: "Configure Salt beacons on a minion: the beacons block, list-based settings, interval, beacon_module for duplicates and disable_during_state_run."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/beacons/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring beacons

Beacons watch things on a minion and fire events on the bus.

- Define a top-level `beacons:` block in `/etc/salt/minion`, a file under `/etc/salt/minion.d/`, or the minion pillar (grains and local config also work).
- Settings are list-based: each beacon name (`inotify`, `load`, ...) maps to a list.
- To run several copies of one beacon module, add `beacon_module` (Neon).
- Default check interval is 1 second; set `interval` (seconds) per beacon.
- `disable_during_state_run: True` pauses the beacon during a state run and resumes after, preventing a loop where a reactor's state changes the watched file. Reactor states should be idempotent too.

Event tags look like `salt/beacon/<minion_id>/<beacon>/<path>`, e.g. `salt/beacon/larry/inotify//etc/important_file`. The inotify beacon needs Pyinotify on the minion.

## Checked

2026-11-09. Read against the beacons source (doc/topics/beacons/index.rst); config locations, beacon_module, the 1 second default, disable_during_state_run and the example tag were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
