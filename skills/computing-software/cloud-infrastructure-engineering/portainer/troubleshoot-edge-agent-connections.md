---
id: computing-software.cloud-infrastructure-engineering.portainer.troubleshoot-edge-agent-connections
name: troubleshoot-edge-agent-connections
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [edge-agent, troubleshooting, telnet, firewall, tls]
level: practitioner
status: docs-checked
description: "Diagnose an Edge Agent that cannot reach the Portainer Server by checking Edge Compute settings, ports 9443 and 8000, and TLS handshakes."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/faqs/troubleshooting/agents-and-environment-management/troubleshooting-edge-agent-connection-issues.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start in Settings, Edge Compute: confirm the Portainer API Server URL and the tunnel address are correct as seen from the Edge environment, and that ports 9443 and 8000 are open in your firewall.

Then scope the problem. If only one agent fails, suspect that environment's network or configuration; if other Edge Agents connect fine, the Server configuration is likely correct.

Test reachability from the Edge host:

```
telnet <Portainer IP> 9443
```

Success means traffic is not blocked, so look elsewhere. Next run `curl -v https://<PortainerServerURL>:9443` from the Edge host to verify connectivity and surface TLS handshake errors. "Connection reset by peer" usually means the connection was closed early by a firewall, incorrect TLS configuration or another network issue. A self-signed Server certificate requires the agent to be deployed with `EDGE_INSECURE_POLL=1`. If settings and firewall rules look right but it still fails, subtle network issues such as VLAN or firewall rules may be the cause.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed unconfirmed agent-log, DNS and many-agents-fail advice; added the documented curl command and Connection reset meaning.

Method: documentation only; no commands were run.
