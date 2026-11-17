---
id: computing-software.cryptography-implementation.protocol-implementation.serving-complete-certificate-chains
name: serving-complete-certificate-chains
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-configuration, certificate-chain-order, fullchain, intermediate-certificate, aia-fetching, unable-to-get-local-issuer, cross-signed]
level: practitioner
status: docs-checked
description: "Serve the right TLS chain: leaf first, each certificate certifying the previous, root optional, and diagnose chain problems with openssl s_client -showcerts."
sources: ["https://datatracker.ietf.org/doc/html/rfc8446#section-4.4.2", "https://letsencrypt.org/certificates/", "https://docs.openssl.org/3.0/man1/openssl-s_client/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving complete certificate chains

A server that sends only its leaf certificate can pass in clients that
already know the intermediate, and fail in clients that do not. Send the
chain the client needs to build a path to a trust anchor it already holds.

## What to send (RFC 8446 4.4.2)

- The sender's certificate MUST be the first CertificateEntry.
- Each following certificate SHOULD directly certify the one immediately
  preceding it.
- A certificate that specifies a trust anchor MAY be omitted from the chain,
  provided supported peers are known to possess it. So the root is normally
  left out.
- Prior to TLS 1.3 each certificate was required to certify the preceding
  one. Receivers SHOULD tolerate extraneous certificates and arbitrary
  ordering (except the end-entity first), but do not rely on that: send the
  correct order.
- The server's certificate_list MUST be non-empty.

## Diagnose with openssl s_client

- `-showcerts` shows all certificates the server sent; the OpenSSL manual
  suggests it when verifying a server certificate has problems.
- By default verification errors are displayed but the connection proceeds;
  add `-verify_return_error` to make the command fail on them.
- `-servername` sets SNI; otherwise SNI is populated from the `-connect` name
  if it is a DNS name.
- Check that each certificate's issuer is the next certificate's subject.

## Alternate chains and cross-signs

Let's Encrypt's Chains of Trust page lists its roots and intermediates,
including roots cross-signed by other roots (the ISRG Root X1 cross-signed by
DST Root CA X3 is marked retired), and states that subscriber certificates are
issued from RSA or ECDSA intermediates according to the subscriber key type.
Pick the chain your issuer documents for your client population.

## Verify

- [ ] `s_client -showcerts` shows the leaf first and each following certificate issuing the previous.
- [ ] Clients with only the root in their trust store connect without custom settings.

## Checked

Method: docs-checked 2026-11-09 against RFC 8446 section 4.4.2, OpenSSL 3.0 s_client manual, Let's Encrypt Chains of Trust page. Removed: the per-server configuration table (nginx, Apache, HAProxy, Java, IIS, Kubernetes), certbot file names, the browser AIA and cache explanation, per-client error strings, the grep and curl diagnostic pipeline, the "do not include both alternate intermediates" advice, the Let's Encrypt cross-sign ending and old Android claims, and SSL Labs and testssl.sh checks.
