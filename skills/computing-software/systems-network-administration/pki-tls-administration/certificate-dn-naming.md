---
id: computing-software.systems-network-administration.pki-tls-administration.certificate-dn-naming
name: certificate-dn-naming
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [certificate-dn-naming, pki-policy-docs, pki, distinguished-name, subject-dn, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Design CA and leaf subject names: DN components, CN usage, uniqueness, name encoding and why identity belongs in the SAN."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate subject and DN naming
Goal: unique, stable names that do not break path building. Source: RFC 5280 sections 4.1.2.4, 4.1.2.6, 4.2.1.6 and 7.1.

## What RFC 5280 says
- Name chaining matches the issuer DN in one certificate with the subject DN in the CA certificate. The comparison follows section 7.1: conforming implementations use the LDAP StringPrep profile (RFC 4518) and caseIgnoreMatch for attributes in PrintableString or UTF8String. It is not a plain byte comparison.
- CAs MUST use PrintableString or UTF8String for DirectoryString attributes, except where they previously issued certificates using Teletex, BMP or Universal strings and may continue for backward compatibility. Implementations MUST support UTF8String and PrintableString.
- A non-empty subject DN MUST be unique for each subject entity certified by one CA, though a CA may issue several certificates with the same DN to the same entity.
- If the only identity is an alternative name form, the subject DN is empty and the subjectAltName is critical; identities such as DNS names, IP addresses, email addresses and URIs belong in the subjectAltName.
- Serial numbers are positive, unique per issuer and at most 20 octets (see x509-base-fields).

## Practitioner advice (not from RFC 5280)
- Because path building relies on issuer and subject DNs matching, keep a CA's DN the same across renewals, and keep the encoding consistent; changing the DN makes the renewed CA a different issuer for certificates issued under the old name.
- Example CA subject: `C=US, O=Example Corp, CN=Example Issuing CA G2`. Do not reuse a CN across different keys unless it is an intended renewal.
- Put the host identity of a TLS leaf in the SAN; treat the CN as legacy (see san-vs-cn-handling). Public CA subject field limits come from the CA/Browser Forum rules; check them if you operate a public CA.
- Plan non-ASCII names and internationalised domain names before issuing.

## Verify
- [ ] The CA subject and issuer, rendered the same way, are identical across renewals.
- [ ] No two live CAs share a subject DN with different keys.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 sections 4.1.2.4 (encodings, name chaining) and 7.1 (comparison rules) and 4.2.1.6. The CA/Browser Forum source was only a documents index page and was dropped. Corrected: the original "matched byte-wise" claim contradicts section 7.1. Removed as unsupported: the 64-bit CSPRNG serial claim, "BRs forbid unvalidated Subject fields", "no longer need CN" and the openssl nameopt command.
