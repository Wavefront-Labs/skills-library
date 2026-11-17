---
id: computing-software.systems-network-administration.linux.bind-reverse-zones-ptr
name: bind-reverse-zones-ptr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bind, bind9, named, reverse-zone, ptr-records, in-addr-arpa, ip6-arpa, rfc2317, classless-delegation, reverse-dns, dns-server, networking, sysadmin]
level: practitioner
status: verified
description: "Serve reverse DNS with BIND: in-addr.arpa and ip6.arpa zone naming, PTR records, RFC 2317 classless delegation for small blocks, matching forward records, and checks."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://datatracker.ietf.org/doc/html/rfc2317
  - https://datatracker.ietf.org/doc/html/rfc3596
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BIND reverse zones and PTR records

**Goal:** `dig -x` returns the right hostname for every server address (mail, SSH, Kerberos
and logs depend on it), and forward and reverse agree.

## 1. Zone naming
- IPv4 /24 `10.0.10.0/24` → zone `10.0.10.in-addr.arpa` (octets reversed, network part only).
- /16 `10.20.0.0/16` → `20.10.in-addr.arpa`; records then are `5.3` for 10.20.3.5.
- IPv6 `2001:db8:10::/48` → nibble-reversed: `0.1.0.0.8.b.d.0.1.0.0.2.ip6.arpa`.
  Generate with `ipv6calc` or `python3 -c "import ipaddress;print(ipaddress.ip_address('2001:db8:10::20').reverse_pointer)"`.

## 2. Zone and records
```
zone "10.0.10.in-addr.arpa" IN { type primary; file "10.0.10.rev"; allow-transfer { key xfer-key; }; };
```
```
$TTL 3600
@   IN SOA ns1.corp.example. hostmaster.corp.example. ( 2026101601 3600 900 1209600 300 )
    IN NS  ns1.corp.example.
    IN NS  ns2.corp.example.
20  IN PTR web01.corp.example.
25  IN PTR mail.corp.example.
53  IN PTR ns1.corp.example.
```
PTR targets **must end with a dot**; without it `web01.corp.example.10.0.10.in-addr.arpa.` is returned.
Keep one PTR per address unless you know every consumer copes with several.
`$GENERATE 100-250 $ IN PTR dhcp-$.corp.example.` fills pools.

## 3. Small public blocks (RFC 2317)
The ISP owns `113.0.203.in-addr.arpa`; you have 203.0.113.64/26. ISP delegates:
```
64/26   IN NS  ns1.corp.example.
$GENERATE 64-127 $ IN CNAME $.64/26.113.0.203.in-addr.arpa.
```
You serve zone `64/26.113.0.203.in-addr.arpa` with `65 IN PTR mail.corp.example.` etc.

## 4. Check and load
```bash
named-checkzone 10.0.10.in-addr.arpa /var/named/10.0.10.rev
rndc reload 10.0.10.in-addr.arpa
dig -x 10.0.10.25 @ns1 +short           # mail.corp.example.
dig +short mail.corp.example @ns1        # must return 10.0.10.25 (forward-confirmed reverse DNS)
```
Dynamic DHCP clients: let Kea/dhcpd update the reverse zone via TSIG (`allow-update { key ddns-key; };`)
and stop hand-editing that zone.

## Gotchas
- Forgetting to bump the SOA serial: secondaries keep stale PTRs.
- Recursive resolvers serving RFC1918 reverse zones locally (Unbound/BIND "empty zones") answer NXDOMAIN
  before asking you. In Unbound a `local-zone` of that name or the `nodefault` type turns a default off; in BIND use `disable-empty-zone` for individual zones (or `empty-zones-enable no`).
- Some mail servers check that the PTR name resolves back to the same IP (forward-confirmed reverse DNS), so keep forward and reverse in step.

## Verify
- [ ] `named-checkzone` OK; `dig -x <ip>` returns the hostname from every resolver clients use.
- [ ] For each PTR, the forward lookup returns the same IP.

## Checked
Checked 2026-10-27 against the BIND 9 Administrator Reference source (github.com/isc-projects/bind9 main), the Unbound unbound.conf source (github.com/NLnetLabs/unbound) and RFC 2317.
- `$GENERATE range owner [ttl] [class] type rdata` syntax matches the PTR and CNAME examples (BIND zones page).
- RFC 2317 classless delegation: parent holds `NS` for the `64/26` label and CNAMEs to `<n>.64/26.<parent zone>`, child zone is named `64/26.<parent zone>`, matching the example.
- BIND empty zones are enabled by default; `empty-zones-enable` and `disable-empty-zone` exist; Unbound default local zones are switched off by a same-name `local-zone` or the `nodefault` type.
- IPv6 nibble form of 2001:db8:10::/48 and the stdlib `reverse_pointer` call were checked by hand.
- Removed unconfirmed claims: cloud provider PTR handling, mail-server rejection behaviour, multiple-PTR breakage. The dead `chapter3.html` source was replaced.
Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (BIND 9.20.30 named run on 127.0.0.1:5353, Fedora 44 python3): named-checkzone on the reverse zone and the RFC 2317 zone named 64/26.113.0.203.in-addr.arpa, $GENERATE pool PTRs, a PTR without trailing dot returning nodot.corp.example.10.0.10.in-addr.arpa., dig -x and forward lookup agreeing, ipaddress.reverse_pointer ending in the documented /48 nibble form. Not run: rndc reload, TSIG-keyed transfers and dynamic updates, empty-zone and Unbound behaviour (documentation only).
