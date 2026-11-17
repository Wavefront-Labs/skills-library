---
id: computing-software.systems-network-administration.dns-dhcp.dnssec-key-rollover-and-cds
name: dnssec-key-rollover-and-cds
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dnssec, bind, dnssec-policy, key-rollover, ksk-rollover, zsk-rollover, cds-cdnskey, ds-record, parental-agents, rndc-dnssec, checkds, csk]
level: advanced
status: verified
description: "Run DNSSEC key rollovers with BIND dnssec-policy: ZSK automatic rolls, KSK/CSK rolls gated on the parent DS, CDS/CDNSKEY and parental-agents, and rndc dnssec checks."
sources:
  - https://bind9.readthedocs.io/en/latest/dnssec-guide.html
  - https://datatracker.ietf.org/doc/html/rfc7583
  - https://datatracker.ietf.org/doc/html/rfc8078
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC key rollovers and CDS

## Policy with automatic rolls (BIND 9.16+; `checkds` needs 9.20)
```
dnssec-policy "standard" {
    keys {
        ksk lifetime P1Y algorithm ecdsap256sha256;
        zsk lifetime P90D algorithm ecdsap256sha256;
    };
    dnskey-ttl PT1H;
    publish-safety PT1H;
    retire-safety PT1H;
    signatures-validity P14D;
    signatures-refresh P5D;
    parent-ds-ttl P1D;           // match the TLD's DS TTL
    parent-propagation-delay PT1H;
};
zone "example.org" {
    type primary; file "example.org.db";
    dnssec-policy "standard";
    inline-signing yes;
    parental-agents { 192.0.2.1; };    // optional: servers that DS queries are sent to
    checkds explicit;                   // 9.20 ARM only: the `checkds` zone statement is absent from the 9.18 ARM
};
```
- Defaults per the ARM: `signatures-validity P2W`, `signatures-refresh P5D`, `dnskey-ttl` 1 hour, `publish-safety` and
  `retire-safety` PT1H, `parent-ds-ttl P1D`, `parent-propagation-delay PT1H`. The built-in `default` policy is a single
  never-rolling CSK (ECDSAP256SHA256) and may change between releases, so define your own policy as above.
- **ZSK** rolls are fully automatic (pre-publication method): new key published, then used, old
  retired after TTLs.
- **KSK/CSK** rolls need the parent to publish the new **DS**. BIND publishes **CDS/CDNSKEY**
  records for the incoming key; a parent that scans CDS/CDNSKEY (RFC 7344, with RFC 8078 for the initial
  bootstrap) can pick it up automatically, but support varies by registry and registrar, so check yours. Otherwise
  submit the DS manually at the registrar.
- BIND waits until it sees the DS at the parent (via `parental-agents`; `checkds yes` queries the parent zone's NS
  records, `explicit` (the default when parental-agents exist) only the listed agents, `no` sends no queries and needs
  the command below; responses are validated so `dnssec-validation` must be on) or you tell it:
  ```
  rndc dnssec -checkds -key <keyid> published example.org
  rndc dnssec -checkds -key <oldkeyid> withdrawn example.org
  ```

## Watch progress
```
rndc dnssec -status example.org        # keys, states, next rollover times
dig +short DS example.org @<parent-ns>
dig +short CDS example.org @ns1.example.org
dig +dnssec DNSKEY example.org
```

## Manual rollover now (compromise or algorithm policy change)
`rndc dnssec -rollover -key <keyid> example.org` schedules an immediate roll per the policy timings.

## Gotchas
- Removing the old DS before the new KSK is in use, or removing the old DNSKEY while the parent
  still only has its DS = **validation failure for the whole zone** (SERVFAIL for validating users).
  Let the policy timings run; never delete key files by hand.
- Long DS TTLs at the parent stretch KSK rolls; plan for them.
- Keep key files (in the `key-directory`) backed up; losing the private KSK forces an emergency roll.

## Verify
- [ ] DNSViz shows a valid chain before, during and after the roll.
- [ ] `rndc dnssec -status` shows the expected next roll dates.
