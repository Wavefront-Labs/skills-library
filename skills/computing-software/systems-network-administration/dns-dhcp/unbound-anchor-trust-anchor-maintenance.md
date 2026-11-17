---
id: computing-software.systems-network-administration.dns-dhcp.unbound-anchor-trust-anchor-maintenance
name: unbound-anchor-trust-anchor-maintenance
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, unbound-anchor, trust-anchor, rfc5011, dnssec, root-ksk]
level: practitioner
status: docs-checked
description: "Maintain the DNSSEC root trust anchor with unbound-anchor and RFC 5011 auto-trust-anchor-file, handle KSK rollovers and fix stale anchors in images."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-anchor.html
  - https://www.rfc-editor.org/rfc/rfc5011
  - https://www.iana.org/dnssec/files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-anchor trust anchor maintenance

A validating resolver needs the root KSK as a trust anchor. IANA lists KSK-2024 (key tag 38696) as signing the root zone since 2026-10-11 and KSK-2017 (key tag 20326) as signing between 2018-10-11 and 2026-10-11; KSK-2017 is scheduled to be revoked on 2027-01-11 and removed on 2027-03-22. Resolvers must have updated trust anchors to keep validating, so stale anchors cause total SERVFAIL.

## Initial anchor
```
unbound-anchor -a /var/lib/unbound/root.key       # RFC 5011 tracking first; falls back to the RFC 7958 method when that fails
echo $?                                           # 1 = updated via the certificate or builtin anchor; 0 = no update needed, RFC 5011 sufficed, or an error occurred
```
The man page suggests running it before starting Unbound, for example from a startup script, and checking the exit value (`unbound-anchor -a root.key || logger "Please check root.key"`).

## Automatic updates (RFC 5011)
```
server:
    auto-trust-anchor-file: "/var/lib/unbound/root.key"
```
Unbound runs RFC 5011 probes several times per month, so the machine must be online frequently. New keys are added after the hold-down (`add-holddown`, default 2592000 seconds = 30 days). The Unbound user needs write permission on the file and its directory (and the file must be inside the chroot, if used).

## Pitfalls
- Golden VM/container images with an old root.key and no network at first boot: the resolver starts
  with an outdated anchor. Run `unbound-anchor` at boot.
- Systems offline for long periods can miss RFC 5011 updates; re-bootstrap with `unbound-anchor`.
- `trust-anchor-file` is a static file; only `auto-trust-anchor-file` is tracked with RFC 5011.

## Check
```
cat /var/lib/unbound/root.key                              # key tags and RFC 5011 state comments
unbound-control get_option auto-trust-anchor-file
dig @127.0.0.1 . DNSKEY +dnssec                            # flags 257 are the KSKs
```
BIND uses `dnssec-validation auto` with a built-in anchor and RFC 5011 management; a BIND release recent enough to contain the current root key is required for a fresh install.

## Verify
- [ ] root.key lists the current KSK(s) as VALID and `dig @127.0.0.1 example.com +dnssec` shows the ad flag.

## Checked

Date: 2026-10-26. NLnetLabs/unbound doc sources (unbound.conf.rst, unbound-control.rst, unbound-anchor.rst, repository pushed 2026-10-21), read on 2026-10-26. IANA root zone KSK page (iana.org/dnssec/files) read 2026-10-26. Confirmed: KSK-2024 tag 38696 signing since 2026-10-11, KSK-2017 tag 20326 signing 2018-10-11 to 2026-10-11, scheduled revocation 2027-01-11 and removal 2027-03-22; unbound-anchor description (RFC 7958 fallback), exit codes, auto-trust-anchor-file probes and write-permission requirement, add-holddown default 30 days, trust-anchor-file being static. The skill previously said the next root roll was planned for 2026-2027; corrected to the current IANA dates. Removed unconfirmed distro ExecStartPre and algorithm grep claims.

Method: documentation only; no commands were run.
