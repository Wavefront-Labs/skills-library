---
id: computing-software.cryptography-implementation.protocol-implementation.revoking-and-denylisting-client-certificates
name: revoking-and-denylisting-client-certificates
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, client-cert-revocation, mutual-tls, crl, ocsp, denylist, mtls]
level: advanced
status: docs-checked
description: "Revoke client certificates in mTLS: CRLs and OCSP at nginx and Envoy, chain-wide CRL coverage, nextUpdate handling, and application deny lists."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/transport_sockets/tls/v3/common.proto", "https://www.rfc-editor.org/rfc/rfc5280"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revoking and deny-listing client certificates

## Options
1. **CRL checking at the terminator**
   - nginx: `ssl_crl file;` takes a PEM CRL used to verify client certificates (so `ssl_verify_client` must be on). When intermediate CAs are used, their CRLs go in the same file.
   - Envoy: `crl` in the certificate validation context (PEM; several CRLs in one source are all used). If it is a filesystem path, Envoy watches the parent directory for file moves to support rotation, but only for dynamic secrets delivered via SDS.
2. **OCSP for client certificates**: nginx `ssl_ocsp on|leaf;` (nginx 1.19.0 and later) validates the client chain, or the leaf only with `leaf`. It needs `ssl_verify_client` set to `on` or `optional`, and a `resolver` to look up the responder hostname.
3. **Short-lived certificates**: a design choice rather than a documented feature of the above; with automated renewal, revocation reduces to refusing to renew.
4. **Application deny list**: after the handshake, check the certificate serial or fingerprint against a revoked list. nginx exposes `$ssl_client_fingerprint` for this.

## CRL pitfalls
- **Cover the whole chain.** Envoy: if a CRL is provided for any CA in the trust chain, one must be provided for every CA in it, otherwise verification fails for both revoked and unrevoked certificates. Setting `only_verify_leaf_cert_crl` to true limits checking to the final certificate.
- **Refresh before `nextUpdate`.** In RFC 5280 the `nextUpdate` field says the date by which the next CRL will be issued (possibly earlier, never later), and conforming issuers must include it. Fetch and deploy each new CRL before then.

## Process
- Revoke at the CA, regenerate the CRL, push it to every terminator and verify the new file is in use.
- Measure the time from revocation to rejection at each edge and record it.
- Test with a revoked certificate: the handshake must fail.

## Checked
Method: docs-checked 2026-11-09 against nginx ngx_http_ssl_module page (ssl_crl, ssl_ocsp, ssl_verify_client, variables), Envoy tls v3 common.proto raw source (crl, only_verify_leaf_cert_crl) and RFC 5280 section 5.1.2.5.
Removed as unconfirmed: nginx rejecting all clients once the CRL expires, HAProxy `crl-file`, Apache `SSLOCSPEnable`, specific CA revoke commands, the 1-24 h lifetime figure, claims that TLS sessions and keep-alive connections survive revocation, the `X-Client-Cert` header, and the sample openssl command.
