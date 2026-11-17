---
id: computing-software.systems-network-administration.pki-tls-administration.san-vs-cn-handling
name: san-vs-cn-handling
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [san-vs-cn-handling, pki-x509-profile, pki, subjectaltname, san, commonname, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Put identities in subjectAltName, support DNS, IP, email and URI types, handle wildcards and know why clients ignore CN."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subject alternative names versus CN
Goal: TLS certificates that validate in modern clients. Source for the encoding rules: RFC 5280 section 4.2.1.6.

## What RFC 5280 requires
- Whenever identities such as an email address, DNS name, IP address or URI are bound into a certificate, the subjectAltName (SAN) extension MUST be used. A DNS name may also appear in the subject field via domainComponent, but implementations need not convert those into DNS names.
- All parts of the SAN must be verified by the CA, and multiple names of each form are allowed.
- If the only subject identity is an alternative name form, the subject DN MUST be empty and the SAN MUST be present and marked critical. With a non-empty subject DN, CAs SHOULD mark the SAN non-critical.
- dNSName: IA5String in the "preferred name syntax"; case is not significant; a dNSName of a single space MUST NOT be used; email addresses must not be encoded as DNS names.
- iPAddress: exactly 4 octets for IPv4 and 16 for IPv6, network byte order.
- rfc822Name: a Mailbox of the form `Local-part@Domain`, no phrase or angle brackets.
- uniformResourceIdentifier: an absolute URI with scheme and scheme-specific part; if it has an authority, the host must be a fully qualified domain name or IP address.

## Practitioner advice (not from RFC 5280)
- Put every hostname clients will use in the SAN, including the one you would have put in the CN. Current browsers and most TLS libraries match the SAN and no longer fall back to the CN; test your own clients.
- Wildcard rules (single leftmost label) come from the TLS name-matching RFCs and CA/Browser Forum rules, not RFC 5280. Confirm your clients' behaviour before relying on wildcards.
- Public CAs follow CA/Browser Forum rules on which IP and internal names they may issue; use a private CA for private IPs and internal names.
- With OpenSSL, `openssl req ... -addext "subjectAltName=DNS:host"` adds a SAN to a request. `openssl x509 -req` does not copy request extensions unless you pass `-extfile` or `-copy_extensions`.

## Verify
- [ ] Inspect the certificate's SAN (`openssl x509 -noout -ext subjectAltName`) and confirm every name is present.
- [ ] A client using your private CA bundle connects without disabling verification.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 section 4.2.1.6 in full. The CA/Browser Forum baseline requirements source was only a documents index page (landing page) and was dropped. Removed as unsupported: Chrome 58 and Go 1.15 CN-fallback removal dates, the one-label wildcard rule as a stated fact, the SPIFFE URI example and the curl check. OpenSSL flags are practitioner advice and were not tested.
