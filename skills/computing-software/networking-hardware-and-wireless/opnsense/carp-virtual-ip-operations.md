---
id: computing-software.networking-hardware-and-wireless.opnsense.carp-virtual-ip-operations
name: carp-virtual-ip-operations
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [carp, vhid, high-availability, multicast, unicast]
level: advanced
status: docs-checked
description: "CARP behaviour on OPNsense: virtual MAC, protocol 112 advertisements, unicast peer, one VHID with IP aliases, state meanings and debug tunable."
sources: ["https://docs.opnsense.org/manual/firewall_vip.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CARP VIP behaviour and troubleshooting

CARP's virtual MAC is 00:00:5e:00:01:XX where XX is the VHID. It uses IP protocol number 112 and sends advertisements to 224.0.0.18 or FF02::12. Since 24.7 unicast is selectable; enter a non-CARP target address on both machines. The source address of CARP packets cannot be set from the firewall (usually the interface's first address), so if something filters between the firewalls, such as a cloud portal, allow CARP from the actual sender; use packet capture if unsure which.

Sharing several addresses: create one CARP VIP with a VHID and add normal IP Alias VIPs that use the same VHID number. The whole set becomes one virtual host: only that VHID advertises, and a hash of the address set is included in advertisements. If the peer's hash differs it assumes the master role because configuration is out of sync. The docs point to the CARP how-to for the correct procedure to add aliases to a running cluster. Multiple CARP VIPs with different VHIDs on one interface are possible but not recommended, because advertising noise and failover work grow with each; CARP mainly reacts to link state.

Status page statuses: INIT (an interface problem, often unconnected or similar), BACKUP (listening; becomes master if advertisements stop briefly), MASTER (active; may drop to backup if a better advertisement is seen, depending on the preempt setting in System > High Availability > Settings), DISABLED (after Temporarily Disable CARP). The page also has maintenance-mode buttons.

For debugging, add the tunable net.inet.carp.log with value 2 in System > Settings > Tunables, then read System > Log Files > General (kernel) or run dmesg.

## Checked

2026-11-03. Read the Virtual IPs manual page (firewall_vip.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
