---
id: computing-software.systems-network-administration.dns-dhcp.dhcp-client-identifier-option-61
name: dhcp-client-identifier-option-61
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, option-61, client-identifier, chaddr, reservations, duid]
level: practitioner
status: gated
description: "Handle DHCP client identifier option 61 vs chaddr: how servers key leases, reservation mismatches, dual-boot/PXE duplicates and Kea/Windows settings."
sources:
  - https://www.rfc-editor.org/rfc/rfc2132#section-9.14
  - https://www.rfc-editor.org/rfc/rfc4361
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#using-client-identifier-and-hardware-address
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html
  - https://networkmanager.dev/docs/api/latest/nm-settings-nmcli.html
  - https://www.freedesktop.org/software/systemd/man/latest/machine-id.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client identifier option 61 vs chaddr

Servers identify a DHCPv4 client by option 61 (client identifier) if present, otherwise by the
hardware address (chaddr). Different software on the same NIC sends different identifiers, so the
same machine can get two leases or miss its reservation.

## Typical identifiers
| Client | Option 61 |
|--------|-----------|
| Windows | `01` + MAC (type 1 = Ethernet) (gated: unconfirmed, source is paywalled or blocked) |
| PXE ROM | often none or `01`+MAC (gated: unconfirmed, source is paywalled or blocked) |
| systemd-networkd | `ClientIdentifier=` defaults to `duid`: RFC 4361 form, type `ff` + IAID + DUID, with the DUID from `DUIDType=` (default `vendor`, a hash of machine-id); `mac` uses the hardware address |
| NetworkManager | `ipv4.dhcp-client-id`: a hex string is sent as given (first byte = type, e.g. `01:` + MAC), `mac`/`perm-mac` send type 01 + MAC, `duid` sends an RFC 4361 identifier using a DUID hashed from /etc/machine-id |
| ISC dhclient | whatever `send dhcp-client-identifier` says in dhclient.conf, e.g. `1:0:a0:24:ab:fb:9c` in its man page |
| Cloned VMs | identical identifiers when the image carries the same machine-id (machine-id(5): images should ship it empty or missing) |

## Symptoms
- A host gets one IP in PXE/installer and another in the OS (two leases, pool drains faster).
- Reservation by MAC ignored because the server matched on client-id first (or vice versa).
- Cloned VMs that carry the same identifier all contend for one lease.

## Server settings
Kea:
```json
"match-client-id": true,                     // default; false = look leases up by chaddr only (global or per subnet)
"host-reservation-identifiers": ["hw-address", "client-id", "duid", "circuit-id"]
```
Reservations can use `"client-id": "01:aa:bb:cc:dd:ee:ff"` or `"hw-address"`.
Windows DHCP: reservations are by MAC; the server matches client-id `01`+MAC as the MAC. Clients
with DUID-style IDs miss Windows reservations. (gated: unconfirmed, source is paywalled or blocked)

## Client fixes
- systemd-networkd: `ClientIdentifier=mac` in `[DHCPv4]`.
- NetworkManager: `ipv4.dhcp-client-id mac`.
- Templates: clear `/etc/machine-id` before cloning.

## Wireshark
`dhcp.option.type == 61` finds the option. For an Ethernet-type identifier Wireshark 4.4.1 decodes the
MAC into `dhcp.hw.mac_addr`, the same field as chaddr, so a packet shows two values (there is no
`dhcp.option.client_id` field).

## Verify
- [ ] The host gets the same reserved address in installer and OS, and the server shows a single lease for it.
