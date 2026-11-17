---
id: computing-software.networking-hardware-and-wireless.tailscale.subnet-router-setup
name: subnet-router-setup
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [subnet-router, advertise-routes, ip-forwarding]
level: practitioner
status: docs-checked
description: "Turn a Linux node into a subnet router that exposes non-Tailscale devices to the tailnet."
sources: ["https://tailscale.com/kb/1019"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Set up a subnet router

Goal: let tailnet devices reach machines that cannot run the Tailscale client.

**Steps on Linux**

1. Enable IP forwarding. If `/etc/sysctl.d` exists:
```
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```
Otherwise append the same two lines to `/etc/sysctl.conf` and run `sudo sysctl -p /etc/sysctl.conf`.
2. If the node uses firewalld, a known issue may need `firewall-cmd --permanent --add-masquerade`.
3. Advertise routes with a comma-separated list:
```
sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24
```
4. Approve the routes: Machines page, find the Subnets badge (or filter `property:subnet`), open the Subnets section, select routes, Save. You can skip this if `autoApprovers` covers the route.
5. Add an access rule whose `dst` includes the subnet; for example a grant with `"ip": ["*:*"]`.

**Facts to remember**

- Subnet routers use SNAT by default, so traffic appears to come from the router.
- Access rules control permitted traffic; route approval controls which routes are injected into client routing tables. They are separate mechanisms.
- All platforms except Apple TV support IPv4 and IPv6 subnets; Apple TV supports IPv4 only.
- Key expiry is disabled by default on tagged devices; disable it on a server to avoid reauthenticating.

**Checklist**

1. Forwarding enabled.
2. Routes advertised and approved.
3. Access rule covers the subnet.
4. Key expiry handled.

## Checked

2026-11-03. Read Subnet routers (kb/1019) and confirmed sysctl forwarding steps, firewalld note, route approval, SNAT default, IPv4/IPv6 support and key-expiry note. Nothing else was removed.

Method: documentation only; no commands were run.
