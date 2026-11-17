---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-protected-resource-metadata
name: oauth-protected-resource-metadata
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-protected-resource-metadata, oauth-metadata-issuer, rfc9728, protected-resource-metadata, resource_metadata, authorization_servers, identity-protocols]
level: advanced
status: docs-checked
description: "Publish /.well-known/oauth-protected-resource so clients learn the authorization servers, scopes and bearer methods for an API, linked from WWW-Authenticate."
sources:
  - https://www.rfc-editor.org/rfc/rfc9728
  - https://www.rfc-editor.org/rfc/rfc8414
  - https://www.rfc-editor.org/rfc/rfc9207
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protected resource metadata (RFC 9728)

Goal: let a client discover how to get a token for an API.

Method: publish a JSON document at a URL formed by inserting the well-known string `oauth-protected-resource` between the host and the path/query of the resource identifier, for example `https://api.example.com/.well-known/oauth-protected-resource` (with the resource path appended for a resource that has one). Members include `resource` (the resource identifier), `authorization_servers` (array of issuer identifiers), `scopes_supported`, `bearer_methods_supported`, `resource_signing_alg_values_supported`, `dpop_signing_alg_values_supported` and `jwks_uri`. The metadata is fetched with HTTP GET. In a 401 `WWW-Authenticate` response the resource adds the parameter `resource_metadata`, the URL of its metadata.

Gotchas:
- If the metadata came from a `resource_metadata` URL, the `resource` value MUST be identical to the URL the client used to request the resource; if not, the metadata MUST NOT be used (RFC 9728 Section 3.3). The client must also check that the resource identifier URL it used as the prefix for the metadata request exactly matches `resource` (impersonation defence, Section 7.3), and perform TLS certificate checks.
- Then fetch the authorization server metadata (RFC 8414); its `issuer` MUST be identical to the issuer identifier used to build the metadata URL.
- `scopes_supported` lists scopes the RS is willing to disclose; it does not mean the client should request all of them.

Verify: request the API without a token and follow the `resource_metadata` link.

## Checked

Date: 2026-11-02. Confirmed in RFC 9728 (well-known path, members, resource_metadata, resource match, Section 7.3 impersonation) and RFC 8414 (issuer identity). Removed as not stated there: the claim about MCP-style tool servers, "attacker's API can point at a legitimate AS and harvest tokens" wording, and RFC 9207 as a basis for any claim (it remains listed as related reading on issuer identification).

Method: documentation only; no commands were run.
