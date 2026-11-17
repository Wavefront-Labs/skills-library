---
id: computing-software.cloud-infrastructure-engineering.cert-manager.faq-renewal-and-secrets
name: faq-renewal-and-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [faq, reissuance, backoff, ca-crt, tls-crt, keystore-password, certificate-failure]
level: practitioner
status: docs-checked
description: "Answer common cert-manager questions: what triggers reissuance, failure backoff flags, why tls.crt omits the root, ca.crt semantics and keystore passwords."
sources:
  - https://cert-manager.io/docs/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reissuance happens when: the Secret is missing, corrupt or lacks cert data; its key does not match the `privateKey` spec or the certificate; the Secret's issuer annotations differ from the Certificate's; names (DNS, IPs, URIs, emails) differ from the spec; the certificate has expired or reached renewal time; or `cmctl renew` was run. With a latest CertificateRequest, cert-manager also compares CSR common name, subject, duration, `isCA`, names and usages. A `spec.duration` change only triggers reissuance if a CertificateRequest exists to compare; after a restore use `cmctl renew`.

Failures: a terminal failure leaves the `Issuing` condition false and sets `status.lastFailureTime`, then retries with exponential backoff, 1 to 32 hours by default. Bounds: `--certificate-request-minimum-backoff-duration` and `--certificate-request-maximum-backoff-duration` (Helm `certificateRequestMinimumBackoffDuration`, `certificateRequestMaximumBackoffDuration`). Terminal causes: issuer marks the request failed or invalid (for example a CA rate limit) or an approver denies it. Ephemeral failures (network) resync within 5 minutes and appear only in controller logs. Retry now with `cmctl renew`; deleting the latest CertificateRequest is usually harmless but risks duplicate issuance. Events are purged after a while.

Secret contents: roots are omitted from `tls.crt` by design. `ca.crt` is a best-effort guess (deepest issuer seen if the root is missing), can change when the issuer changes, and is updated with the certificate, so it cannot hold old and new CAs during rotation and is unsuitable as a trust source.

Defaults: duration 90 days; without `renewBefore`, renewal at 2/3 of the actual duration; ECDSA via `privateKey.algorithm: ECDSA`, `size: 256`.

JKS/PKCS#12 passwords are legacy compatibility, not security; use a constant like `changeit`.

## Checked

2026-11-03: Confirmed against the FAQ page: every reissuance trigger listed, the CertificateRequest comparisons, `spec.duration` caveat and `cmctl renew` after restore, terminal failure signals and the 1 to 32 hour backoff with its flags and Helm values, ephemeral resync up to 5 minutes, delete-latest-CertificateRequest advice, events being purged, root omitted from `tls.crt`, `ca.crt` best-effort semantics, 90 day default duration and renewal at 2/3, the ECDSA `size: 256` example, and the JKS/PKCS#12 password advice. Removed: the instruction to use trust-manager (the FAQ does not name it; it only says the CA must be trusted another way).

Method: documentation only; no commands were run.
