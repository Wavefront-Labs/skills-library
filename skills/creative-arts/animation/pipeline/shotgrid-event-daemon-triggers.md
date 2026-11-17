---
id: creative-arts.animation.pipeline.shotgrid-event-daemon-triggers
name: shotgrid-event-daemon-triggers
category: creative-arts
field: animation
product: pipeline
tags: [shotgrid-events, event-daemon, event-log, triggers, webhooks, production-tracking, automation]
level: advanced
status: draft
description: "Automate pipeline reactions to ShotGrid changes with the Shotgun Event Daemon: plugin callbacks, event filters, config, state handling, idempotency and webhook alternatives."
sources:
  - https://developer.shotgridsoftware.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Event daemon triggers

ShotGrid records every change as an **EventLogEntry**. The open-source **Shotgun Event Daemon** (shotgunEvents, from Shotgun Software) polls those entries and calls your Python plugins, so you can react to status changes without anyone clicking a button: create folders when a shot is created, notify when a task is approved, kick off a render when a version is submitted.

## Components
- **shotgunEventDaemon.py** runs as a service on a server you control.
- **Plugins** are Python files in the configured plugin path, each exposing `registerCallbacks(reg)`.
- **Config** (`shotgunEventDaemon.conf`): the site URL, a script name and key, plugin paths, logging, and where the last processed event ID is stored.

## A plugin
```python
def registerCallbacks(reg):
    match = {"Shotgun_Task_sg_status_list_Change": ["*"]}
    reg.registerCallback("daemon_script", "<script_key_from_env>", on_status, match, None)

def on_status(sg, logger, event, args):
    meta = event["meta"]
    if meta.get("new_value") == "apr":
        logger.info("Approved: %s", event["entity"])
        # act here: update a field, notify, queue a job
```
- `matchEvents` filters by event type and optional attribute lists. Event types follow a `Shotgun_<Entity>_<Change|New|Retirement|...>` pattern; check the daemon's README for the exact list.
- Never hard-code keys: read secrets from the environment or a vault.

## Reliability rules
1. **Idempotent callbacks**: events can be replayed after a restart; a repeated event must not duplicate folders or jobs.
2. **Keep callbacks fast**: queue long work to the farm or a worker.
3. **Handle exceptions**: the daemon logs and continues, but silent failures hide missed events; monitor the log.
4. **State**: the daemon stores the last event ID; back it up so you do not skip or reprocess after a rebuild.
5. **Test** in a sandbox site first.

## Alternatives
Newer Flow Production Tracking versions offer webhooks that push events to a URL; compare to the daemon (polling) before choosing, and check the current docs for availability and limits.

## Verify
- [ ] A test change triggers the callback exactly once.
- [ ] Restarting the daemon does not duplicate actions.
- [ ] Errors reach a monitored log.
