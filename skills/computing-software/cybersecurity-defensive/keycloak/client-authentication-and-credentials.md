---
id: computing-software.cybersecurity-defensive.keycloak.client-authentication-and-credentials
name: client-authentication-and-credentials
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, client-authenticator, client-secret, signed-jwt, manage-clients]
level: practitioner
status: docs-checked
description: "Choose Keycloak confidential client authentication (secret, signed JWT, IdP-issued JWT, JWT with client secret, X509) and who may read client secrets."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/oidc/con-confidential-client-credentials.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client authentication and credentials
The client's *Credentials* tab has a *Client Authenticator* drop-down that sets the credential type.

- **Client ID and Secret** (default): a random secret is generated; you can override it, *Regenerate* it, or reference a value in an external vault. The secret may go in an `Authorization: Basic` header with client_id, or as `client_id` and `client_secret` parameters in the POST body; *Allowed authentication method* restricts the client to one (for example Basic only).
- **Signed JWT issued by the client**: self-signed client assertions, no shared secret. You can enforce the *Signature algorithm* (any is valid by default) and *Max expiration* (tokens older than that are rejected; tokens should be issued right before authentication; 60 seconds by default). Configure the client's public key or certificate in the *Keys* tab; Keycloak never stores the private key. Recommended: generate the key pair externally and use *Use JWKS URL* (Keycloak reimports the key automatically if it changes), or *Import Certificate* (Certificate PEM, Public Key PEM, JSON Web Key Set or a keystore; an uploaded private key is discarded). Generating keys in the console is deprecated.
- **Signed JWT issued by an Identity Provider**: client assertions issued by an IdP (an OpenID Connect provider with client-assertion support enabled, SPIFFE JWT SVIDs, Kubernetes service accounts). Configure the *Identity provider* alias and the *Federated subject* (the `sub` claim of the assertion).
- **Signed JWT with Client Secret**: a JWT signed with the client secret (which can reference a vault); same Signature algorithm and Max expiration settings.
- **X509 Certificate**: Keycloak validates the client certificate during the TLS handshake, including the certificate Subject DN and the root CA Subject DN (trust anchor). The client_id comes from the `client_id` query or form parameter. Using a regexp such as `(.*?)(?:$)` for the Subject DN is deprecated.

Reading secrets: viewing a client secret through the Admin REST API needs `manage-clients`. Users with only `view-clients` see the masked placeholder `**********` on `GET /admin/realms/{realm}/clients`, `GET /admin/realms/{realm}/clients/{id}` and `GET /admin/realms/{realm}/clients/{id}/client-secret`. Any delegated administrator or automation that must read secrets needs the `manage-clients` realm role. For rotation see client-secret-rotation-policy.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/oidc/con-confidential-client-credentials.adoc. Removed: the "confirm against your version" hedge, the unsourced gotchas (public-client advice, shared-secret preference) and the Verify step; added the IdP-issued JWT and X509 details.
Method: documentation only; no commands were run.
