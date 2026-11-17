---
id: computing-software.cryptography-implementation.protocol-implementation.certificate-transparency-sct-and-monitoring
name: certificate-transparency-sct-and-monitoring
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-validation, certificate-transparency, sct, rfc6962, ct-monitoring, ct-policy, mis-issuance]
level: advanced
status: docs-checked
description: "Use Certificate Transparency (RFC 6962): how SCTs reach clients, monitoring public logs for your domains, privacy effects of logging, and client-side enforcement."
sources: ["https://datatracker.ietf.org/doc/html/rfc6962"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate Transparency: SCTs and monitoring

Certificate Transparency (RFC 6962, an Experimental-category RFC) uses publicly auditable, append-only,
untrusted logs of certificates. Anyone can submit certificates to a log, and anyone can monitor the logs for newly
added certificates. Those concerned about mis-issuance can watch the logs, which turns CA mis-issuance into
something you can detect. A log returns a Signed Certificate Timestamp (SCT) as a promise to include the entry.

## How SCTs reach the client
1. **Embedded in the certificate** as an X.509v3 extension (OID 1.3.6.1.4.1.11129.2.4.2): the CA submits a
   precertificate to the logs and embeds the returned SCTs in the final certificate.
2. **TLS extension** `signed_certificate_timestamp` in the handshake.
3. **Online Certificate Status Protocol** (OCSP) response carrying the SCTs (stapled or fetched).

Which SCTs a client demands (how many, from which logs) is client policy, not defined by RFC 6962. Read the policy of
each browser or platform you target.

## Monitor your domains (the main value for operators)
- Use a CT search or monitoring service, or tail the logs yourself, to list every logged certificate for your names.
- Alert on certificates for your names issued by unexpected CAs or for unexpected names, and route alerts to
  security on-call.
- Use the logs as inventory: forgotten hosts and shadow-IT certificates show up there.

## Privacy considerations
Names in a logged certificate are public. Do not put internal hostnames on publicly trusted certificates; use a
private CA whose certificates are not logged.

## Enforcing CT in your own clients
Non-browser clients rarely check SCTs. If you add checking, verify the SCT signature against the log's public key
and keep your list of trusted logs current; a stale list can cause outages, so weigh this against pinning
alternatives.

## Verify
- [ ] CT monitoring alerts exist for all registered domains.
- [ ] No internal hostnames are exposed via public certificates.

## Checked
2026-11-01. Confirmed against RFC 6962: abstract and sections 1 to 3 (append-only logs, monitoring, SCT delivery by
certificate extension OID 1.3.6.1.4.1.11129.2.4.2, TLS extension signed_certificate_timestamp and OCSP, precertificates).
Removed: browser enforcement claims and SCT counts, Chrome and Apple policy pages, crt.sh and named monitoring
services, library names, CAA cross-check and the openssl command (none are in RFC 6962).
Method: documentation only; no commands were run.
