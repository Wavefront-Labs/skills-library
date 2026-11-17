---
id: computing-software.systems-network-administration.network-design.active-directory-firewall-ports
name: active-directory-firewall-ports
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, active-directory-ports, kerberos, ldap, rpc-dynamic-ports, smb, firewall-rules]
level: practitioner
status: docs-checked
description: "Open the right ports between clients, DCs and member servers for Active Directory: Kerberos, LDAP/GC, SMB, DNS, RPC endpoint mapper and the dynamic range, and how to restrict RPC."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/service-overview-and-network-port-requirements
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-domains-and-trusts
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/restrict-ad-rpc-traffic-to-specific-port
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active Directory firewall ports

## Client/member server -> domain controller
| Port | Proto | Service |
|---|---|---|
| 53 | TCP/UDP | DNS |
| 88 | TCP/UDP | Kerberos |
| 123 | UDP | W32Time |
| 135 | TCP | RPC endpoint mapper |
| 137-138 / 139 | UDP / TCP | NetBIOS (legacy; only if needed) |
| 389 | TCP/UDP | LDAP |
| 445 | TCP | SMB (SYSVOL/NETLOGON, Group Policy) |
| 464 | TCP/UDP | Kerberos password change |
| 636 | TCP | LDAPS |
| 3268 / 3269 | TCP | Global Catalog / GC over TLS |
| 49152-65535 | TCP | RPC dynamic (Netlogon, replication, DFSR) |
| 9389 | TCP | AD Web Services (PowerShell AD module) |

DC <-> DC replication needs the same set both ways plus the dynamic range.

## Restricting the dynamic range
Rather than opening 16k ports through a firewall:
- Pin AD replication: `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters\TCP/IP Port`
  (DWORD) to e.g. 50000.
- Pin Netlogon: `HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters\DCTcpipPort`.
- Pin DFSR to a static port with `Dfsrdiag.exe` (see the service overview page).
- Or narrow the whole RPC range through Windows' dynamic-port settings.
Restart services/DCs after the change and update firewall rules.

## Testing
```
Test-NetConnection dc01 -Port 88
```
Test each TCP port from each client zone; UDP ports need the real protocol client, not a port check.

## Verify
- [ ] Directory replication and Group Policy refresh succeed across the firewall from a client in each zone.

## Checked

- Date: 2026-10-28
- Confirmed: ports 53, 88, 123, 135, 389, 445, 464, 636, 3268, 3269, 9389 and the 49152-65535 dynamic range, the NTDS TCP/IP Port and Netlogon DCTcpipPort registry values, and Dfsrdiag.exe (Microsoft Learn service overview, firewall for domains and trusts, restrict AD RPC pages).
- Removed: the 5722 DFSR port, netsh dynamicport syntax, portqry, nltest, dcdiag, repadmin and gpupdate, the LDAP-ping remark, the Kerberos-over-TCP remark.

Method: documentation only; no commands were run.
