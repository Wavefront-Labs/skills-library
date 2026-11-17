---
id: computing-software.cloud-infrastructure-engineering.portainer.edge-agent-join-token-and-ports
name: edge-agent-join-token-and-ports
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [edge-agent, edge-key, edge-id, ports, tls]
level: advanced
status: docs-checked
description: "Understand how the Edge Agent finds and trusts the Server, including the EDGE_KEY contents, Edge ID, ports 9443 and 8000 and self-signed certificates."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/edge-agent.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Edge architecture means only the environments need to reach Portainer; Agents never need to be exposed to the internet. Portainer needs only TCP ports 9443 and 8000 exposed. The API and UI used to be served on 9000; the API was extended so remote agents can poll for instructions on 9443, and 8000 is a TLS tunnel server used on demand.

When you create an Edge environment you give it a friendly name and confirm the FQDN:PORT agents will use to connect. Make sure the name resolves in DNS. An Edge ID, a random UUID, is generated per environment and appears in the command Portainer shows.

The join token `EDGE_KEY` is unique per environment and is base64-encoded data separated by pipe characters containing:

- the Portainer API URL (how the agent calls home);
- the reverse tunnel server address (the same host with the tunnel port, 8000 by default, unless changed at deployment or in Edge Compute settings);
- the tunnel server fingerprint, which prevents man-in-the-middle attacks when the tunnel is created;
- the environment identifier.

If the Server uses a self-signed certificate, deploy agents with `-e EDGE_INSECURE_POLL=1`.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
