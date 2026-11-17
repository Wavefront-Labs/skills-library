---
id: computing-software.cryptography-implementation.protocol-implementation.alpn-for-http2-and-http3
name: alpn-for-http2-and-http3
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, alpn-h2-h3, alpn, http2, http3, quic, alt-svc]
level: practitioner
status: docs-checked
description: "Configure ALPN for HTTP/2 and HTTP/3: protocol identifiers, HTTP/2 TLS requirements, Alt-Svc and HTTPS DNS records for h3, and diagnosing fallback to HTTP/1.1."
sources: ["https://www.rfc-editor.org/rfc/rfc7301", "https://www.rfc-editor.org/rfc/rfc9113#section-9.2", "https://www.rfc-editor.org/rfc/rfc9460", "https://www.rfc-editor.org/rfc/rfc7838"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALPN for HTTP/2 and HTTP/3

## HTTP/2 over TLS
- The client offers `h2` and `http/1.1` in the ALPN extension; the server selects one. `h2` (octets 0x68 0x32)
  identifies HTTP/2 over TLS. `h2c` is the cleartext identifier and MUST NOT be sent by a client or selected by a
  server for HTTP/2 over TLS (RFC 9113 section 3).
- RFC 9113 9.2: HTTP/2 over TLS needs TLS 1.2 or higher, the server_name (SNI) extension, and for TLS 1.2 compression
  and renegotiation disabled. TLS 1.2 deployments should avoid the prohibited cipher suites in RFC 9113 Appendix A,
  and must support TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 with P-256. An endpoint may close a connection that
  negotiates a prohibited suite with an `INADEQUATE_SECURITY` error, so check your cipher list against Appendix A.
- With TLS 1.3, servers MUST NOT send post-handshake CertificateRequest on HTTP/2 connections.
- Completing a TLS handshake that selects `h2` is sufficient protection against cross-protocol attacks.
- Server configuration syntax differs per product; list `h2` before `http/1.1` in the product's ALPN setting.

## HTTP/3
- HTTP/3 runs over QUIC with ALPN `h3` (RFC 9460 7.1 shows a client trying `h3` over QUIC alongside `h2` and
  `http/1.1` over TLS/TCP). Clients discover it by:
  - an `Alt-Svc` header on an HTTP/1.1 or h2 response, e.g. `Alt-Svc: h3=":443"; ma=86400` (RFC 7838 defines the
    `ma` freshness parameter in seconds and `persist`), or
  - a DNS HTTPS record (RFC 9460) with an `alpn` SvcParam listing the protocols, e.g. `alpn="h2,h3"`. The default
    ALPN set for HTTPS records is the single value `http/1.1`, unless `no-default-alpn` is present.
- QUIC uses UDP: open UDP in firewalls and load balancers, since a blocked UDP path makes clients fall back to TCP.

## Diagnose
- Capture the ClientHello and ServerHello and check the ALPN extension on both sides.
- TLS-terminating proxies must pass ALPN through or terminate h2 themselves; L4 load balancers forwarding TCP leave
  ALPN to the backend.
- Browser developer tools show the negotiated protocol per request.

## Verify
- [ ] The server's ALPN selection is `h2` for a client offering `h2, http/1.1`, and the browser shows h2 / h3.
- [ ] The negotiated TLS 1.2 cipher suite is not on the RFC 9113 Appendix A list.

## Checked
2026-11-01. Confirmed against RFC 9113 (sections 3, 9.2, 9.2.1 to 9.2.3), RFC 9460 (sections 7.1 and 9 on
alpn, no-default-alpn and the HTTPS default ALPN set) and RFC 7838 (Alt-Svc, ma, persist). Removed: nginx, Apache,
HAProxy and Envoy configuration lines and version numbers, openssl and curl diagnostic commands, a fixed UDP port
and the claim that "no ALPN means HTTP/1.1".
Method: documentation only; no commands were run.
