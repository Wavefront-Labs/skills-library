---
id: computing-software.cybersecurity-defensive.keycloak.action-token-handler-spi
name: action-token-handler-spi
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, action-token, jwt, verify-email, handler-spi]
level: practitioner
status: docs-checked
description: "Understand Keycloak action tokens (verify email, reset credentials) and extend them with the action token handler SPI."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_development/topics/action-token-handler-spi.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# action token handler spi
An action token is a special JWT that permits its bearer to perform an action such as resetting a password or validating an email address, usually sent as a link. Keycloak offers four basic token types: reset credentials, confirm email address, execute required action(s), and confirm linking of an account with an external identity provider. The action token handler SPI lets you implement any functionality that initiates or modifies an authentication session.

Anatomy: a standard JWT signed with the active realm key; payload fields:
- `typ`: identification of the action (for example `verify-email`);
- `iat`, `exp`: times of validity;
- `sub`: user id; `azp`: client name; `iss`: URL of the issuing realm; `aud`: list containing the realm URL;
- `asid` (optional): authentication session id;
- `nonce` (optional): random nonce guaranteeing uniqueness of use when the operation can run only once.
Custom JSON-serialisable fields are allowed.

Processing: a token passed to `<root>/realms/master/login-actions/action-token` via the `key` parameter is validated (signature, time, handler chosen by `typ`), attached to or replaces the browser's authentication session, validated per token type (user and client exist and are enabled, custom validations, single-use check), then the handler acts; single-use tokens are invalidated when the flow finishes.

Implement `ActionTokenHandler` (extend `AbstractActionTokenHandler`; only `handleToken(token, context)` is mandatory) and `ActionTokenHandlerFactory` (`getId()` must match the token's `typ` exactly), and register the factory like any SPI provider. A custom token class can extend `DefaultActionToken`, which must have a private no-argument constructor.

## Checked
2026-11-03. Confirmed against server_development/topics/action-token-handler-spi.adoc. Removed (not on the page): the realm *Tokens* tab lifespans, the key-rotation, short-lifetime, hostname and mail-scanner remarks, and the Verify step.
Method: documentation only; no commands were run.
