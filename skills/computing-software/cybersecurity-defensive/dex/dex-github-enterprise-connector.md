---
id: computing-software.cybersecurity-defensive.dex.dex-github-enterprise-connector
name: dex-github-enterprise-connector
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [github-enterprise, connector, hostname, rootca]
level: practitioner
status: docs-checked
description: "Point the Dex GitHub connector at GitHub Enterprise with hostName and an optional rootCA for self-signed certificates."
sources:
  - https://dexidp.io/docs/connectors/github/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GitHub Enterprise uses the same `github` connector type with two extra fields. Register Dex as an OAuth app on the Enterprise instance first, then:

```yaml
connectors:
- type: github
  id: github
  name: GitHub
  config:
    clientID: $GITHUB_CLIENT_ID
    clientSecret: $GITHUB_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    orgs:
    - name: my-organization
    teamNameField: slug
    hostName: git.example.com
    rootCA: /etc/dex/ca.crt
```

- `hostName`: required only for GitHub Enterprise. It is the hostname of the Enterprise account as listed on the management console. The docs say to make sure this domain is routable on your network.
- `rootCA`: optional, for self-signed or untrusted CA root certificates.

All the cloud options (`orgs`, `teams`, `loadAllGroups`, `teamNameField`) still apply, including the `org:team` group claim format.

Gotchas:

- `hostName` must be routable on your network.

The page's example client run is `./bin/example-app --issuer-root-ca examples/k8s/ssl/ca.pem`.

## Checked

2026-11-03: read against Dex docs, GitHub connector (https://dexidp.io/docs/connectors/github/).

Removed or corrected: The unconfirmed callback-must-equal-redirectURI gotcha; reworded the Kubernetes guide remark.

Method: documentation only; no commands were run.
