---
id: computing-software.systems-network-administration.dns-dhcp.clients-getting-wrong-dhcp-options
name: clients-getting-wrong-dhcp-options
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, wrong-dhcp-options, option-precedence, client-classes, troubleshooting]
level: practitioner
status: docs-checked
description: "Diagnose clients receiving wrong DHCP options: option precedence (global, subnet, pool, class, reservation), rogue servers, relays and client caching."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcpv4-option-precedence
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-top
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clients getting wrong options

## Step 1: what did the client receive, and from whom? (practitioner advice)
Capture the DHCP ACK and read the server identifier. An unexpected server ID means a rogue or secondary server answered; stop there and find it. Windows DHCP servers can be authorised in Active Directory so that unauthorised servers do not hand out addresses (Microsoft Learn).

## Step 2: option precedence
- Kea: options can be set at host reservation, pool, subnet, shared network, class and global scope. The documented order, most important first, is host reservation, pool, subnet, shared network, class, global.
- Windows DHCP: offers reservations (a fixed address per client), DHCP policies that apply options by client characteristics such as MAC address or vendor class, and server and scope option levels. Precedence between these levels is not stated on the page read; check the Windows scope/policy documentation for your version.

Typical causes (practitioner experience):
| Symptom | Cause |
|---------|-------|
| Old DNS servers handed out | A more specific level (scope, pool, reservation) still holds the old value |
| PXE clients get the wrong boot file | Class or policy match too broad |
| Router wrong on one VLAN | Wrong subnet selected (relay or giaddr mismatch) |
| Option never arrives | Client did not request it (see step 3) |

## Step 3: requested versus forced options (Kea)
- Kea adds a defined option to the response when the client requests it, with a few exceptions that are always added.
- Setting `"always-send": true` on the option forces it; `"never-send": true` stops it being added, and never-send wins when both are set.
- These two flags are sticky: if enabled anywhere in the inheritance chain they apply, even when disabled at a higher-priority level.
- They have no effect on options that cannot be requested, such as options in a custom space.

## Step 4: client caching (practitioner advice)
Clients keep options until they renew. After fixing the server, force a renew or reconnect (release and renew on the client, or reboot the device). Some devices, such as IP phones, may keep TFTP or boot server values until reset.

## Verify
- [ ] A fresh ACK from the intended server contains the corrected options and the client shows them.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Kea DHCPv4 option precedence/always-send/never-send text and the Microsoft Learn DHCP overview (policies, reservations, authorisation). Removed as unsupported: the Wireshark filters, the Windows and Cisco IOS precedence chains, the Windows "always sends configured options" claim, the VoIP option 150/66 row, the ipconfig/dhclient/nmcli commands and the kea debug log name. Steps marked practitioner advice are not from the cited pages.
