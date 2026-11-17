---
id: computing-software.systems-network-administration.pki-tls-administration.caa-wildcard-iodef-tree
name: caa-wildcard-iodef-tree
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [caa-wildcard-iodef-tree, pki-caa, caa, issuewild, iodef, subdomain-policy, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Control wildcard issuance with issuewild, report violations with iodef and override CAA per subdomain."
sources:
  - https://www.rfc-editor.org/rfc/rfc8659
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAA wildcard, iodef and tree climbing
Goal: fine-grained issuance policy across a zone. All rules are from RFC 8659.
- `issuewild` has the same syntax as `issue` but authorises wildcard names only. Each `issuewild` is ignored for non-wildcard names. If at least one `issuewild` exists in the Relevant RRset for a wildcard name, every `issue` is ignored for that wildcard name.
- Without `issuewild`, `issue` covers wildcards too.
- Tree climbing: the search climbs from the name towards the root (not including `.`) and uses the first non-empty CAA RRset. So records at `payments.example.com` replace, not merge with, those higher up for that name and below. For `*.X` the Relevant RRset is computed from `X`.
- Aliases: the CAA lookup per name follows CNAMEs per RFC 1034 (RFC 8659 dropped the old RFC 6844 tree-climbing on every CNAME and DNAME target, leaving alias handling to the CA's recursive resolver).
- Examples from the RFC: `issue "ca1.example.net"` plus `issuewild "ca2.example.org"` lets ca1 issue for the name and subdomains and only ca2 for wildcards. `issuewild "ca2.example.org"` together with `issue ";"` allows only ca2, and only for wildcards. `issuewild` alone leaves non-wildcard issuance open to any CA.
- `iodef` takes a URL: `mailto:` sends an IODEF report as a MIME attachment; `http` or `https` submits it as a web service request (RFC 6546). No other schemes are supported. Reports concern requests or issuance that violate the issuer's or the name holder's policy.
- Critical flag: Flags value 128 means a CA must not issue for a name whose RRset has a critical property with an unknown tag. Use it only for tags you need enforced.
```
example.com.          CAA 0 issue "ca1.example.net"
example.com.          CAA 0 issuewild ";"
```
- In that example ca1 may issue for `example.com` and subdomains, and no CA may issue for `*.example.com` (the placeholder CA names come from the RFC examples).
- Zone operators: use a DNS provider that answers unknown types correctly (NOERROR, not NOTIMP or dropped); see section 6 of the RFC for failure modes.
Verify:
- [ ] A CAA query for the override name returns only the override set.
- [ ] A wildcard issuance attempt is refused where `issuewild ";"` applies.

## Checked
Confirmed 2026-11-08 against RFC 8659 sections 3, 4.2 to 4.5, 6, 7. Removed: "support for iodef by CAs is patchy" (not stated), the claim that a subdomain CAA does not stop parent-level wildcard issuance (replaced by the lookup rule above), the DNS provider DNSSEC-signing advice (DNSSEC is only recommended, section 5.1), and the `dig` commands.
Method: docs-only read of cited pages, 2026-11-08
