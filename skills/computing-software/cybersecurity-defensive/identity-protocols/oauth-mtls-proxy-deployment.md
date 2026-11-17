---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-mtls-proxy-deployment
name: oauth-mtls-proxy-deployment
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-mtls-proxy-deployment, oauth-mtls, mtls, load-balancer, reverse-proxy, client-cert-header, termination, identity-protocols]
level: sme
status: docs-checked
description: "Deploy mTLS-bound OAuth behind load balancers: passthrough versus termination, trusted certificate headers, separate mTLS endpoints and health checks."
sources:
  - https://www.rfc-editor.org/rfc/rfc8705
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS behind proxies and gateways

Goal: keep certificate binding intact in real infrastructure.

What RFC 8705 says: an AS or RS MAY terminate TLS at a load balancer, reverse proxy or other intermediary; how the client certificate metadata is securely communicated between the intermediary and the application server is out of scope (Section 6.5). The RS must still verify the certificate used on the connection against the one bound to the token (Section 3), so the application needs a trustworthy channel for that certificate or its hash.

Options:
1. Keep mutual TLS end to end (pass TLS through) so the application sees the certificate itself.
2. Terminate at the proxy and forward the certificate or its thumbprint to the application over a channel you can trust; design and document that hop yourself, since the RFC leaves it open.
3. Use `mtls_endpoint_aliases` in AS metadata so clients doing mutual TLS use alias endpoints, possibly on a different host, letting the AS behave differently on the mutual-TLS host (RFC 8705 Section 5).

Gotchas:
- If the trust in the forwarded certificate data fails, certificate binding stops protecting anything.
- The RFC does not describe particular headers, proxy products or request-versus-require settings; check your proxy's own documentation.

Verify: send forged certificate data from outside the trusted hop and confirm it is not accepted.

## Checked

Date: 2026-11-02. Confirmed in RFC 8705 Sections 3, 5 and 6.5. Removed as not stated there: the `X-Client-Cert` header name and URL-encoded PEM format, overwrite/strip rules, claims about cloud load balancers, request-not-require TLS advice.

Method: documentation only; no commands were run.
