---
id: computing-software.cloud-infrastructure-engineering.saltstack.beacons-reactor-revert-workflow
name: beacons-reactor-revert-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, beacons, reactor, inotify, revert, workflow, events]
level: advanced
status: docs-checked
description: "Wire a Salt inotify beacon to a reactor that reverts a modified file by re-applying its managed state, following the documented step order."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/beacons/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Beacon plus reactor: revert a changed file

Documented workflow:
1. Install Pyinotify on the minion (the inotify beacon needs it).
2. Configure the inotify beacon on `/etc/important_file` with `disable_during_state_run: True`; restart the minion.
3. On the master run `salt-run state.event pretty=true` to confirm events arrive.
4. Create a reactor SLS and a state SLS that manages the file, then map the tag in the master config.
5. Run the master in debug mode to troubleshoot, then modify the file to trigger it.

Master config mapping (one top-level `reactor` section only): the tag pattern `salt/beacon/*/inotify//etc/important_file` maps to `/srv/reactor/revert.sls`.

The reactor applies a state to the minion that sent the event, restoring the file to its managed contents. The page's reactor SLS targets the minion with `data['id']`.

## Checked

2026-11-09. Read against the beacons source (doc/topics/beacons/index.rst); the step order, tag mapping and reactor example were confirmed there. Corrected the minion ID reference to `data['id']` as the page shows.
Method: documentation only; no commands were run.
