---
id: computing-software.cloud-infrastructure-engineering.saltstack.events-master-tags
name: events-master-tags
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, events, event-bus, tags, salt-job, salt-auth, presence]
level: advanced
status: docs-checked
description: "Reference the Salt master event tags and data keys: salt/auth, minion start, salt/key, salt/job new/start/ret/prog, salt/run and presence events."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/event/master_events.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Master event tags

- `salt/auth`: `id`, `act` (accept, pend, reject, full, denied, error), `pub`. Reacting on it can loop; prefer `salt/key` or `salt/minion/<MID>/start`.
- `salt/minion/<MID>/start`: `id`; fires each time a minion connects.
- `salt/key`: `id`, `act`. Does not fire in auto-accept mode or with pre-seeded keys (Salt Cloud).
- `salt/job/<JID>/new`: `jid`, `tgt`, `tgt_type`, `fun`, `arg`, `minions`, `user`.
- `salt/job/<JID>/start/<MID>`: opt-in with `--start-event` or `start_event=True`.
- `salt/job/<JID>/ret/<MID>`: `id`, `jid`, `retcode`, `fun`, `return`.
- `salt/job/<JID>/prog/<MID>/<RUN NUM>`: per state function when `state_events` is enabled.
- `salt/run/<JID>/new` (`jid`, `fun`, `fun_args`, `user`) and `salt/run/<JID>/ret` (adds `return`).
- `salt/presence/present` (`present` list) and `salt/presence/change` (`new`, `lost`); both need `presence_events`.

Cloud events use `name` instead of `id`: `salt/cloud/<VM NAME>/creating`, `requesting`, `querying`, `waiting_for_ssh`, `deploying`, `created`, `destroying`, `destroyed`.

The page says its list is not comprehensive.

## Checked

2026-11-09. Read against the master events source (doc/topics/event/master_events.rst); tags and data keys were confirmed there. Removed the salt-run state.event line (not on that page).
Method: documentation only; no commands were run.
