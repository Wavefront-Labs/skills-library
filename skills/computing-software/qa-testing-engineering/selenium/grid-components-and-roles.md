---
id: computing-software.qa-testing-engineering.selenium.grid-components-and-roles
name: grid-components-and-roles
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [grid-components, selenium-grid, router, distributor, session-map, event-bus]
level: practitioner
status: docs-checked
description: "Understand and deploy Selenium Grid 4 roles: router, distributor, session map, session queue, event bus and nodes, in standalone, hub-node and fully distributed modes."
sources:
  - https://www.selenium.dev/documentation/grid/components/
  - https://www.selenium.dev/documentation/grid/getting_started/
  - https://www.selenium.dev/documentation/grid/architecture/
  - https://www.selenium.dev/documentation/grid/advanced_features/external_datastore/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid roles (router, distributor, session map, event bus)

## Components
| Component | Job |
|---|---|
| **Router** | entry point (`:4444`); new session requests go to the queue, existing session commands are forwarded directly to the owning node (looked up in the session map) |
| **Session queue** | FIFO of new session requests; times out requests not matched in `session-request-timeout` |
| **Distributor** | knows all nodes and slots; takes requests from the queue, picks a matching slot, asks the node to create the session, records it in the session map |
| **Session map** | session id -> node URI |
| **Event bus** | messaging between components (ZeroMQ by default; ports 4442 publish, 4443 subscribe) |
| **Node** | runs browsers via drivers or relays; registers with the distributor via the event bus, sends heartbeats |

## Modes
```bash
# Standalone: all in one process (local, small CI)
java -jar selenium-server-4.x.jar standalone

# Hub and node: hub = router + distributor + session map + queue + event bus
java -jar selenium-server-4.x.jar hub
java -jar selenium-server-4.x.jar node --hub http://hub:4444

# Fully distributed: each role separately (large grids, HA)
java -jar selenium-server-4.x.jar event-bus
java -jar selenium-server-4.x.jar sessions
java -jar selenium-server-4.x.jar sessionqueue
java -jar selenium-server-4.x.jar distributor --sessions http://sessions:5556 --sessionqueue http://queue:5559 --bind-bus false
java -jar selenium-server-4.x.jar router --sessions http://sessions:5556 --distributor http://distributor:5553 --sessionqueue http://queue:5559
java -jar selenium-server-4.x.jar node --publish-events tcp://event-bus:4442 --subscribe-events tcp://event-bus:4443
```
Session map can be backed by Redis or JDBC for persistence.

## Choosing
- Standalone: one machine.
- Hub/node: several machines; the Event Bus lives inside the hub.
- Distributed: each component started separately, ideally on different machines, so they can scale or fail independently.

## Debugging by role
- Session never starts: queue/distributor (no matching stereotype, no free slot).
- Commands fail mid-session: router to node network, or the node died.
- Nodes disappear: event bus ports blocked, heartbeat timeouts.

## Security
Set `--registration-secret` (the Grid management endpoints take it in the `X-REGISTRATION-SECRET` header) and enable basic auth on the router; do not expose an unauthenticated Grid publicly.

## Verify
The Grid `/status` endpoint and Grid UI list the expected nodes after start, and a test session's path (router -> node) is visible in logs or traces.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51). Confirmed: roles and responsibilities (router, FIFO new session queue with request timeout, distributor, session map, event bus, node heartbeats), default ports (4444 router, 4442/4443 event bus, 5553 distributor, 5556 session map, 5559 queue, 5555 node), the distributed start commands and `--bind-bus false`, ZeroMQ as the default event bus implementation, Redis and JDBC session map backends, `--registration-secret`, router basic auth. Removed as undocumented: node-count sizing guidance, the stale session map remark and the per-component `/status` claim.

Method: documentation only; no commands were run.
