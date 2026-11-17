---
id: computing-software.cloud-infrastructure-engineering.saltstack.reactor-types-and-debugging
name: reactor-types-and-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, reactor, local, runner, wheel, caller, debugging, events]
level: advanced
status: docs-checked
description: "Pick the right Salt reaction type (local, runner, wheel, caller), read beacon-nested event data, fire test events and debug reactors in the foreground."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/reactor/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reaction types and debugging

Types:
- `local`: run a remote-execution function on targeted minions.
- `runner`: run a runner function on the master.
- `wheel`: run a wheel function on the master.
- `caller`: run a remote-execution function on a masterless minion, via the Reactor Engine in the minion config.

Since 2017.7.2 a unified schema passes arguments under `args` for every type; the older schema (`arg`/`kwarg`, or arguments directly under the runner or wheel function) still works. Give runner and wheel reactions unique state IDs, or they can overwrite each other in the async queue and lose reactions.

Event data: events from beacons nest their payload, so the minion ID is `data['data']['id']`, not `data['id']`.

Fire test events (data is a dict such as `{orchestrate: refresh}`; `event.send` goes to the master, `event.fire` to the minion's local bus) and watch the bus:

```
salt-run event.send <tag>
salt-call event.send <tag>
salt-call event.fire '<data>' <tag>
salt-run state.event pretty=True
```

Debug: stop the master and run `salt-master -l debug` in the foreground. The log shows the master gathering reactors for a tag, compiling reactions, and the rendered SLS or any render errors; an empty render is ignored by the reactor.

## Checked

2026-11-09. Read in full the Salt Reactor System page (doc/topics/reactor/index.rst, master branch). Corrected the unified-schema statement (only `args`) and the `event.fire` argument order; added the unique state ID warning.

Method: documentation only; no commands were run.
