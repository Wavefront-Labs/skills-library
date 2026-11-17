---
id: computing-software.systems-network-administration.dns-dhcp.client-dns-registration
name: client-dns-registration
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, client-dns-registration, dynamic-dns, windows, ipconfig-registerdns]
level: practitioner
status: docs-checked
description: "Get clients to register their own A/PTR records: Windows DNS client refresh, DHCP option 81 (Client FQDN) interplay and secure dynamic updates."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/configure-dns-dynamic-updates-windows-server-2003
  - https://www.rfc-editor.org/rfc/rfc4702
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Client DNS registration

The Learn source here is an older (Windows Server 2003 era) article; treat version-specific defaults as a starting point and test on your own servers.

## Windows clients
- By default Windows registers A and PTR resource records every 24 hours regardless of the computer's role; the interval can be changed with the `DefaultRegistrationRefreshInterval` registry entry (key path on the Learn page).
- Force an update of the registration with `ipconfig /registerdns`.
- An update that changes nothing leaves the zone at its current version; zone changes happen only if names or addresses actually change.
- DNS has no release or tombstone mechanism: names are not removed when a host goes inactive, though clients try to delete or update old records when a name or address changes. Configure aging and scavenging to clear stale records.
- Windows DNS clients try a nonsecure dynamic update first and, if it is refused, a secure update. Secure dynamic update is supported only for AD-integrated zones, and a zone that becomes AD-integrated enables only secure updates by default.

## DHCP-registered records (option 81)
- A DHCP server can register A and PTR records on behalf of its clients, using the Client FQDN option (option 81) sent in the DHCPREQUEST.
- With default server settings, the DHCPACK's option 81 tells the client that the server will register the PTR record and the client will register its own A record.
- If the request carries no option 81, the server leases without option 81.
- RFC 4702 defines the option: the client states whether it will update the forward (A/AAAA) mapping itself or asks the server to do it, and may ask the server to perform no DNS updates.
- Windows DHCP servers doing secure updates on behalf of clients with secure dynamic updates and Windows DNS servers may leave stale records; the Learn article walks through an example.

## Troubleshooting
| Symptom | Check |
|---------|-------|
| Record missing | zone allows dynamic updates (secure only for AD-integrated), client registration enabled |
| Update refused | zone's secure-update setting and who owns the existing record |
| Stale record with old IP | aging and scavenging; both DHCP server and client updating |

## Verify
- [ ] After `ipconfig /registerdns`, the name resolves to the new address on every DNS server that hosts the zone.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the Learn dynamic updates article (searched for the cited claims) and RFC 4702 option text. Removed as not stated by those pages: GPO path and NIC dialog path, event IDs 8018-8020, the Linux SSSD settings and nsupdate example, and the IP/zone examples.
