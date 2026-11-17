---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-mtls-client-authentication
name: oauth-mtls-client-authentication
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-mtls-client-authentication, oauth-mtls, rfc8705, tls_client_auth, self_signed_tls_client_auth, mtls, client-certificate, identity-protocols]
level: advanced
status: docs-checked
description: "Authenticate clients at the token endpoint with tls_client_auth (PKI, subject DN or SAN) or self_signed_tls_client_auth (registered JWKS)."
sources:
  - https://www.rfc-editor.org/rfc/rfc8705
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mTLS client authentication

Goal: use certificates instead of secrets for client authentication.

Method (RFC 8705 Section 2):
- PKI method: register `token_endpoint_auth_method` `tls_client_auth` and MUST use exactly one of `tls_client_auth_subject_dn`, `tls_client_auth_san_dns`, `tls_client_auth_san_uri`, `tls_client_auth_san_ip`, `tls_client_auth_san_email`. The AS relies on a validated certificate chain and matches the subject DN or subject alternative name.
- Self-signed method: register `self_signed_tls_client_auth` and the client's certificates through `jwks` or `jwks_uri`; each certificate is the `x5c` of a JWK in the set, and the AS matches the presented certificate to it.
- The client MUST include `client_id` in every request to the AS that uses mutual-TLS client authentication, so the AS can find the client's registration.

Gotchas:
- Which CAs are trusted for validating client and server certificates is a local decision (out of scope in RFC 8705).
- Server metadata `mtls_endpoint_aliases` lists alternative endpoints (for example `token_endpoint`) that a client intending to use mutual TLS MUST use in preference to the conventional ones; the aliases may use a different host, so the AS can differ its TLS behaviour per host (e.g. by server_name).
- Certificate-bound tokens and mutual-TLS client authentication can be used independently of each other.

Verify: call the token endpoint with a client certificate and key, then without a certificate; the second call must fail client authentication.

## Checked

Date: 2026-11-02. Confirmed in RFC 8705 Sections 2.1, 2.2, 2.3, 3.4 and 5 (metadata, `mtls_endpoint_aliases`, `client_id`). Removed as not stated there: "automate renewal" and "certificate expiry equals credential expiry", and the claim that the self-signed variant "enables rotation".

Method: documentation only; no commands were run.
