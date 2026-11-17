---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-provider-metadata
name: oidc-provider-metadata
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-provider-metadata, oidc-discovery, discovery, well-known, openid-configuration, issuer, metadata, identity-protocols]
level: practitioner
status: docs-checked
description: "Consume /.well-known/openid-configuration: issuer match, endpoints, supported algorithms and the metadata fields that drive client behaviour."
sources:
  - https://openid.net/specs/openid-connect-discovery-1_0.html
  - https://www.rfc-editor.org/rfc/rfc8414.txt
  - https://openid.net/specs/openid-connect-rpinitiated-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider configuration document

Goal: configure a client from one URL.

Method: GET `{issuer}/.well-known/openid-configuration` (HTTP GET; the issuer's trailing `/` is removed first, and a path in the issuer comes before `/.well-known/openid-configuration`, for example `https://example.com/issuer1/.well-known/openid-configuration`). RFC 8414 uses `/.well-known/oauth-authorization-server` inserted between host and path for its own metadata. Key fields: `issuer` (required), `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint`, `jwks_uri`, `scopes_supported`, `response_types_supported`, `grant_types_supported`, `subject_types_supported`, `id_token_signing_alg_values_supported` (must include RS256), `token_endpoint_auth_methods_supported`, plus `end_session_endpoint` (RP-Initiated Logout) and `code_challenge_methods_supported` (RFC 8414).

Gotchas:
- The `issuer` in the document must be identical to the issuer URL used to fetch it, and to the `iss` claim in ID Tokens from that issuer.
- Defaults when omitted: `grant_types_supported` is `["authorization_code","implicit"]`; `response_modes_supported` is `["query","fragment"]`; `token_endpoint_auth_methods_supported` is `client_secret_basic`.
- `token_endpoint` is required unless only the implicit flow is used.

Verify: curl the document and compare issuer strings.

## Checked
2026-11-02. Confirmed against OpenID Connect Discovery 1.0 sections 3, 4 and 4.3, RFC 8414 and RP-Initiated Logout section 2.1. Removed: the "{tenantid} placeholder" remark, "cache with expiry; do not hard-code endpoints" and the RFC 8414-form confusion for path issuers (Discovery appends the well-known suffix after the issuer path).
Method: documentation only; no commands were run.
