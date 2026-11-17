---
id: computing-software.cybersecurity-defensive.pomerium.downstream-mtls-mkcert
name: downstream-mtls-mkcert
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [downstream-mtls, mkcert, client-certificate-import, ca-file, pkcs12]
level: practitioner
status: docs-checked
description: "Require client certificates for Pomerium routes using downstream_mtls with a CA file, shown with mkcert for local testing only."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/certificates-and-tls.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Downstream mTLS requires end users to present a trusted client certificate; without one browsers see a Pomerium error page. Each user or device has its own certificate; the docs note that standards such as PCI-DSS and HIPAA recommend or require mutual authentication for sensitive data transport.

The docs' proof of concept uses `mkcert`, which they say is for local testing only; production needs real certificate management.

1. `mkcert -install` creates a local root CA.
2. `mkcert '*.localhost.pomerium.io'` yields `_wildcard.localhost.pomerium.io.pem` and `_wildcard.localhost.pomerium.io-key.pem`.
3. Set `certificate_file` and `certificate_key_file` to them (skip if a server certificate already exists).
4. `mkcert -client -pkcs12 "yourUsername@localhost.pomerium.io"` produces a `.p12` file.
5. In `config.yaml` add `downstream_mtls` with `ca_file` pointing at mkcert's `rootCA.pem`.
6. Import the `.p12` into the browser (Chrome on Linux: `chrome://settings/certificates`, Import, default password `changeit`). Visiting a route such as `https://verify.localhost.pomerium.io` then prompts for a certificate.

Policy interaction: by default, a `deny` rule using the `invalid_client_certificate` criterion is added to all policies when downstream mTLS is configured (the Enforcement Mode setting can change this default). Match certificates in policy with ppl-certificate-matcher.

## Checked

2026-11-04. Confirmed against the Certificates and TLS and PPL pages: mkcert steps, client certificate, downstream_mtls ca_file, Chrome import, invalid_client_certificate default deny. Reworded the compliance and default-deny lines to match the pages.

Method: documentation only; no commands were run.
