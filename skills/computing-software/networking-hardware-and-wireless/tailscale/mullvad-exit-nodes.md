---
id: computing-software.networking-hardware-and-wireless.tailscale.mullvad-exit-nodes
name: mullvad-exit-nodes
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [mullvad, mullvad-exit-nodes, dns-leaks]
level: advanced
status: docs-checked
description: "Know the requirements, limitations and DNS considerations for Mullvad exit nodes."
sources: ["https://tailscale.com/kb/1258"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mullvad exit nodes

Goal: avoid known pitfalls with the Mullvad add-on.

**Requirements and limitations**

- The Mullvad VPN add-on must be purchased before Mullvad exit nodes are available.
- They do not work with custom DERP servers.
- Access policies for Mullvad exit nodes do not work with Google-synced groups.
- With Tailnet Lock, you must sign each Mullvad exit node.
- If you manage the policy file with GitOps, the checkout flow might be locked; buy extra licenses on the Billing page.
- The Windows client does not show the full list of Mullvad exit nodes; use the CLI.
- You cannot manage Mullvad access using both the admin console and the policy file; if you use the policy file, manage all access there.

**DNS considerations**

- Tailscale v1.48.3 and later need no extra configuration.
- v1.48.1 and v1.48.2 use the device's local DNS, so you may lose DNS unless you allow local network access for exit nodes or add a global nameserver with Override DNS servers.
- Overriding local DNS makes all clients use the chosen DNS server for all queries while connected, even without an exit node.
- Allowing LAN access can permit DNS leaks but keeps local names (printers, NAS) resolving.

**Checklist**

1. Sign nodes if using Tailnet Lock.
2. Pick one management method.
3. Check client version for DNS behaviour.

## Checked

Confirmed against Tailscale kb/1258 (Mullvad exit nodes), read in full: every listed requirement and limitation, the v1.48.1 to v1.48.3 DNS behaviour, and the override DNS and local network access trade-offs. Nothing was removed.

Method: docs-checked 2026-11-09 against https://tailscale.com/kb/1258
