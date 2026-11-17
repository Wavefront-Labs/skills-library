---
id: computing-software.devops-ci-cd.verdaccio.uplink-authentication-tokens
name: uplink-authentication-tokens
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [uplink-auth, token-env, private-registry, uplink-token, npm-token-env, codeartifact, bearer]
level: practitioner
status: docs-checked
description: "Authenticate to a private upstream registry with the uplink auth block using token_env or token, including the AWS CodeArtifact header settings and Helm secrets."
sources:
  - https://verdaccio.org/docs/uplinks/
  - https://verdaccio.org/docs/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
uplinks:
  private:
    url: https://private-registry.domain.com/registry
    auth:
      type: bearer
      token_env: true        # reads NPM_TOKEN
```
- `token_env: FOO_TOKEN` reads `process.env['FOO_TOKEN']` instead.
- `token: 'value'` writes it in the file (not recommended). `token` takes priority over `token_env`.
- Helm chart: inject with `secretEnvVars` (chart 4.8.0+), e.g. `--set secretEnvVars.FOO_TOKEN=...`.

AWS CodeArtifact needs `accept: */*` in headers:
```yaml
uplinks:
  aws-codeArtifact:
    url: https://private-registry.domain.com/registry
    cache: false
    auth:
      type: bearer
      token_env: CODEARTIFACT_AUTH_TOKEN
    strict_ssl: false
    headers:
      'Accept': '*/*'
      'Accept-Encoding': 'gzip, deflate, br'
      'Cache-Control': 'no-cache'
```
The `headers` key sets custom headers for any uplink (for example `authorization`).

## Checked

2026-11-04. Confirmed against the Verdaccio Uplinks page (auth block, token_env, token priority, CodeArtifact accept header example, secretEnvVars) and Kubernetes page (chart 4.8.0). Removed: the unsupported 401 troubleshooting tip.
Method: documentation only; no commands were run.
