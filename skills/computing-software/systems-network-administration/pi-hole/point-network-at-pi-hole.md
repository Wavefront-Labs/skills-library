---
id: computing-software.systems-network-administration.pi-hole.point-network-at-pi-hole
name: point-network-at-pi-hole
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-dns-rollout, router-dhcp-dns, host-resolver]
level: intro
status: docs-checked
description: "Make clients and the Pi-hole host itself resolve through Pi-hole after installation, and avoid the host DNS catch-22."
sources: ["https://docs.pi-hole.net/main/post-install/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Point your network at Pi-hole

Installing Pi-hole does not make anything use it automatically.

**Network clients, in order of preference**

1. Configure the router so DHCP clients receive Pi-hole as their DNS server. All devices are then filtered without further changes.
2. If the router cannot set a DNS server, enable Pi-hole's built-in DHCP server and disable DHCP on the router first.
3. As a last resort, set the DNS server manually on each device.

**The Pi-hole host**

The host does not use Pi-hole by default. To make it do so, set Pi-hole as the host's upstream resolver. If the host uses `dhcpcd`, add this to `/etc/dhcpcd.conf`:

```text
static domain_name_servers=127.0.0.1
```

**Catch-22 warning.** If the host depends on Pi-hole for DNS and Pi-hole fails, the host loses name resolution. That can block repair attempts such as `pihole -r`, which needs a working internet connection. Keep a fallback in mind before pointing the host at itself.

**Checklist**

1. Set the router's DHCP DNS option (or enable Pi-hole DHCP and disable the router's).
2. Renew a client lease and confirm queries show up in the Pi-hole query log.
3. Decide deliberately whether the host should use Pi-hole.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Post-Install (main/post-install). Nothing needed removing.
Method: documentation only; no commands were run.
