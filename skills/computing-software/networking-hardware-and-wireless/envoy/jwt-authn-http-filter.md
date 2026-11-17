---
id: computing-software.networking-hardware-and-wireless.envoy.jwt-authn-http-filter
name: jwt-authn-http-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, jwt-authn, jwt, jwks, remote-jwks, providers, rules, requirement, forward-payload-header]
level: practitioner
status: docs-checked
description: "Validate JWTs in Envoy with the jwt_authn filter: providers, remote or inline JWKS, audiences, per-path rules and payload forwarding."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/jwt_authn_filter.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/security/jwt_authn_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jwt authn http filter
The jwt_authn filter verifies a JWT signature, audiences, issuer and time restrictions. Supported algorithms: ES256/384/512, HS256/384/512, RS256/384/512, PS256/384/512 and EdDSA. Config has two fields: `providers` (how to verify: where to extract the token, where to fetch the JWKS, where to output the payload) and `rules` (route matches and the requirement for each).

```yaml
http_filters:
- name: envoy.filters.http.jwt_authn
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
    providers:
      provider_name1:
        issuer: https://example.com
        audiences: [bookstore_android.apps.googleusercontent.com]
        remote_jwks:
          http_uri: { uri: https://example.com/jwks.json, cluster: example_jwks_cluster, timeout: 1s }
          cache_duration: 300s
    rules:
    - match: { prefix: /api }
      requires: { provider_name: provider_name1 }
```
If `audiences` is empty, audiences are not checked. JWKS may be inline or fetched via a cluster, which must exist and use TLS (`UpstreamTlsContext` with `sni`) for HTTPS. The verified header and payload can be written to dynamic metadata so later filters (RBAC) can use claims; a path not listed in `rules` is allowlisted, which is how public paths are exempted.

Gotcha: per the docs, a request that matches no rule, or a rule with an empty `requires`, does not need JWT verification, so end with a catch-all requirement. The JWKS cluster must be reachable for remote keys to be fetched. Verify with a valid and a tampered token via curl.

## Checked

2026-11-03. Confirmed against: jwt_authn_filter.rst (algorithms, providers and rules, no-match behaviour) and jwt_authn config.proto (remote_jwks, cache_duration). Removed or corrected: the jwt_authn.* stats claim.

Method: documentation only; no commands were run.
