---
id: computing-software.cloud-infrastructure-engineering.netdata.firewall-egress-endpoints
name: firewall-egress-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, firewall, egress-allowlist, port-19999]
level: practitioner
status: docs-checked
description: "Firewall and security-platform rules for Netdata: inbound and outbound ports, the outbound domains and how to disable each connection."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configure-netdata-for-cybersecurity-platforms.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ports:
- 19999/TCP inbound: local dashboard and Child streaming (`[web] port`).
- 19999/TCP outbound: Child to Parent streaming.
- 443/TCP outbound: ACLK, anonymous telemetry, automatic updates.

Outbound domains (443):
- `app.netdata.cloud`, `api.netdata.cloud`, `mqtt.netdata.cloud`: only when the node is connected to a Space; avoid by not connecting to Cloud.
- `us-east1-netdata-analytics-bi.cloudfunctions.net`: telemetry, on by default; disable with `--disable-telemetry` or the opt-out file.
- `repository.netdata.cloud`: packages and auto-updates; disable with `--no-updates` at install or by disabling `netdata-updater.sh`.
- `get.netdata.cloud`: installer script, install time only.
- Dashboard page-view telemetry goes from the browser to PostHog, so browser proxy policy governs it.

Access models: Cloud-only with `[web] mode = none` (not on Parents); gateway/reverse proxy with `bind to = 10.0.0.15:19999 localhost:19999`; management network with `allow connections from = localhost 10.*`.

Recommendations: never expose 19999 directly to the internet; use HTTPS at the published entry point; prefer domain allowlists over IPs; allow Cloud egress if using claiming, Cloud dashboards or bearer token protection.

Security products may block the Agent because it monitors network and CPU activity; add an exclusion for the Netdata executable if needed.

## Checked

2026-11-04. Confirmed against the Netdata page on configuring for cybersecurity platforms: ports and protocols, [web] port, the four Cloud domains, telemetry, repository and get domains with their disable methods, the PostHog browser note, the three access models and their example settings, the recommendations list, and the Sophos behaviour note. Nothing removed.

Method: documentation only; no commands were run.
