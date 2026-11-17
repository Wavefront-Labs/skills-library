---
id: computing-software.systems-network-administration.pki-tls-administration.name-constraints-extension
name: name-constraints-extension
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [name-constraints-extension, pki-constraints, pki, nameconstraints, permitted-subtrees, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Restrict a private subordinate CA to chosen DNS, email, IP and directory name spaces with the nameConstraints extension, per RFC 5280."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name constraints extension
Goal: let a CA sign only for `corp.example.com`, so its compromise cannot mint certificates for other domains.
RFC 5280 section 4.2.1.10:
- Only in CA certificates. Conforming CAs MUST mark it critical. Either `permittedSubtrees` or `excludedSubtrees` MUST be present (never an empty sequence).
- It restricts the subject distinguished name and the subject alternative names of every later certificate in the path. A restriction applies only when that name form is present; a certificate with no name of the constrained type is acceptable.
- Anything matching `excludedSubtrees` is invalid regardless of `permittedSubtrees`.
- Not applied to self-issued certificates unless it is the last certificate in the path.
- DNS: a constraint `host.example.com` is satisfied by that name plus any name made by adding labels to the left (`www.host.example.com` yes, `host1.example.com` no).
- Email: the full address constrains one mailbox; a host name (`example.com`) means any address at that host; a leading period (`.example.com`) means any address in the domain but not on the host itself.
- URIs: the constraint applies to the host part, which must be a fully qualified domain name. A leading period matches one or more additional labels (`.example.com` matches `my.host.example.com`, not `example.com`). A URI with no FQDN host (such as an IP address host) MUST be rejected if a URI constraint exists.
- IP addresses: an address plus mask, 8 octets for IPv4 and 32 octets for IPv6 (CIDR style). 192.0.2.0/24 is `C0 00 02 00 FF FF FF 00`.
- Directory names apply to the subject field and directoryName SANs and must be stated identically to the encoding in the certificate.
- Applications MUST process directoryName constraints and SHOULD process rfc822Name, URI, dNSName and iPAddress constraints. If a critical constraint covers a name form that appears in a later certificate, the application MUST either process the constraint or reject the certificate.
- CAs SHOULD NOT impose constraints on x400Address, ediPartyName or registeredID. `minimum` must be zero and `maximum` absent.
- If an rfc822Name constraint exists and the certificate has no SAN, the constraint is applied to the subject `emailAddress` attribute.
Verify:
- [ ] A certificate for a name outside the permitted space fails validation in the clients you rely on.
- [ ] An in-scope leaf validates in those same clients.

## Checked
Confirmed 2026-11-08 against RFC 5280 section 4.2.1.10 (semantics, matching rules, encodings). Removed: the openssl.cnf `nameConstraints` sample and its `excluded;IP` lines, the `openssl verify -x509_strict` check, the claim about older clients rejecting critical extensions, the claim that some clients apply constraints to CN, and the "no permitted subtree means any value allowed" gotcha (section 4.2.1.10 does not say this; section 7 was not read).
Method: docs-only read of cited pages, 2026-11-08
