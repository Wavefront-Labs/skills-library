---
id: computing-software.cloud-infrastructure-engineering.docker.registry-token-auth-with-external-auth-server
name: registry-token-auth-with-external-auth-server
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, registry, registry-auth, registry-token-auth, bearer-token, docker-auth, private-registry]
level: advanced
description: "Configure distribution's token auth so an external server (docker_auth, Harbor core, Keycloak bridge) issues scoped bearer JWTs with per-repo ACLs."
sources: ["https://distribution.github.io/distribution/spec/auth/token/", "https://distribution.github.io/distribution/about/configuration/", "https://github.com/cesanta/docker_auth"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registry token auth with an external auth server

htpasswd is all-or-nothing. Token auth lets an auth server decide per user, per repository,
per action (`pull`, `push`, `delete`).

## The flow
1. Client hits `GET /v2/...` -> registry returns `401` with
   `WWW-Authenticate: Bearer realm="https://auth.example.com/token",service="registry.example.com",scope="repository:team-a/api:pull,push"`.
2. Client calls the realm with basic creds and those params.
3. Auth server returns a JWT signed with its private key containing an `access` claim:
   `[{"type":"repository","name":"team-a/api","actions":["pull","push"]}]`.
4. Client retries with `Authorization: Bearer <jwt>`; registry verifies signature, `iss`,
   `aud` (= service), expiry and the access claim.

## Registry config
```yaml
auth:
  token:
    realm: https://auth.example.com/token
    service: registry.example.com
    issuer: "Acme auth server"
    rootcertbundle: /certs/auth-server.crt   # public part of the cert used to sign tokens
```

## docker_auth server example
```yaml
server: { addr: ":5001" }
token:
  issuer: "Acme auth server"       # must equal registry issuer
  expiration: 900
  certificate: /certs/auth-server.crt
  key: /certs/auth-server.key
users:
  "ci": { password: "$2y$05$..." }  # bcrypt
ldap_auth: { addr: ldap.example.com:636, tls: always, base: "ou=people,dc=example,dc=com" }
acl:
  - match: { account: "ci" }
    actions: ["pull", "push"]
  - match: { account: "/.+/", name: "${account}/*" }   # users own their namespace
    actions: ["*"]
  - match: { account: "/.+/" }
    actions: ["pull"]
```

## Gotchas
- `issuer` and `service` must match exactly between registry and auth server, or every
  request is rejected as unauthorized - check the registry log. The registry `issuer` must match the `iss` the auth server inserts.
- Token validity is time based, so keep clocks in sync on the registry and the auth server.
- Trusted signing keys come from `rootcertbundle` (public part of the signing certificate, identified by JWK thumbprint) and/or `jwks` (a JWKS file of trusted keys).
- Harbor, GitLab and Quay already implement this; only run your own server for bare
  distribution.

## Verify
```sh
curl -si https://registry.example.com/v2/ | grep -i www-authenticate
curl -s -u ci:pass "https://auth.example.com/token?service=registry.example.com&scope=repository:team-a/api:pull"
# the JSON response carries the token (and may carry access_token and expires_in)
```

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (token spec, configuration auth.token table) and cesanta/docker_auth examples/reference.yml. Confirmed: 401 with WWW-Authenticate Bearer realm, service and scope challenge, realm/service/issuer/rootcertbundle/jwks keys under auth.token, issuer must match the issuer the token carries, rootcertbundle holds the public part of signing certificates, docker_auth server.addr, token.issuer, token.expiration, token.certificate/key, ldap_auth tls and base keys, acl match with account and name and the `${account}` expansion. Removed unconfirmed claims: the registry:catalog scope, the `401 invalid token` message, certificate rollover advice, nbf-specific validation, and the JWT decoding pipeline.

Method: documentation only; no commands were run.
