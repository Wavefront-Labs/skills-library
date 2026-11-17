---
id: computing-software.data-engineering.druid.druid-authentication-and-authorization-chain
name: druid-authentication-and-authorization-chain
category: computing-software
field: data-engineering
product: druid
tags: [authentication, authorization, authenticator-chain, escalator, basic-security, kerberos]
level: advanced
status: docs-checked
description: "Configure the authenticator chain, escalator and authorizers."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core security properties (non-extension-specific):
- `druid.auth.authenticatorChain`: JSON list of Authenticator names, default `["allowAll"]`.
- `druid.escalator.type`: the Escalator used for internal Druid communications (for example Broker to Historical), default `"noop"`. It must use an authentication scheme supported by an Authenticator in the chain.
- `druid.auth.authorizers`: JSON list of Authorizer names, default `["allowAll"]`.
- `druid.auth.unsecuredPaths`: paths where security checks are skipped; all requests to them are allowed. Default empty.
- `druid.auth.allowUnauthenticatedHttpOptions`: default false. If true, unauthenticated HTTP OPTIONS requests are allowed, mainly for CORS preflight (which Druid does not support directly; third-party extensions can). You must also add `"OPTIONS"` to `druid.server.http.allowedHttpMethods`. It lets unauthenticated users learn which endpoints are valid and information about server configuration, including loaded extensions.

## Authenticator chain

A request is checked by Authenticators in the order of `druid.auth.authenticatorChain` until one authenticates it or sends an HTTP error response; later ones are skipped. If none does, an HTTP error response is sent at the end. Implementations come from extensions. This enables the Kerberos and HTTP Basic authenticators from the `druid-kerberos` and `druid-basic-security` core extensions:
```
druid.auth.authenticatorChain=["kerberos", "basic"]
```
Built-in authenticators:
- `allowAll`: authenticates everything and directs it to the Authorizer named `allowAll`; only for the default unsecured configuration (`druid.auth.authorizer.allowAll.type=allowAll`).
- `anonymous` (type `anonymous`): authenticates everything and routes it to the Authorizer named by `druid.auth.authenticator.<name>.authorizerName` (required), with `identity` default `defaultUser`. Meant for a default level of access, so put it at the end of the chain.
- `trustedDomain` (type `trustedDomain`): authenticates requests from `domain` (a fully qualified host name if only one host is allowed), with required `name` and `authorizerName`, optional `identity` and `useForwardedHeaders` (default false; the leftmost X-Forwarded-For host is used, which can be spoofed, so enable with caution).

## Authorizers and defaults

Only one Authorizer authorizes any given request. The built-in `allowAll` authorizer accepts every request; extensions provide others, for example `druid.auth.authorizers=["basic"]` from `druid-basic-security`. If the chain or authorizer list is empty or unspecified, Druid creates a single `allowAll` Authenticator or Authorizer, and the `noop` escalator matches that unsecured default, so a fresh cluster is open until you change them.

An authenticated request carries an AuthenticationResult naming the identity and the Authorizer to use. Internal requests run as an "internal system user" with full access; how it is defined is left to extensions. Property names `druid.auth.authenticator.<name>.name` and `druid.auth.authorizer.<name>.name` are reserved for extension implementers.

## Checked

Confirmed against the Druid docs page "Authentication and Authorization": property table defaults, chain semantics, built-in authenticators and their properties, authorizer rules and default unsecured behaviour. Corrected the chain example to the page's JSON list syntax and removed the closing note that restated the page without adding checkable content.

Method: docs-only read of cited pages, 2026-11-08
