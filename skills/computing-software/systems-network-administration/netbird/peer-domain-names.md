---
id: computing-software.systems-network-administration.netbird.peer-domain-names
name: peer-domain-names
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, peer-dns-names, netbird-cloud-domain, hostname-collisions, rename-peer]
level: intro
status: docs-checked
description: "How NetBird names peers under netbird.cloud, how to rename them, and what the Reject Hostname Collisions setting does when a name is already taken."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/index.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/register-machines-using-setup-keys.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From v0.11.0 each peer gets a DNS name under `netbird.cloud`, such as `my-server.netbird.cloud`.

- The Domain Name field cannot be edited directly; rename the peer to change it.
- If a name is already taken, the peer gets an IP-based suffix.
- Settings > Clients > Reject Hostname Collisions makes the rename fail instead of adding a suffix.

Ephemeral peers: they get a suffix built from the last two octets of the NetBird IP (for example `ci-runner-12-7.netbird.cloud`) even when nobody else uses the plain name. With Reject Hostname Collisions on they get plain names, but any peer whose name is taken then fails to register. Leave it off if ephemeral peers intentionally share a hostname.

Set a hostname at login with `netbird up --hostname <name>`.

Linux resolves peer names without custom nameservers. On macOS, Windows and mobile, DNS is only changed when nameservers are configured; otherwise use the NetBird IPs.

For extra names beyond the hostname, use extra DNS labels.

## Checked

2026-11-04: read the DNS overview page (automatic peer domain names, default behaviour per platform), the setup keys page (ephemeral peers and the collision toggle) and the CLI page for the hostname flag. Confirmed the v0.11.0 start, rename rule, suffix format, toggle effects and platform behaviour. Nothing removed.

Method: documentation only; no commands were run.
