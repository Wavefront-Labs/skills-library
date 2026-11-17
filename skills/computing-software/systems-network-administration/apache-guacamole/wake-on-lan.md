---
id: computing-software.systems-network-administration.apache-guacamole.wake-on-lan
name: wake-on-lan
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, wake-on-lan, wol, wol-send-packet, wol-mac-addr, wol-broadcast-addr, magic-packet]
level: practitioner
status: docs-checked
description: "Wake a sleeping host before a Guacamole connection with wol-send-packet, wol-mac-addr, wol-broadcast-addr, wol-udp-port, wol-wait-time."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wake-on-LAN

Set on any connection:
| Parameter | Default |
|---|---|
| `wol-send-packet` | `false`; `true` sends a magic packet before connecting |
| `wol-mac-addr` | required when sending is enabled |
| `wol-broadcast-addr` | 255.255.255.255 (IPv4 broadcast or IPv6 multicast address) |
| `wol-udp-port` | 9 |
| `wol-wait-time` | optional; seconds to wait before the first connection attempt |

Behaviour: by default Guacamole connects immediately after sending the packet; a positive `wol-wait-time` delays the first attempt so the target can boot.

Checklist:
1. Configure the target and network for WoL; the manual notes that several factors outside Guacamole affect it.
2. Set `wol-mac-addr` to the target NIC.
3. Set `wol-broadcast-addr` if the default local broadcast does not reach the target.
4. Set `wol-wait-time` to give the target time to boot.

Verify: shut the target down, connect, and watch the session come up.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Guacamole manual Configuring Guacamole page: the Wake-on-LAN section was read in full; other sections were not. Confirmed: parameters wol-send-packet (default off), wol-mac-addr (required when sending), wol-broadcast-addr (default 255.255.255.255), wol-udp-port (default 9) and wol-wait-time (seconds, positive value, optional). Removed the five-retries claim and the guacd layer-2 placement claim, which the page does not state, and reworded the BIOS and directed-broadcast checklist items to what the page says.
