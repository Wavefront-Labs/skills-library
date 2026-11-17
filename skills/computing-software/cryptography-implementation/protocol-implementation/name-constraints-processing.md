---
id: computing-software.cryptography-implementation.protocol-implementation.name-constraints-processing
name: name-constraints-processing
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, name-constraints-validation, name-constraints, x509, path-validation, rfc-5280]
level: advanced
status: docs-checked
description: "Process X.509 name constraints during path validation: permitted and excluded subtrees for DNS, IP, email, URI and DN, and testing validator behaviour."
sources: ["https://www.rfc-editor.org/rfc/rfc5280"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name constraints processing

## Semantics (RFC 5280 4.2.1.10)
- `permittedSubtrees`: if a certificate has a name of a constrained type, it must fall within at least one
  permitted subtree of that type. If no name of the type is present, the certificate is acceptable.
- `excludedSubtrees`: a name matching any excluded subtree is invalid regardless of permitted subtrees.
- Constraints accumulate down the path and are not applied to self-issued certificates unless the certificate
  is the last in the path.
- Conforming CAs must mark the extension critical, must not issue an empty sequence, and the `minimum` field
  must be zero with `maximum` absent.
- DNS: the constraint `host.example.com` is satisfied by that name plus any name with labels added on the left
  (`www.host.example.com`), not by `host1.example.com`.
- Email: a full address constrains one mailbox, a host name constrains all addresses at that host, a leading dot
  (`.example.com`) constrains all addresses in the domain but not the host itself.
- URI: the constraint applies to the host part and must be a fully qualified domain name; `.example.com` is satisfied
  by `host.example.com` but not `example.com`. A URI whose host is an IP address or absent must be rejected when a
  URI constraint exists.
- IP: an IPv4 constraint is 8 octets (address then mask, CIDR style), IPv6 is 32 octets; for example
  192.0.2.0/24 is `C0 00 02 00 FF FF FF 00`.
- directoryName constraints apply to the subject (when non-empty) and to directoryName SANs, compared as DN
  attributes; state them with the same encoding as the subject. An rfc822Name constraint with no SAN is applied
  to the subject `emailAddress` attribute.

## Pitfalls
- A validator that cannot process a constrained name form in a critical extension must reject the certificate.
- Constrain every name type you care about: a DNS constraint does not limit IP SANs, and the RFC treats each
  name form separately. Add an IP constraint if no IPs should be allowed.
- Applications must handle directoryName constraints and should handle rfc822Name, URI, dNSName and iPAddress.

## Testing
- Generate a constrained intermediate and leaves that violate it for each name form; validation must fail.
- Run a public name-constraint test suite against your validator and record any gaps.

## Verify
- [ ] Each name form (DNS, IP, email, URI, DN) has an accepting and a rejecting test.

## Checked
Date: 2026-10-31. Confirmed in RFC 5280 section 4.2.1.10: subtree semantics, critical requirement, minimum and
maximum rules, self-issued exemption, DNS, email, URI, directoryName and iPAddress matching and the C0 00 02 00
example. Removed: CN-fallback and "modern libraries" claims, the CA/B Forum non-critical and old macOS claims, and
the BetterTLS "thousands of cases" and Netflix claims (the cited page returned 404 and was not confirmed).
Method: documentation only; no commands were run.
