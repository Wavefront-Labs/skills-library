---
id: computing-software.systems-network-administration.headscale.web-ui-and-tools
name: web-ui-and-tools
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, web-ui, headplane, operator, exporter, third-party]
level: intro
status: docs-checked
description: "Headscale has no built-in web UI; community web interfaces and tools (Headplane, operator, exporters, migration tools) and their support status."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/web-ui.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/integration/tools.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/api.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web UIs and third-party tools

Headscale doesn't provide a built-in web interface. Everything below is community-contributed and not maintained by the headscale authors. Ask for UI support on the Discord "web-interfaces" channel.

## Web UIs (examples from the list)

- Headplane (tale): advanced frontend inspired by Tailscale.
- headscale-ui (gurucomputing), headscale-admin (GoodiesHQ), HeadscaleUi (simcu): admin interfaces.
- ouroboros (yellowsink): for users managing their own devices.
- unraid-headscale-admin (ich777): Unraid, local `docker exec` and API modes.
- headscale-console (rickli-cloud): WebAssembly-based client supporting SSH, VNC and RDP with optional self-service capabilities.
- headscale-piying (wszgrcy): visual ACL configuration.

## Tools

- headscale-operator: Kubernetes operator.
- tailscale-manager: manages route advertisements dynamically.
- headscalebacktosqlite: migrates the database from PostgreSQL back to SQLite.
- headscale-pf: populates user groups from Jumpcloud or Authentik.
- headscale-client-go: Go client for the HTTP API.
- headscale-zabbix: Zabbix monitoring template.
- tailscale-exporter: Prometheus exporter using the headscale API.

## Notes

- The Headscale API, which a web interface integrates with, requires an API key (api-keys-rest).
- The policy can be stored in the database, which the policy page says is typically only required when a web interface is used (policy-basics).

## Checked

2026-11-04. Confirmed against the Headscale web interfaces and tools pages (project names, owners and descriptions as listed; only a selection is given), the API page and the policy page footnote. Removed the advice to vet third-party code, which the pages do not give.

Method: documentation only; no commands were run.
