---
id: computing-software.cryptography-implementation.protocol-implementation.spiffe-ids-and-svid-rotation
name: spiffe-ids-and-svid-rotation
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, mutual-tls, mtls, spiffe, spire, x509-svid, workload-identity]
level: practitioner
status: docs-checked
description: "SPIFFE workload identity: SPIFFE ID rules, X509-SVID certificate and validation requirements, Workload API streaming of SVIDs and bundles for rotation."
sources: ["https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md", "https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md", "https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Workload_API.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPIFFE IDs and SVID rotation

## SPIFFE ID (SPIFFE-ID spec)

`spiffe://<trust-domain>/<path>`, an RFC 3986 URI.
- Scheme MUST be `spiffe`; the trust domain name MUST be non-empty; no query
  or fragment.
- Trust domain host: lowercase, no percent-encoding. Trust domain names are
  self-registered with no central authority, so uniqueness is not guaranteed;
  colliding domains keep operating independently but cannot federate.
- Path identifies the workload; its meaning is up to the administrator. Path
  rules: no percent-encoding, no empty or `.` / `..` segments, no trailing
  `/`, segments only `[a-zA-Z0-9.-_]`. The path is case-sensitive; scheme and
  trust domain are case-insensitive.
- Implementations MUST support IDs up to 2048 bytes and SHOULD NOT generate
  longer ones.

## X509-SVID (spec)

- Exactly one URI SAN, which is the SPIFFE ID. More than one URI SAN: the
  validator MUST reject. Other SAN types (such as DNS) are allowed.
- Leaf: `cA` false; key usage extension set and critical, `digitalSignature`
  MUST be set (`keyEncipherment` and `keyAgreement` MAY); `keyCertSign` and
  `cRLSign` MUST NOT be set. EKU SHOULD be present, and then
  `id-kp-serverAuth` and `id-kp-clientAuth` MUST both be set. Leaf SPIFFE IDs
  MUST have a non-root path.
- Signing certificates: `cA` true, `keyCertSign`; they MUST NOT be used for
  authentication.
- Leaf validation for authentication: RFC 5280 path validation to the CA
  bundle, then check `cA` is false, `keyCertSign` and `cRLSign` unset, scheme
  is `spiffe`, path is non-root, and a single URI SAN.
- Bundles represent each CA certificate as an RFC 7517 JWK with `use` set to
  `x509-svid`, carried in `x5c`.

## Workload API (rotation)

- `FetchX509SVID` and `FetchX509Bundles` are gRPC server-side streams, used so
  updates such as revocations and CA introductions propagate quickly.
- Every stream message carries the full set of information, not a delta. The
  client SHOULD treat absence as redaction: unload a bundle no longer sent and
  cease using redacted SVIDs.
- The first response is sent as soon as possible after the request. Updates
  follow events such as SVID rotation or CRL updates.
- `PermissionDenied` means the client is not entitled to SVIDs or bundles; it
  MAY reconnect after a backoff.
- Fetched bundles MUST only be used to authenticate X509-SVIDs. The private
  key in the response is unencrypted DER PKCS#8. If chain certificates are
  returned, the leaf comes first.
- A process that reads certificate files once at startup will miss updates;
  consume the stream.

## Verify

- [ ] A peer with a different SPIFFE ID, or a certificate with two URI SANs, is rejected.
- [ ] A soak test longer than the SVID lifetime keeps serving without restarts.

## Checked

Method: docs-checked 2026-11-09 against SPIFFE-ID.md, X509-SVID.md and SPIFFE_Workload_API.md (raw files). Removed: sources spire-concepts and go-spiffe (not read), the Kubernetes naming convention and prod/non-prod domain advice, SPIRE attestation, socket path and SVID TTL defaults, Go code and `tlsconfig` helpers, spiffe-helper, JWT-SVID bearer-token advice, federation bundle endpoint profiles, and the verify items about spire-server.
