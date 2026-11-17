---
id: computing-software.systems-network-administration.dns-dhcp.rrsig-expiry-monitoring
name: rrsig-expiry-monitoring
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, rrsig-expiry, monitoring, nagios, prometheus]
level: practitioner
status: verified
description: "Monitor DNSSEC signature expiry and key state: RRSIG inception/expiration checks per authoritative server, alert thresholds and common causes."
sources:
  - https://www.rfc-editor.org/rfc/rfc4034#section-3.1.5
  - https://github.com/nlnetlabs/ldns
  - https://bind9.readthedocs.io/en/latest/dnssec-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RRSIG expiry monitoring

Expired signatures are the most common DNSSEC outage: the zone becomes bogus and validating
resolvers (Google, Cloudflare, Quad9, most ISPs) return SERVFAIL.

## What to check, per authoritative server
```
dig +dnssec +norecurse @ns1.example.com example.com SOA | grep RRSIG
example.com. 3600 IN RRSIG SOA 13 2 3600 20261101000000 20261018000000 12345 example.com. ...
                                         ^expiration     ^inception
```
Check SOA, DNSKEY (signed by KSK, often a different schedule) and a sample of other RRsets.

## Script
```
exp=$(dig +dnssec +norecurse @ns1.example.com example.com DNSKEY | awk '$4=="RRSIG"{print $9}' | sort | head -1)
days=$(( ( $(date -ud "${exp:0:8} ${exp:8:2}:${exp:10:2}" +%s) - $(date +%s) ) / 86400 ))
[ $days -lt 7 ] && echo "CRITICAL DNSKEY RRSIG expires in $days days"
```
Tools: `ldns-verify-zone -e P7D` (the period is ISO 8601, `-e 7d` is rejected; "signatures may not expire within
this period"), `check_dnssec_expiry` (Icinga/Nagios plugin, github.com/mrimann/check_dnssec_expiry),
`prometheus-dnssec-exporter` (chrj and systemli forks on GitHub), and BIND's `dnssec-verify` on the signed zone file.
The awk/date script above was run on sample dig lines (GNU date 8.32 in Git Bash): it picked the earliest
expiration and printed 10 days; the RRSIG layout (expiration, then inception, then key tag) matches what dnspython
`dns.dnssec.sign` produced for a 14-day lifetime (`20261104205345 20261021205345 35155`).

## Alert thresholds
Warn when remaining validity drops below half the normal re-sign interval, critical below 3 days.
For BIND dnssec-policy defaults (signatures 14 days, refresh 5 days before expiry) remaining
validity should never drop below about 5 days.

## Typical causes
- Manual signing cron stopped; HSM unreachable; signer stopped after disk full.
- Secondary not transferring (stale signed copy on one NS only: check every NS).
- Wrong clock on the signer (inception in the future).

## Verify
- [ ] Alerts fire in a test (lower threshold temporarily) and every authoritative server is checked, not just the primary.
