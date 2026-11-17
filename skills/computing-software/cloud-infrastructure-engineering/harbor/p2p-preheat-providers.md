---
id: computing-software.cloud-infrastructure-engineering.harbor.p2p-preheat-providers
name: p2p-preheat-providers
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [p2p-preheat, dragonfly, kraken, preheat-provider, harbor]
level: practitioner
status: docs-checked
description: "Add Dragonfly or Kraken preheat provider instances to Harbor, choose auth mode, check version compatibility and know the delete restriction."
sources:
  - https://goharbor.io/docs/main/administration/p2p-preheat/
  - https://goharbor.io/docs/main/administration/p2p-preheat/manage-preheat-providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
P2P preheating pushes matching images into a P2P engine cache before pulls. Harbor supports Dragonfly (v1.0.5+) and Kraken (v0.1.3+). Install the P2P engine first. Kraken needs extra setup from its Harbor integration guide because of preheat API limits.

Roles: the system administrator creates provider instances, usable by all projects. A project admin then creates preheat policies in a project with resource filters and criteria (content trust and vulnerability status), triggered manually, on a schedule or by events.

Create an instance under Administration, **Distributions**, **+NEW INSTANCE**:
1. **Provider**: Dragonfly or Kraken.
2. Name, optional description.
3. Preheat API endpoint, for example `http://my-provider.com` or `http://my-provider.com:8002`.
4. **Auth Mode**: NONE, Basic (username and password) or OAuth (bearer token).
5. **Enable** checkbox, and optionally **Skip certificate verification** for self-signed certificates.
6. **TEST CONNECTION**, then **OK**.

The list shows a **Healthy** status when connectivity works. **ACTIONS** offers Edit, Enable or Deactivate, and Delete. Only instances not referenced by any preheat policy can be deleted, so delete the policies first.

Version compatibility: Harbor `>=v2.12.0` pairs with Dragonfly `>=v2.1.59`; Harbor `<v2.12.0` pairs with Dragonfly `>=v1.0.5, <v2.1.59`. Dragonfly v1 is archived and v2 is not compatible with it.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: P2P Preheat and Manage Preheat Providers.
Method: documentation only; no commands were run.
