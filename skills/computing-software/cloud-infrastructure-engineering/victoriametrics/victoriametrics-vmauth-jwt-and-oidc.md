---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmauth-jwt-and-oidc
name: victoriametrics-vmauth-jwt-and-oidc
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmauth, jwt, oidc, claims, multi-tenant-access, enterprise]
level: sme
status: docs-checked
description: "Authenticate vmauth users with JWT public keys or OIDC discovery and template tenant IDs from token claims."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmauth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmauth jwt and oidc

vmauth users can authenticate with a JWT instead of a password. Two verification modes appear in the docs.

Public key with claim matching:

```yaml
users:
  - jwt:
      public_keys:
        - |
          -----BEGIN PUBLIC KEY-----
          ...
          -----END PUBLIC KEY-----
      match_claims:
        role: admin
    url_prefix: "http://victoria-metrics-admin:8428/"
```

OIDC discovery from the identity provider issuer:

```yaml
users:
  - jwt:
      oidc:
        issuer: "https://your-identity-provider.example.com"
      match_claims:
        aud: "theClientID"
    url_prefix: "http://victoria-metrics:8428/"
```

`match_claims` restricts which tokens map to a user entry, so use different entries per role or audience.

Request templating lets tenant routing follow the token: `url_prefix` may contain placeholders such as `{{.MetricsAccountID}}` and `{{.MetricsProjectID}}` filled from the token `vm_access` claim, for example `http://vminsert:8480/insert/{{.MetricsAccountID}}:{{.MetricsProjectID}}/prometheus/`. This gives multi-tenant access for Grafana or vmagent with one vmauth.

The page presents these JWT forms alongside enterprise-only features such as `ip_filters`; confirm edition support for your release before depending on them. Keep `-reloadAuthKey` set so `/-/reload` cannot be triggered by anyone.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
