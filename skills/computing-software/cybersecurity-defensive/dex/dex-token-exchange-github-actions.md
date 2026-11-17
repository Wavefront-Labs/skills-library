---
id: computing-software.cybersecurity-defensive.dex.dex-token-exchange-github-actions
name: dex-token-exchange-github-actions
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [token-exchange, github-actions, oidc, ci]
level: advanced
status: docs-checked
description: "Exchange a GitHub Actions OIDC token for a Dex token in a workflow, using the id-token write permission and a Dex service container."
sources:
  - https://dexidp.io/docs/guides/token-exchange/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs show Dex running as a service inside a GitHub Actions workflow and exchanging the job's OIDC token.

Dex config uses the GitHub Actions issuer as an OIDC connector:

```yaml
issuer: http://127.0.0.1:5556/
storage:
  type: sqlite3
  config:
    file: dex.db
web:
  http: 0.0.0.0:8080
connectors:
- type: oidc
  id: github-actions
  name: github-actions
  config:
    issuer: https://token.actions.githubusercontent.com
    scopes:
    - openid
    - groups
    userNameKey: sub
staticClients:
- name: My app
  id: my-app
  secret: my-secret
  public: true
```

Workflow essentials:

```yaml
permissions:
  id-token: write
jobs:
  job:
    runs-on: ubuntu-latest
    services:
      dex:
        image: ghcr.io/dexidp/dex:latest
        ports:
        - 80:8080
```

Replace the service image with one that has your config baked in. The `id-token: write` permission is required to request the JWT. A `github-script` step reads `ACTIONS_RUNTIME_TOKEN` and `ACTIONS_ID_TOKEN_REQUEST_URL`, which inline scripts cannot see, then `curl` fetches the GitHub token and posts it to `http://127.0.0.1/token` with `connector_id=github-actions`.

Gotcha: the sample client sets `public: true`, so its secret is not treated as secret.

## Checked

2026-11-08: Read the Dex Machine Authentication guide in full. Confirmed the Dex config, the id-token write permission, the Dex service container with an image that includes the config, the github-script step and the exchange request to the /token endpoint. Removed the workflow secrets advice, which that page does not state.
Method: documentation only; no commands were run.
