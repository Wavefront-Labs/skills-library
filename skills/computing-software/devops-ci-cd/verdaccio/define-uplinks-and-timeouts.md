---
id: computing-software.devops-ci-cd.verdaccio.define-uplinks-and-timeouts
name: define-uplinks-and-timeouts
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [uplinks, uplink-timeout, fail-timeout, uplink-definition, maxage, max-fails, strict-ssl]
level: practitioner
status: docs-checked
description: "Define Verdaccio uplinks and tune url, timeout, maxage, fail_timeout, max_fails, cache, strict_ssl, headers and agent_options per remote registry."
sources:
  - https://verdaccio.org/docs/uplinks/
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An uplink links an external npm-compatible registry (verdaccio, npmjs, JFrog, Nexus, yarn registry).

```yaml
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
  server2:
    url: http://mirror.local.net/
    timeout: 100ms
    maxage: 10m
    fail_timeout: 10m
    max_fails: 2
    cache: true
    strict_ssl: true
    agent_options:
      maxSockets: 10
```
Defaults: `timeout` 30s, `maxage` 2m (how long cached metadata is valid), `fail_timeout` 5m, `max_fails` 2, `cache` true, `strict_ssl` true. Time units follow NGINX notation. Other keys: `ca`, `headers`, `auth`, `http_proxy`, `https_proxy`, `no_proxy`.

How it behaves: for each client request Verdaccio makes one call to each configured uplink. `max_fails` limits failed requests and `fail_timeout` defines the max time before a request counts as a failure.

Gotchas:
- Each extra uplink adds lookup latency; limit per package with `proxy:` in `packages`.
- Names must be unique keys.

## Checked

2026-11-04. Confirmed against the Verdaccio Uplinks page (property table with defaults, NGINX time units, one call per uplink, unique names, compatible registries). Removed: the merge-and-skip behaviour claim and the closing Verify tip.
Method: documentation only; no commands were run.
