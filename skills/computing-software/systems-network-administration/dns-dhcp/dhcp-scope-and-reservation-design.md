---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-scope-and-reservation-design
name: dhcp-scope-and-reservation-design
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv4, dhcpv6, dhcp-scope, scope-sizing, lease-duration, lease-time, dhcp-reservation, exclusion-range, client-identifier, mac-randomisation, private-wifi-address, dhcp-failover, load-balance, hot-standby, mclt, split-scope, kea, kea-ha, isc-dhcp, windows-dhcp, dhcpserver-powershell, dhcp-policies, pxe, option-66, option-67, option-93, option-43, option-82, relay-agent, superscope, shared-network, scope-exhaustion, slaac]
level: practitioner
status: docs-checked
description: "Design DHCP scopes: sizing and lease times per segment, reservations vs statics, Windows failover and Kea HA, PXE by client architecture, exhaustion monitoring."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-top
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/
  - https://kea.readthedocs.io/en/latest/
  - https://datatracker.ietf.org/doc/html/rfc2131
  - https://datatracker.ietf.org/doc/html/rfc4578
  - https://www.rfc-editor.org/rfc/rfc2132
  - https://www.rfc-editor.org/rfc/rfc3046
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP scope and reservation design — never run out, never single-home

**Goal:** scopes sized and timed for how each segment is really used, reservations that
survive device quirks, and a DHCP service that keeps leasing when a server dies.
DORA, relays and the basic options (3/6/15) are in
`computing-software.systems-network-administration.dns-dhcp.dns-records-and-resolution-troubleshooting`.

## 1. Size the scope
- Count **peak concurrent devices**, not people: laptop + phone + tablet per person on
  Wi-Fi, plus devices that come and go during the lease time.
- Effective demand ≈ peak concurrent + (arrivals per lease period × churn). Short leases
  shrink the second term.
- Target peak utilisation ≤ ~80%; alert at 80, act at 90.
- If a scope is too small, enlarge the subnet (re-plan the VLAN) rather than adding a
  second subnet to the same VLAN (superscope/shared-network). Multinetting works but
  makes routing, ACLs and troubleshooting harder.

## 2. Lease time per segment
| Segment | Typical lease | Why |
|---|---|---|
| Guest / public Wi-Fi | 1–4 h | high churn, many one-off devices |
| Corporate Wi-Fi | 8–24 h | daily churn |
| Wired desktops | 3–8 days | stable, survives long weekends/outages |
| Servers, printers, infra | reservations or statics | must not change |
By default clients start renewing at 50% of the lease (T1, RFC 2131), so a 1-hour lease means renewals every 30 min:
more DHCP load, and DNS dynamic-update churn. Very short leases plus a DHCP outage hurt
fastest; long leases buy time to fix a dead server.

## 3. Reservations vs statics vs exclusions
- **Reservation:** DHCP always gives this client this IP. Central record, options still
  delivered. Prefer for printers, APs, cameras, appliances.
- **Static:** configured on the device; put it in an **excluded** range (or outside the
  pool) and record it in IPAM. Use for DHCP servers, gateways, DNS servers, hypervisor
  hosts and anything needed to bring DHCP itself up.
- **MAC randomisation:** a device that uses a different MAC per SSID breaks MAC reservations and
  MAC-based NAC. Disable it per SSID on managed devices via MDM, or reserve by client
  identifier where the platform supports it.
- Devices that send a client-id (option 61) different from their MAC get a different lease from the OS than from firmware; reserve by the
  identifier they actually send (check a capture or the server log).

## 4. Redundancy
- **Windows DHCP failover**, per scope, between two servers:
  - *Load balance* (default 50/50) for two servers in one site;
  - *Hot standby* for a hub-and-branch design (standby keeps a reserve, default 5%).
  - MCLT (default 1 h) limits how far one partner can extend a lease alone; in
    partner-down state the survivor takes the whole pool only after MCLT.
  ```powershell
  Add-DhcpServerv4Failover -Name 'DHCP1-DHCP2' -PartnerServer dhcp2.corp.example `
      -ScopeId 10.10.10.0 -LoadBalancePercent 50 -SharedSecret '<FAILOVER_SECRET>'
  ```
  Replicate changes to a failover-enabled scope manually
  (`Invoke-DhcpServerv4FailoverReplication`) from the server whose settings you want to keep.
- **Kea**: the HA hook in `load-balancing`,
  `hot-standby` or `passive-backup` mode; or a shared database lease backend.
- **Split scope**, two servers with non-overlapping pools, is the legacy fallback
  when neither supports failover.
- Relays must point at **both** servers (`ip helper-address` twice).

## 5. Options and policies
- **PXE for mixed BIOS/UEFI**: do not set static options 66/67 for everyone. Use
  policies (Windows DHCP policies or Kea client classes) matching option 93 (client
  architecture, RFC 4578): `0` (Intel x86PC) → a BIOS loader; `7` (EFI BC) or `9` (EFI x86-64) →
  the EFI loader.
  Better still, IP helpers to the PXE server and no 66/67 at all where the deployment tool
  supports it.
- Option 43 (vendor-specific) carries controller addresses for APs/phones; its format is
  vendor-defined. Copy the vendor's exact encoding.
- Option 82 (relay agent information, RFC 3046) lets you assign by switch/port.
- IPv6: decide per segment between SLAAC, stateless DHCPv6 (options only), or
  stateful DHCPv6.

## 6. Monitor
```powershell
Get-DhcpServerv4ScopeStatistics
Get-DhcpServerv4Failover | Select Name, State, PartnerServer
```
Kea: query `statistic-get-all` via the control agent; graph assigned vs total addresses.
Watch also for many DECLINEs (address conflict) and NAKs (clients from wrong subnets).

## Verify
- [ ] Every scope ≤ 80% at peak; alerting in place.
- [ ] Lease times chosen per segment and documented.
- [ ] Infra on statics in excluded ranges; appliances on reservations; MAC randomisation handled.
- [ ] Failover/HA state "Normal" on all scopes; relays list both servers.
- [ ] One DHCP server stopped in a test: clients still obtain and renew leases.
- [ ] PXE boot works for both a BIOS and a UEFI client.

## Checked
2026-10-28. Confirmed against the Microsoft Learn DHCP failover overview and Add-DhcpServerv4Failover reference (load balance default 50:50, hot standby reserve default 5%, MaxClientLeadTime default 1 hour, DHCPv4 scopes only, manual replication), RFC 2131 (T1 defaults to 0.5 of the lease), RFC 4578 (option 93 types 0, 7, 9), RFC 2132 (options 15, 43, 61, 66, 67) and RFC 3046 (option 82). Removed as unconfirmed: Windows default 8-day lease, failover version gate, ISC DHCP end-of-life date, 80/20 split figure, reservation-in-exclusion rule, MAC randomisation platform detail, Android DHCPv6 claim, vendor option 43 encoding, `PercentageInUse` filter.
Method: documentation only; no commands were run.
