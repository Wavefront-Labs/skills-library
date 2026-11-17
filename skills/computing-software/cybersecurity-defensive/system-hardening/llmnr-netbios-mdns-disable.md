---
id: computing-software.cybersecurity-defensive.system-hardening.llmnr-netbios-mdns-disable
name: llmnr-netbios-mdns-disable
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-hardening, llmnr-netbios-disable, llmnr, nbt-ns, mdns, name-poisoning, responder]
level: practitioner
status: docs-checked
description: "Disable LLMNR, NBT-NS and mDNS name resolution fallbacks across Windows fleets via GPO, DHCP and registry to stop Responder-style credential capture."
sources: ["https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-admx-dnsclient", "https://attack.mitre.org/techniques/T1557/001/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disable LLMNR, NBT-NS and mDNS

**Goal:** Windows hosts never broadcast name lookups that an attacker on the LAN can answer to harvest NTLM hashes.

## LLMNR
GPO: Computer Configuration > Administrative Templates > Network > DNS Client > **Turn off multicast name resolution** = Enabled.
The policy writes the `EnableMulticast` value (see the DNS Client ADMX policy reference).

## NetBIOS over TCP/IP (NBT-NS)
No single GPO setting. Options:
- The DNS Client policy "Configure NetBIOS settings" exists in newer Windows builds (see the DNS Client ADMX policy reference for the supported versions).
- Otherwise disable NetBIOS over TCP/IP per network adapter (adapter properties, DHCP option or script); the exact registry value and DHCP option names were not confirmed in this review, so check Microsoft's NetBT documentation before scripting.

## mDNS
Windows can answer mDNS queries. Block inbound UDP 5353 with the host firewall or disable mDNS through the DNS client settings your Windows build supports. Check printing/casting dependencies first.

## Also
- Make sure internal DNS resolves everything users need; these protocols are fallbacks for failed DNS.

## Verify
- [ ] Run Responder in analyse mode (`-A`) on a test segment: no LLMNR/NBT-NS/mDNS queries from managed hosts.
- [ ] Adapter settings show NetBIOS over TCP/IP disabled on all interfaces.

## Checked

2026-10-28. Confirmed against: Microsoft Learn Policy CSP ADMX_DnsClient (Turn off multicast name resolution, EnableMulticast, Configure NetBIOS settings, NetBT FQDN queries).

Removed as unconfirmed: NetBT registry value and path, DHCP option 001 detail, per-interface script, mDNS registry value, WPAD bullet, Responder verification detail, Windows version claims.

Method: documentation only; no commands were run.
