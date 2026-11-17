---
id: computing-software.networking-hardware-and-wireless.opnsense.firewall-advanced-multiwan-and-routing
name: firewall-advanced-multiwan-and-routing
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [multiwan, reply-to, sticky-connections, anti-lockout, static-route-filtering]
level: advanced
status: docs-checked
description: "Advanced OPNsense firewall settings for routing: sticky connections, shared forwarding, force gateway, reply-to, skip rules and anti-lockout."
sources: ["https://docs.opnsense.org/manual/firewall_settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Advanced firewall routing options

Several options in Firewall > Settings > Advanced shape routing behaviour.

- Skip rules (Gateway Monitoring): normally, if a rule's chosen gateway is down, the rule is still created and traffic goes to the default gateway. Enabling this means the rule is not created while the gateway is down.
- Sticky connections: with a gateway group the same source keeps the same gateway while a state exists; an optional timeout changes this.
- Shared forwarding: policy routing in pf rules makes packets skip traffic shaper and captive portal processing; this option shares the forwarding decision across components for complex setups.
- Disable force gateway: by default a gateway is enforced on WAN-type interfaces (those with a gateway). It underlies the floating rule "let out anything from firewall host itself (force gw)" using route-to for non-local traffic. Disabling changes routing of local traffic bound to an address.
- Disable reply-to: by default reply-to keeps replies leaving the interface they arrived on, wanted for multi-WAN. With bridging, disable it if the WAN gateway differs from the gateway of hosts behind the bridge. Side effect: traffic from the interface's own network is also replied to the configured gateway; disable it globally and set per rule, or add a local-traffic rule above with reply-to disabled in the rule's advanced options.
- Static route filtering: with static routes defined, traffic entering and leaving the same interface bypasses the firewall; generally add per-network rules manually instead.
- Disable anti-lockout: unchecked means GUI and SSH access on LAN is always permitted regardless of rules. If you check it, make sure your own rule allows access or you lock yourself out.
- Schedule States: by default schedule expiry clears existing states; this option keeps them.

## Checked

2026-11-03. Confirmed against the OPNsense Firewall Settings (Advanced) manual page: skip rules, sticky connections, shared forwarding, force gateway, reply-to, static route filtering, anti-lockout, schedule states. Nothing removed.

Method: documentation only; no commands were run.
