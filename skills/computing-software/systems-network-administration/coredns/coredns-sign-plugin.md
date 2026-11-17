---
id: computing-software.systems-network-administration.coredns.coredns-sign-plugin
name: coredns-sign-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, sign, dnssec, zone-signing, csk]
level: sme
status: docs-checked
description: "Sign zone files with a common signing key, understand re-sign timing, the signed output location and the lack of rollover support."
sources:
  - https://coredns.io/plugins/sign/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce a signed zone for file or auto to serve.

sign adds DNSSEC records to a zone file; file and auto then serve the signed result. Only NSEC is supported. At least one Common Signing Key is required; there is no ZSK/KSK split and no key or algorithm rollover.

```
sign DBFILE [ZONES...] {
    key file|directory KEY...|DIR...
    directory DIR
}
```

- `key file` uses key file names as given; `key directory` looks in DIR for `K<name>+<alg>+<id>` files, ignores their metadata (Activate, Publish) and requires KSK keys.
- `directory` is where signed zones are written as `db.<name>.signed`; default `/var/lib/coredns`. A relative path is prefixed with root.

Signing rules:
- Re-sign when the last signing was more than 6 days ago (with jitter) or when signatures have only 14 days left. Both are checked on the SOA signatures.
- RRSIGs have inception of minus 3 hours (minus jitter 0 to 18 hours) and expiration of plus 32 days (plus jitter 0 to 5 days).
- NSEC is added for all names; the TTL is the SOA negative-cache TTL.
- Apex CDS/CDNSKEY are replaced with ones derived from the keys (SHA1 and SHA256 CDS).
- The SOA serial is overwritten with the Unix epoch of signing.

The page's Bugs section says the `keys directory` form is not implemented. Keys are not to be included in the zone; sign adds them. Create keys with coredns-keygen or dnssec-keygen.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/sign/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing; added the page's Bugs note on key directory.

Method: documentation only; no commands were run.
