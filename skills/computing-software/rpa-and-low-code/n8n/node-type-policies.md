---
id: computing-software.rpa-and-low-code.n8n.node-type-policies
name: node-type-policies
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, node-type-policies, api, allow-deny-delegate, nodes-exclude, enterprise]
level: advanced
status: docs-checked
description: "Block or allow n8n nodes per instance or project with node type policies through the public API: rules, delegate, version conflicts and limits."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/control-node-availability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide which nodes users may use. Preview feature, Enterprise (Cloud and self-hosted), from n8n 2.45.0; avoid relying on it in production. No settings page yet: manage with the public API.

## Model
A policy has `rules` and a `defaultAction`. A rule has `id` (unique, reported when it blocks a node), `action` (`allow`, `deny`, or `delegate`; only the instance policy accepts `delegate`) and `selector`: `{ "kind": "name", "value": "n8n-nodes-base.executeCommand" }` (exact type, also covers tool versions such as Gmail Tool) or `{ "kind": "package", "value": "n8n-nodes-base" }` (must be installed). First matching rule wins, else `defaultAction`. No wildcards. Find a node's type by copying it on the canvas and reading `type`.

Combining: instance `deny` blocks for good; `allow` lets the project policy restrict further; `delegate` blocks unless the project has an explicit `allow` rule (its `defaultAction` does not count).

## API
Send `X-N8N-API-KEY` with scope `nodeTypePolicy:manage`. Endpoints: `GET` and `PUT /api/v1/node-type-policies/instance` (owners, admins) and `/api/v1/node-type-policies/projects/<project-id>` (also that project's admins). Every policy has a `version`; `PUT` the version you read (`0` if never set) or get `409 Conflict`. `PUT` replaces all rules, so resend existing ones. Takes effect in about a second.
```json
{ "version": 0, "defaultAction": "allow", "rules": [
  { "id": "block-execute-command", "action": "deny",
    "selector": { "kind": "name", "value": "n8n-nodes-base.executeCommand" } },
  { "id": "ssh-on-request", "action": "delegate",
    "selector": { "kind": "name", "value": "n8n-nodes-base.ssh" } } ] }
```

## Effects and limits
- Existing workflows with a blocked node: open, edit and save (without adding blocked types) allowed; publish and run refused (failed execution).
- A deny-by-default policy also blocks Manual Trigger and Sticky Note; allow them explicitly.
- Not a data boundary: HTTP Request or Code can still reach the service. On self-hosted use `NODES_EXCLUDE` to stop loading nodes.
- Source control pulls skip workflows using a blocked node.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/administer/manage-users-and-access/control-node-availability

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
