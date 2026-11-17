---
id: computing-software.cryptography-implementation.protocol-implementation.dedicated-client-auth-ca-design
name: dedicated-client-auth-ca-design
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, client-auth-ca, mutual-tls, mtls, pki-design, client-certificates]
level: advanced
status: docs-checked
description: "Design a dedicated CA for mTLS client certificates: EKU clientAuth, SPIFFE-style URI identity, separate trust domains, and scoping the server trust list."
sources: ["https://www.rfc-editor.org/rfc/rfc5280", "https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/transport_sockets/tls/v3/common.proto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated client-auth CA design

## Why separate
- A server verifies client certificates against whatever CA certificates it is configured to trust. Pointing that list at a CA that issues certificates to others (such as a public CA) means any certificate it issued can pass chain validation, so use a CA you control and scope the list to it.
- SPIFFE guidance: keep workloads in different locations, or in environments with different security practices (for example staging or lab versus production), in distinct trust domains. An SVID is valid only if signed by an authority within its SPIFFE ID's trust domain.

## Profile
- Extended key usage (RFC 5280 section 4.2.1.12): if present, the certificate may only be used for one of the listed purposes, and an application may require a particular purpose. `id-kp-clientAuth` is "TLS WWW client authentication", with digitalSignature and/or keyAgreement as consistent key usage bits. Key usage and extended key usage are processed independently and the certificate may only be used for a purpose consistent with both.
- Identity: a SPIFFE ID is a URI of the form `spiffe://trust-domain/workload-identifier`, which fits a URI subject alternative name.
- Lifetimes and root/intermediate layout are policy choices, not defined by these sources.

## Server configuration
- nginx `ssl_client_certificate file;` names the PEM trusted CA certificates used to verify client certificates. The list is sent to clients; `ssl_trusted_certificate` verifies without sending the list.
- Envoy `trusted_ca` in the validation context holds the trusted CAs. If it is a filesystem path, a watch is added on its parent directory to support rotation.
- Certificate validity proves authentication only; map the identity to permissions explicitly in the application.

## Verify
- [ ] A client certificate from a different CA (for example staging) is rejected.
- [ ] A certificate without the clientAuth purpose is rejected where the verifier requires it.

## Checked
Method: docs-checked 2026-11-09 against RFC 5280 section 4.2.1.12, the SPIFFE concepts page (SPIFFE ID, trust domain, SVID), the nginx ngx_http_ssl_module page and the Envoy tls v3 common.proto source.
Removed as unconfirmed: the claim that Chrome root program policy drops clientAuth EKU from public TLS server certificates in 2026 (the Chrome page was not confirmed), name constraints advice, specific keyUsage and lifetime recommendations, and the example SPIFFE URI. Section 4.2.1.12 only was read for the EKU text.
