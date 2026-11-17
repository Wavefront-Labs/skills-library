---
id: computing-software.database-administration.elasticsearch.saml-and-oidc-single-sign-on
name: saml-and-oidc-single-sign-on
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, saml-realm, oidc-realm, elasticsearch-security, single-sign-on, role-mapping]
level: practitioner
status: docs-checked
description: "Configure Elasticsearch SAML or OpenID Connect realms for Kibana single sign-on, map IdP groups to roles, and debug assertion and redirect failures."
sources:
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/users-roles/cluster-or-deployment-auth/saml-attribute-mapping.md
  - https://github.com/elastic/docs-content/blob/main/troubleshoot/elasticsearch/security/trb-security-saml.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/bootstrap-checks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML and OIDC single sign-on

**Goal:** users log in to Kibana with Okta/Entra ID/ADFS, with roles from IdP groups. SSO is a subscription feature; check the Elastic subscriptions page for your tier.

## Prerequisites
- TLS on the HTTP layer (`xpack.security.http.ssl.enabled: true`).
- Token service: set `xpack.security.authc.token.enabled: true`; the token service requires HTTPS on the HTTP interface (a bootstrap check enforces this).

## SAML realm (elasticsearch.yml, every node)
```yaml
xpack.security.authc.realms.saml.okta1:
  order: 2
  idp.metadata.path: "https://example.okta.com/app/abc/sso/saml/metadata"
  idp.entity_id: "http://www.okta.com/abc"
  sp.entity_id: "https://kibana.example.com"
  sp.acs: "https://kibana.example.com/api/security/saml/callback"
  sp.logout: "https://kibana.example.com/logout"
  attributes.principal: "nameid"
  attributes.groups: "groups"
```
Kibana (`kibana.yml`):
```yaml
xpack.security.authc.providers:
  saml.okta1: { order: 0, realm: "okta1", description: "Log in with Okta" }
  basic.basic1: { order: 1 }      # keep a break-glass login
```

## OIDC realm
```yaml
xpack.security.authc.realms.oidc.entra1:
  order: 3
  rp.client_id: "<app id>"
  rp.response_type: code
  rp.redirect_uri: "https://kibana.example.com/api/security/oidc/callback"
  op.issuer: "<op issuer URL>"
  op.authorization_endpoint: "<op authorization endpoint>"
  op.token_endpoint: "<op token endpoint>"
  op.jwkset_path: "<URL or path of the JWKS>"   # a local file path is allowed
  claims.principal: sub                      # use the claim your OP releases
  claims.groups: "<groups claim name>"
```
Client secret goes in the keystore: `bin/elasticsearch-keystore add xpack.security.authc.realms.oidc.entra1.rp.client_secret`.

## Role mapping
```json
PUT _security/role_mapping/okta-admins
{ "roles": ["superuser"], "enabled": true,
  "rules": { "all": [ { "field": { "realm.name": "okta1" } }, { "field": { "groups": "es-admins" } } ] } }
```

## Debugging
- Enable `logger.org.elasticsearch.xpack.security.authc.saml: debug` temporarily (via the cluster settings API); logs show signature and audience failures.
- Common causes: `sp.entity_id` not matching the audience the IdP sends (the log line `does not match required audience` shows both values), ACS URL not exactly matching (`sp.acs` is `<kibana>/api/security/saml/callback`), the OIDC redirect URI not exactly matching (`<kibana>/api/security/oidc/callback`), IdP signing keys not matching the metadata, groups attribute not released by the IdP.

## Verify
Log in through Kibana; `GET _security/_authenticate` from the session shows `authentication_realm.name: okta1` and expected `roles`.

## Checked

Checked 2026-10-25 against elastic/docs-content `main` (Stack 9.x docs). Confirmed: SSO is a subscription feature; SAML realm settings `idp.metadata.path`, `idp.entity_id`, `sp.entity_id`, `sp.acs` (callback path), `attributes.principal` (`nameid`) and `attributes.groups`; OIDC settings `rp.client_id`, `rp.response_type`, `rp.redirect_uri`, `op.*`, `claims.*`, `op.jwkset_path` file option, client secret via keystore setting `...rp.client_secret`; token service needs HTTPS; the SAML debug logger name; audience mismatch troubleshooting. Removed unconfirmed claims: token service on by default, the `allowed_clock_skew` default and the Entra endpoint values. Kibana `xpack.security.authc.providers` layout (documented in the SAML page) and the role mapping JSON were not re-read line by line; `sp.logout` is an optional setting not confirmed here.

Method: documentation only; no commands were run.
