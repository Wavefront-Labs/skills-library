---
id: computing-software.collaboration-platform-administration.zulip.network-ports-and-firewall
name: network-ports-and-firewall
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-firewall, network-requirements, port-4369, epmd]
level: practitioner
status: docs-checked
description: "Plan the network exposure of a Zulip server: HTTPS 443, optional 80 and 25, protecting epmd port 4369, outbound access, DNS name and Smokescreen."
sources: ["https://zulip.readthedocs.io/en/latest/production/requirements.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip network and firewall requirements

Inbound traffic Zulip needs:

- HTTPS, normally port 443 (the port is configurable), from wherever users are.
- Port 80 is optional. Zulip only serves content over HTTPS and redirects HTTP to it.
- Port 25 only if you enable the incoming email gateway.
- SSH on port 22 is not needed by Zulip itself but most installs want it for administration.

Block port 4369 with a firewall. It is `epmd`, an Erlang service that cannot bind to localhost only. Left open, anyone can learn that RabbitMQ is running and on which port, although nothing further leaks.

Outbound traffic: HTTP and HTTPS (ports 80 and 443) to the public Internet, used for image and website previews and for mobile push notifications. You can skip this if you disable those features. You also need outbound SMTP, usually port 587, to your mail provider.

You need a domain name such as `zulip.example.com` for users. A public DNS name makes Certbot certificates and services like Google authentication simpler. A non-public domain or even an IP address can be the external hostname, but that is not recommended.

Zulip can run behind a reverse proxy. It also routes outgoing HTTP through Smokescreen, a proxy that prevents server-side request forgery against private resources. If your network already has an outgoing HTTP proxy, Zulip can use that instead.

Certificates and SMTP credentials are the two credentials to prepare before installing.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/requirements.html (zulip.readthedocs.io, latest). Removed: nothing.

Method: documentation only; no commands were run.
