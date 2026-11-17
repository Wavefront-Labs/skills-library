---
id: computing-software.networking-hardware-and-wireless.tailscale.subnet-router-high-availability
name: subnet-router-high-availability
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [subnet-router-ha, advertise-same-routes, accept-routes]
level: advanced
status: docs-checked
description: "Run two or more routers advertising identical routes and avoid accept-routes pitfalls."
sources: ["https://tailscale.com/kb/1115"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Subnet router high availability

Goal: fail over between subnet routers without changing client config.

**Steps**

1. On two or more devices in the same network, advertise the exact same route prefixes:
```
sudo tailscale set --advertise-routes=10.0.0.0/24,10.1.0.0/24
```
You can add as many routers as you want for failover. Review the prefix matching requirements before using overlapping routes.
2. Open the Machines page, open the router menu, choose Review subnet routes, then Enable the routes. Tailscale distributes them to other devices.
3. Consider disabling key expiry on the servers.

**Avoid `--accept-routes` on the routers.** If both routers advertise and accept `192.168.1.0/24`, the standby router sends that traffic through the primary even though it is local, creating an inefficient path. This applies to active-passive failover and regional routing. For most HA setups use `--advertise-routes` alone, unless you specifically need that behaviour.

**App connectors.** Run two or more with the same tag and assign your apps to that tag:
```
sudo tailscale up --advertise-connector --advertise-tags="tag:connector"
```
Then check routing from clients. Compare selection behaviour and failover timing in Route selection.

**Checklist**

1. Same prefixes everywhere.
2. Routes enabled.
3. No `--accept-routes` on routers.

## Checked

2026-11-03. Read Subnet router failover (kb/1115) and confirmed same-prefix advertising, route enabling, the `--accept-routes` caution and the app connector HA command. Nothing else was removed.

Method: documentation only; no commands were run.
