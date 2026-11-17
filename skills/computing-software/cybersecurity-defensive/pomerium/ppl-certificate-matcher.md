---
id: computing-software.cybersecurity-defensive.pomerium.ppl-certificate-matcher
name: ppl-certificate-matcher
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [certificate-matcher, client-certificate, spki-hash, fingerprint, san-email]
level: advanced
status: docs-checked
description: "Match client certificates in a Pomerium policy by fingerprint, SAN or SPKI hash, and why SPKI hashes survive certificate renewal."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `client_certificate` criterion takes a certificate matcher. The docs mark the syntax beta and subject to change.

Keys: `fingerprint`, `san_dns`, `san_email`, `san_uri`, `spki_hash`.

- `fingerprint`: SHA-256 hash of the full certificate, in long form (colon-separated, uppercase) or short form (lowercase, no colons).
- `spki_hash`: base64-encoded SHA-256 hash of the Subject Public Key Info. It stays the same across renewals if the key pair is unchanged, so prefer it for allowlists of rotating certificates.
- SAN keys match the Subject Alternative Name entries.

The docs' examples pair each certificate rule with `authenticated_user: true`, covering: a SAN email ending in a domain, one fingerprint, and an allowlist of SPKI hashes. They also give OpenSSL commands to compute the fingerprint and SPKI hash.

Remember that configuring downstream mTLS adds a default deny rule for requests lacking a trusted client certificate (`invalid_client_certificate`); the Enforcement Mode setting changes that. Certificate criteria do not apply to SSH routes.

## Checked

2026-11-04. Read the Pomerium Policy Language page: certificate matcher keys, fingerprint long and short forms, SPKI hash and renewal note, the default invalid_client_certificate deny, and the SSH inapplicability list all confirmed. Nothing removed.

Method: documentation only; no commands were run.
