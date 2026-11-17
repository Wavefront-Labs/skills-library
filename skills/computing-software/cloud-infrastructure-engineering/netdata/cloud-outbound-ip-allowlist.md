---
id: computing-software.cloud-infrastructure-engineering.netdata.cloud-outbound-ip-allowlist
name: cloud-outbound-ip-allowlist
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, ip-allowlist, webhook-notifications, mcp-endpoint]
level: practitioner
status: docs-checked
description: "Allowlist the IPs Netdata Cloud connects from for webhooks and custom MCP servers by reading the live ips-v4 endpoint, failing closed on bad fetches."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-cloud/netdata-cloud-outbound-ips.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scope: connections from Netdata Cloud to your systems, namely webhook notifications to a webhook URL you host, and MCP connections to a Custom MCP Server or self-hosted MCP endpoint. This is the reverse of Agents connecting to Cloud; for Agent egress see firewall-egress-endpoints.

Fetch the live list (no authentication; `text/plain`, one IPv4 CIDR block per line):

```
curl -fsS https://app.netdata.cloud/ips-v4
```

Do not copy addresses from documentation; always read the live endpoint.

Automation rules:
- Refresh on a schedule and reconcile the allowlist so changes do not silently break notifications.
- Fail closed: if the fetch fails or returns an empty body, keep the previous list.
- Parse defensively: skip blank lines, trim whitespace, treat each entry as a CIDR block.

Gotchas:
- The list is IPv4 only; there is no IPv6 equivalent.
- An IP allowlist is a network control, not identity. Keep webhook authentication (mutual TLS, Basic or Bearer).

## Checked

2026-11-04: scope, endpoint behaviour (no authentication, text/plain, one IPv4 CIDR per line, IPv4 only), the curl command and the automation guidance confirmed against the Netdata Cloud outbound IP addresses page.

Method: documentation only; no commands were run.
