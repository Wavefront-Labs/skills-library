---
id: computing-software.qa-testing-engineering.selenium.grid-standalone-hub-node-distributed
name: grid-standalone-hub-node-distributed
category: computing-software
field: qa-testing-engineering
product: selenium
tags: [hub-and-node, selenium-grid, grid-standalone, distributed-grid]
level: practitioner
status: docs-checked
description: "Choose and start Selenium Grid 4 modes: standalone, hub and node, and fully distributed components, with the right ports, event bus settings and registration checks."
sources:
  - https://www.selenium.dev/documentation/grid/getting_started/
  - https://www.selenium.dev/documentation/grid/configuration/cli_options/
  - https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standalone, hub-and-node and distributed modes

## Standalone (one process, all roles)
```bash
java -jar selenium-server-<version>.jar standalone --selenium-manager true
```
Detects local browsers/drivers; endpoint `http://localhost:4444`. Good for a single CI machine.

## Hub and node
```bash
# hub (router, distributor, session map, queue, event bus in one)
java -jar selenium-server.jar hub
# each node
java -jar selenium-server.jar node --hub http://hub-host:4444 --max-sessions 4
```
Nodes connect to the event bus on ports **4442 (publish) / 4443 (subscribe)**; open those between nodes and hub, plus 4444 for clients and the node port (5555 default) from hub to node.
Explicit: `node --publish-events tcp://hub:4442 --subscribe-events tcp://hub:4443`.

## Fully distributed
Start separately: `event-bus`, `sessions` (session map), `sessionqueue`, `distributor`, `router`, `node`. Use for large grids where components scale or fail independently; most teams don't need it.

## Choosing
| Need | Mode |
|---|---|
| One machine, a few browsers | standalone |
| Several machines / OSes | hub and node |
| Components that must scale or fail independently | distributed (or Kubernetes with autoscaling, see the KEDA skill) |

## Health checks
```bash
curl -s http://hub:4444/status
```
The status lists every registered node with its availability (`up`, `draining` or `down`), sessions and slots. The Grid UI at the Grid URL (default `http://localhost:4444`) shows the same.

## Gotchas
- Nodes advertise their URL; in NAT/Docker set `--host`/`--port` or `--grid-url` so the hub can reach them.
- The recommended `--max-sessions` is the number of processors; `--override-max-sessions true` lets you exceed it at the cost of session stability.

## Verify
`/status` lists all expected nodes as `up`, and a test session appears in the UI.

## Checked

Checked 2026-10-25 against the Selenium documentation source (seleniumhq.github.io, pushed 2026-10-23, examples tracking Selenium 4.51). Confirmed: `standalone --selenium-manager true`, hub and node commands, `--hub`, `--publish-events`/`--subscribe-events`, event bus ports 4442/4443 and node port 5555, `--max-sessions` and `--override-max-sessions` semantics, `--host`, `--port` and `--grid-url`, node availability values. Removed as undocumented: the jq pipeline over `/status`, the `/ui` path, and the claim that mismatched server versions are unsupported.

Method: documentation only; no commands were run.
