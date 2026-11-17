---
id: computing-software.cryptography-implementation.secure-implementation.certificate-chain-length-and-size-limits
name: certificate-chain-length-and-size-limits
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, chain-length-limit, certificate-validation, input-validation, dos, path-building]
level: advanced
status: docs-checked
description: "Bound certificate chain processing against untrusted input: maximum chain depth, certificate count and size, path-building work limits, and library settings."
sources: ["https://docs.openssl.org/3.0/man3/SSL_CTX_set_verify/", "https://pkg.go.dev/crypto/x509", "https://www.rfc-editor.org/rfc/rfc8446#section-4.4.2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate chain length and size limits

Chains arrive from untrusted peers (TLS, S/MIME, code signing). Unbounded processing invites DoS via huge chains,
deep paths or combinatorial path building.

## Limits to set
- **Depth**: OpenSSL `SSL_CTX_set_verify_depth(ctx, 5)` sets the maximum chain depth allowed;
  `SSL_set_verify_depth` does the same for one connection. Pick a depth just above your
  real chains (typically a handful of certificates).
- **Count and bytes in a message**: the TLS 1.3 `certificate_list` vector is `<0..2^24-1>` bytes (RFC 8446),
  far more than any real chain needs. Cap the received handshake size in your stack and check its default.
- **Per-certificate size**: reject certificates over a sane size you choose before parsing extensions.
- **Path-building work**: cap the number of candidate chains and signature checks your validator attempts;
  check your library's security advisories for chain-building and policy-processing denial-of-service fixes
  and keep libraries patched.
- **Custom constraint hooks**: Go's `CertPool.AddCertWithConstraint` (go1.22) lets you discard chains that
  fail your own check, for example a depth or size policy.

## Your own validators
- If you build chains manually (custom trust stores, AIA fetching), cap depth and total candidates, cache
  failures, and timeout AIA fetches (and restrict them to HTTP with size limits).
- Reject duplicates and loops in supplied intermediates.

## Verify
- [ ] Test with a 50-certificate chain and a 1 MiB certificate: rejected quickly with bounded CPU and memory.

## Checked

2026-10-31. Confirmed: OpenSSL 3.0 `SSL_CTX_set_verify` page (`SSL_CTX_set_verify_depth` and `SSL_set_verify_depth` set the maximum depth), RFC 8446 (`certificate_list<0..2^24-1>`), Go `crypto/x509`
(`AddCertWithConstraint`, added go1.22.0). Removed as unconfirmed: the OpenSSL default depth 100, the
`SSL_CTX_set_max_cert_list` default of 100 KiB, Go `maxChainSignatureChecks`, the CVE numbers and the Go name-comparison
cap, and the "2-4 certificates" figure.
Method: documentation only; no commands were run.
