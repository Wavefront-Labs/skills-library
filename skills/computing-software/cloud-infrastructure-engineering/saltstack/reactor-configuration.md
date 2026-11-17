---
id: computing-software.cloud-infrastructure-engineering.saltstack.reactor-configuration
name: reactor-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, reactor, events, master-config, jinja, tuning]
level: practitioner
status: docs-checked
description: "Configure the Salt reactor: map event tags to reaction SLS files in the master config, available Jinja context, best practices and worker tuning options."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/reactor/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reactor configuration

The reactor lets the master (or a minion) act when an event with a matching tag fires on the event bus. Each event has a tag and a data dictionary.

- Master config `reactor:` (by default `/etc/salt/master` or `/etc/salt/master.d/reactor.conf`) maps tags (globs allowed) to one or more reaction SLS files; file names may be globs, local paths or `salt://` URLs (base environment unless `?saltenv=` is given).
- Reaction files are YAML plus Jinja, like state files, but the Jinja context is minimal: `tag`, `data`, and a `salt` object for quick calls. Grains and pillar are not available.

Best practice:
- Keep reactor files small with few reactions; matching and rendering run sequentially.
- Reactions are asynchronous and do not support requisites.
- Put complex or slow work in orchestration and have the reactor trigger it.

Tuning for many long jobs: raise `reactor_worker_hwm` (the queue size; `0` is bounded only by memory, so watch memory use) and `reactor_worker_threads` (more concurrent workers, each holding a copy of the Salt code).

Common uses: auto-accepting matching minion keys, highstate on minion start, syncing custom grains or modules on the `salt/minion/*/start` tag, passing event data to states or orchestration as inline pillar.

## Checked

2026-11-09. Read in full the Salt Reactor System page (doc/topics/reactor/index.rst, master branch). Removed the unsupported claim about a single `reactor` section; sharpened the file-path and tuning wording.

Method: documentation only; no commands were run.
