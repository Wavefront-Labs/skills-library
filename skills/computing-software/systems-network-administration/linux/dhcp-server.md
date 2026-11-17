---
id: computing-software.systems-network-administration.linux.dhcp-server
name: dhcp-server
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dhcp-server, dhcpd, isc-dhcp, kea, kea-dhcp4, dnsmasq, dhcp-relay, reservations, host-reservation, lease-database, pxe-options, option-66, next-server, dhcpv6, ra, radvd, ddns, lpic-2, networking, sysadmin, subnet-declaration, dhcp-pool, dhcp-options]
level: practitioner
status: docs-checked
description: "Hand out addresses on Linux with ISC Kea (current), legacy dhcpd, or dnsmasq: subnets, pools, reservations, PXE/DNS/NTP options, lease inspection, relays, and IPv6 with radvd/Kea DHCPv6."
sources:
  - https://kea.readthedocs.io/en/latest/
  - https://github.com/isc-projects/dhcp/blob/master/README
  - https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
  - https://github.com/radvd-project/radvd
  - https://datatracker.ietf.org/doc/html/rfc2132
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DHCP server on Linux — Kea first, dhcpd for legacy, dnsmasq for small networks

**Goal:** serve leases with the right options (gateway, DNS, NTP, PXE), pin important
hosts with reservations, and see who has what.

## 1. Kea (ISC's replacement; ISC DHCP is end-of-life, 4.4.3 was its final planned release)
Install Kea with your distro's package manager.
`/etc/kea/kea-dhcp4.conf`:
```json
{ "Dhcp4": {
    "interfaces-config": { "interfaces": [ "eth1" ] },
    "lease-database": { "type": "memfile", "persist": true, "name": "/var/lib/kea/kea-leases4.csv" },
    "valid-lifetime": 86400, "renew-timer": 43200, "rebind-timer": 75600,
    "option-data": [
        { "name": "domain-name-servers", "data": "10.0.0.53, 10.0.0.54" },
        { "name": "domain-name", "data": "corp.example" },
        { "name": "domain-search", "data": "corp.example" },
        { "name": "ntp-servers", "data": "10.0.0.5" }
    ],
    "subnet4": [ {
        "id": 1,
        "subnet": "10.0.10.0/24",
        "pools": [ { "pool": "10.0.10.100 - 10.0.10.250" } ],
        "option-data": [ { "name": "routers", "data": "10.0.10.1" } ],
        "reservations": [
            { "hw-address": "52:54:00:aa:bb:cc", "ip-address": "10.0.10.20", "hostname": "printer1" }
        ],
        "next-server": "10.0.0.9",
        "boot-file-name": "pxelinux.0"
    } ],
    "client-classes": [ {
        "name": "uefi", "test": "option[93].hex == 0x0007",
        "boot-file-name": "grubx64.efi"
    } ],
    "loggers": [ { "name": "kea-dhcp4", "output_options": [ { "output": "syslog" } ], "severity": "INFO" } ]
} }
```
```bash
kea-dhcp4 -t /etc/kea/kea-dhcp4.conf      # syntax/semantic check
systemctl enable --now kea-dhcp4            # service name varies by distro
tail /var/lib/kea/kea-leases4.csv           # memfile lease database (CSV); default name kea-leases4.csv
# allow 67/udp (DHCP server port) through the firewall
# Kea 2.7.9+: memfile lease files load only from the build-time data directory (override with KEA_DHCP_DATA_DIR)
```
- Kea selects the subnet from the receiving interface, or from the relay's `giaddr` when the message is relayed; a subnet can also list `relay` `ip-addresses` to match relays in unusual setups. A client matching no subnet gets no lease.
- Host reservations are controlled by `reservations-global`, `reservations-in-subnet` and `reservations-out-of-pool` (a subnet reservation wins over a global one); read the host reservation section for your version's defaults.
- Reload: the control channel `config-reload` command re-reads the config file, or restart (leases persist with `persist: true`).
- DDNS to BIND: add `"dhcp-ddns": { "enable-updates": true }` and run `kea-dhcp-ddns` with a TSIG key.
- Kea DHCPv6 (`kea-dhcp6`) hands out addresses/DNS; router advertisements still come from
  `radvd` (`AdvManagedFlag on` to tell clients to use DHCPv6).

## 2. Legacy ISC dhcpd (end-of-life; for existing installs only)
`/etc/dhcp/dhcpd.conf`:
```
authoritative;
default-lease-time 43200; max-lease-time 86400;
option domain-name "corp.example";
option domain-name-servers 10.0.0.53, 10.0.0.54;
subnet 10.0.10.0 netmask 255.255.255.0 {
    range 10.0.10.100 10.0.10.250;
    option routers 10.0.10.1;
    option ntp-servers 10.0.0.5;
    next-server 10.0.0.9;
    filename "pxelinux.0";
}
host printer1 { hardware ethernet 52:54:00:aa:bb:cc; fixed-address 10.0.10.20; }
class "uefi" { match if substring(option vendor-class-identifier, 0, 20) = "PXEClient:Arch:00007"; filename "grubx64.efi"; }
```
```bash
dhcpd -t -cf /etc/dhcp/dhcpd.conf        # test the config (-t); service name and config path vary by distro
less <lease file>                        # the dhcpd.leases file (see -lf in dhcpd(8) for the location)
```
`authoritative;` matters: without it the server won't NAK clients holding addresses from
a previous server, so they keep stale leases.

## 3. dnsmasq (labs, small offices, PXE boxes — DHCP+DNS+TFTP in one)
```
# /etc/dnsmasq.d/lan.conf
interface=eth1
dhcp-range=10.0.10.100,10.0.10.250,255.255.255.0,12h
dhcp-option=option:router,10.0.10.1
dhcp-option=6,10.0.10.1
dhcp-host=52:54:00:aa:bb:cc,10.0.10.20,printer1
enable-tftp
tftp-root=/srv/tftp
dhcp-match=set:efi,option:client-arch,7
dhcp-boot=tag:efi,grubx64.efi
dhcp-boot=tag:!efi,pxelinux.0
```
`dnsmasq --test; systemctl enable --now dnsmasq; cat /var/lib/misc/dnsmasq.leases` (lease file location per the dnsmasq man page; `--dhcp-leasefile` overrides it).

## 4. Relays and troubleshooting
- Clients on other VLANs need a relay agent (the router/L3 switch's DHCP helper feature, or dnsmasq's `--dhcp-relay`; ISC's `dhcrelay` is part of the end-of-life ISC DHCP). The server then
  selects the subnet from `giaddr`.
- Watch the conversation: `tcpdump -ni eth1 -vv 'port 67 or port 68'` — DISCOVER without
  OFFER = wrong interface/subnet or firewall; OFFER without REQUEST = another server answered
  first (rogue DHCP; find it by the OFFER's source MAC).
- `journalctl -u kea-dhcp4 -f` / `-u dhcpd` (unit names vary by distro).
- Run only one DHCP server per broadcast domain unless they are set up as a failover pair (Kea's high-availability hook).
- NetworkManager on the server interface: give it a static IP; DHCP on the same NIC confuses everyone.

## Verify
- [ ] Config test passes; a test client (`nmcli con up`, `dhclient -v eth0`) gets an address, router and DNS from your pools.
- [ ] A reserved MAC always receives its fixed address; the lease file/db shows it.
- [ ] `tcpdump` shows exactly one OFFER per DISCOVER on the segment.

## Checked
Checked 2026-10-27 against the Kea Administrator Reference source (github.com/isc-projects/kea master), the ISC DHCP README and dhcpd man pages (github.com/isc-projects/dhcp), the dnsmasq man page and the radvd.conf man page.
- ISC DHCP README: the software is End-Of-Life and 4.4.3 is the final release planned; its client and relay components are end-of-life.
- Kea: `lease-database` memfile with `persist`, `valid-lifetime`/`renew-timer`/`rebind-timer`, option names `routers`, `domain-name-servers`, `domain-search`, `ntp-servers`, class `test` with `option[93].hex == 0x0007`, `next-server`/`boot-file-name`, `relay` `ip-addresses`, `kea-dhcp4 -t`, `config-reload`, `dhcp-ddns` `enable-updates`, `kea-leases4.csv` default name.
- dhcpd: `authoritative;` semantics, `-t -cf`, `fixed-address`.
- dnsmasq: `dhcp-match` with `option:client-arch`, `dhcp-boot` with `tag:` filters, `enable-tftp`, `tftp-root`, `--test`, `--dhcp-relay`, lease file path.
- radvd: `AdvManagedFlag` exists.
- Removed unconfirmed claims: distro packaging details, the `dhcp-lease-list` helper, vendor `ip helper-address`, libvirt use of dnsmasq, "last line wins" for the Kea CSV, a literal Kea log message, DHCPNAK-storm causes.
Method: documentation only; no commands were run.
