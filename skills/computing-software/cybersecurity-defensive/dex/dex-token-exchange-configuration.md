---
id: computing-software.cybersecurity-defensive.dex.dex-token-exchange-configuration
name: dex-token-exchange-configuration
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [token-exchange, oidc, machine-auth, workload-identity]
level: advanced
status: docs-checked
description: "Configure Dex for RFC 8693 token exchange so CI jobs swap an upstream OIDC token for a Dex token: oidc connector and a public client."
sources:
  - https://dexidp.io/docs/guides/token-exchange/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Interactive connectors are hard for machines such as CI pipelines. Token exchange lets a client trade an access or ID token it already holds for a Dex token, like GCP or AWS web identity federation. Runners such as GitHub Actions, Buildkite and CircleCI can use it.

Flow: the client gets a token from the upstream IdP, exchanges it at Dex, uses the Dex token, and repeats at expiry.

Only the OIDC connector supports token exchange. `clientID`, `clientSecret` and `redirectURI` are not required for it.

```yaml
oauth2:
  grantTypes:
  - "urn:ietf:params:oauth:grant-type:token-exchange"
connectors:
- name: My Upstream
  type: oidc
  id: my-upstream
  config:
    issuer: https://token.example.com
    scopes:
    - groups
    - federated:id
    userNameKey: sub
    # getUserInfo: true
staticClients:
- name: My App
  id: my-app
  secret: my-secret
  public: true
```

Notes:

- The submitted subject token is verified against the connector `issuer`.
- `getUserInfo` is required to exchange access tokens, since access tokens are treated as opaque and validated through the user info endpoint.
- The exchange grant is in the default `grantTypes`; keep it if you set the list.
- The client is public because the caller would otherwise need the secret. To serve humans and machines, create a dedicated public client and use cross-client trust.

## Checked

2026-11-08: Read the Dex Machine Authentication guide in full. Confirmed the purpose, the flow steps, OIDC-only support, the optional fields, the config example, issuer verification of the subject token, getUserInfo for access tokens, the default grant type and the public client rationale.
Method: documentation only; no commands were run.
