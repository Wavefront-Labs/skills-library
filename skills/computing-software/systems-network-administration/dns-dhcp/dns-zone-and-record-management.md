---
id: computing-software.systems-network-administration.dns-dhcp.dns-zone-and-record-management
name: dns-zone-and-record-management
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-zone, zone-file, bind, named, named-checkzone, named-checkconf, rndc, rndc-freeze, origin, trailing-dot, axfr, ixfr, zone-transfer, notify, tsig, primary-secondary, windows-dns, ad-integrated-zone, dynamic-dns, secure-dynamic-updates, aging, scavenging, dnsserver-powershell, dnssec, dnssec-policy, ksk, zsk, ds-record, dns-as-code, octodns, dnscontrol, terraform, cname-apex, alias-record, ptr, reverse-zone]
level: advanced
status: docs-checked
description: "Run authoritative zones: BIND zone-file syntax traps, checkzone/rndc workflow, secured AXFR/IXFR with TSIG, AD-integrated zones and scavenging, BIND dnssec-policy, DNS-as-code."
sources:
  - https://bind9.readthedocs.io/en/latest/
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/
  - https://datatracker.ietf.org/doc/html/rfc1035
  - https://datatracker.ietf.org/doc/html/rfc2317
  - https://www.rfc-editor.org/rfc/rfc2181
  - https://www.rfc-editor.org/rfc/rfc2308
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNS zone and record management — change zones like code, replicate them securely

**Goal:** make record changes that are syntactically safe, replicate to every secondary,
stay clean over years (no stale dynamic records), and can be signed with DNSSEC. Record
semantics, TTL/serial basics, delegation and `dig` troubleshooting are in
`computing-software.systems-network-administration.dns-dhcp.dns-records-and-resolution-troubleshooting`.

## 1. BIND zone files: the traps
```
$ORIGIN corp.example.
$TTL 3600
@     IN SOA ns1.corp.example. hostmaster.corp.example. (
            2026101501 ; serial YYYYMMDDnn
            3600       ; refresh
            900        ; retry
            1209600    ; expire (14 days)
            300 )      ; negative-caching TTL
      IN NS  ns1.corp.example.
      IN NS  ns2.corp.example.
ns1   IN A   192.0.2.53
www   IN A   192.0.2.80
mail  IN A   192.0.2.25
@     IN MX  10 mail
api   IN CNAME www
```
- **Trailing dot.** `mail.corp.example` without a dot becomes
  `mail.corp.example.corp.example.`. Bare labels (`mail`) are relative to `$ORIGIN`.
- The SOA email has no `@`: `hostmaster.corp.example.` = `hostmaster@corp.example`.
- **CNAME rules:** a name with a CNAME may have no other records, so no CNAME at the zone
  apex (`@`) where SOA/NS live. Use provider ALIAS/ANAME/flattening or an A record.
  MX and NS targets must be names with A/AAAA, not CNAMEs.
- Forgetting to bump the serial means secondaries never pick up the change.

Workflow on every edit:
```bash
named-checkzone corp.example /var/named/corp.example.zone   # syntax + semantic check
named-checkconf -z                                          # whole config and all zones
rndc reload corp.example
dig @ns2.corp.example corp.example SOA +short               # secondary serial matches?
```
For zones that also take dynamic updates, never edit the file directly:
`rndc freeze corp.example` → edit → bump serial → `rndc thaw corp.example`, or use
`nsupdate`. 

## 2. Zone transfers done safely
```
key "xfr-key" { algorithm hmac-sha256; secret "<TSIG_SECRET>"; };
zone "corp.example" {
    type primary;
    file "corp.example.zone";
    allow-transfer { key "xfr-key"; };
    also-notify { 192.0.2.54; };
};
```
- Restrict AXFR to secondaries (TSIG preferred over IP lists). Open AXFR leaks your whole
  zone; test from outside with `dig @ns1.corp.example corp.example AXFR` (should fail).
- NOTIFY makes secondaries pull at once; refresh/retry/expire are the fallback. If a
  secondary cannot reach the primary for longer than **expire**, it stops answering for
  the zone.
- Generate TSIG keys with `tsig-keygen xfr-key`; store the secret outside the repo.

## 3. Windows AD-integrated zones
- Set dynamic updates to **Secure only**.
- **Aging and scavenging** removes stale dynamic records. Aging is not enabled by default
  (`Set-DnsServerZoneAging`); a record with a non-zero timestamp that is not refreshed within
  NoRefreshInterval plus RefreshInterval can be removed at the next scavenging. Before enabling on an old zone, list
  stale records and confirm devices that registered once and never refresh (some
  appliances) have static records instead.
```powershell
Add-DnsServerResourceRecordA -ZoneName corp.example -Name app01 -IPv4Address 192.0.2.81 -CreatePtr
Set-DnsServerZoneAging -Name corp.example -Aging $true -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00
Get-DnsServerResourceRecord -ZoneName corp.example -RRType A | Where Timestamp -lt (Get-Date).AddDays(-30)
```

## 4. Reverse zones
Create a reverse zone per allocated block (e.g. `2.0.192.in-addr.arpa` for 192.0.2.0/24)
and keep PTRs in step with A records. For delegated subnets smaller than /24 you need RFC 2317
classless delegation with your provider.

## 5. DNSSEC (dnssec-policy)
```
zone "corp.example" { type primary; file "corp.example.zone";
                      dnssec-policy default; inline-signing yes; };
```
BIND creates and rolls keys automatically; you publish the **DS** record at the parent
(registrar). The BIND reference says `dnssec-policy` needs dynamic DNS or `inline-signing`,
and that inline-signing is the default for DNSSEC zones; check your version's docs for
the policy defaults. Validate from a validating resolver with `dig +dnssec` and look for the
`ad` flag.

## 6. DNS as code
For public and cloud zones, manage records in Git with octoDNS, DNSControl or Terraform:
pull request → `plan`/`preview` diff → review → apply. This gives history, review and a
rebuild path if the provider account is lost. Import existing records first so the tool
does not delete what it does not know about.

## Verify
- [ ] `named-checkzone`/`named-checkconf -z` clean before every reload.
- [ ] All authoritative servers return the same SOA serial.
- [ ] AXFR refused from an unauthorised host.
- [ ] AD zones: secure-only updates; scavenging enabled with intervals understood.
- [ ] Every A record for a server has a matching PTR.
- [ ] DNSSEC zones validate (`ad` flag from a validating resolver); DS at parent matches the active KSK.

## Checked
2026-10-28. Confirmed against RFC 1035 (SOA fields, EXPIRE), RFC 2181 (a name with a CNAME has no other data; NS/MX targets must not be aliases), RFC 2308 (SOA MINIMUM as negative-caching TTL), RFC 2317 (classless in-addr.arpa delegation), the BIND 9 reference and DNSSEC guide (`tsig-keygen`, `rndc freeze`/`thaw` before editing a dynamic zone, `dnssec-policy` with `inline-signing`, `ad` flag), and the Set-DnsServerZoneAging and Add-DnsServerResourceRecordA references (aging off by default, interval parameters, `-CreatePtr`). Removed as unconfirmed: the 7+7 day aging defaults, AD zone replication scope, DnsUpdateProxy advice, journal-loss claim, BIND version gates, `rndc dnssec -status`, `delv` and the failure-mode list.
Method: documentation only; no commands were run.
