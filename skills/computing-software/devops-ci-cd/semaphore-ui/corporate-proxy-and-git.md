---
id: computing-software.devops-ci-cd.semaphore-ui.corporate-proxy-and-git
name: corporate-proxy-and-git
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [proxy, no-proxy, git, forwarded-env-vars, troubleshooting, semaphore-ui]
level: practitioner
status: docs-checked
description: "Fix git clone failures behind a corporate proxy by forwarding proxy and CA variables to Semaphore tasks."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/env-vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run Semaphore behind a corporate proxy

Goal: make git clones and tasks honor proxy settings.

Proxy variables set in a systemd unit apply only to the Semaphore server, not to git. With only this in the unit file:

```ini
[Service]
Environment="HTTPS_PROXY=http://proxy.internal:3128"
Environment="HTTP_PROXY=http://proxy.internal:3128"
Environment="NO_PROXY=.corp.example.com"
```

cloning an internal repository can fail with `fatal: Authentication failed for 'https://git.corp.example.com/...'` because git never saw `NO_PROXY` and sent the request through the external proxy. Forward the variables:

```json
{ "forwarded_env_vars": ["HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"] }
```

or `SEMAPHORE_FORWARDED_ENV_VARS='["HTTP_PROXY","HTTPS_PROXY","NO_PROXY"]'`.

Notes:
- Always forward `NO_PROXY` with the others, or internal Git servers go through the proxy.
- Many tools read lowercase `http_proxy`, `https_proxy`, `no_proxy`; names are case sensitive on Linux, so list both spellings if the host sets lowercase.
- For TLS-intercepting proxies forward `GIT_SSL_CAINFO`, `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE` instead of disabling verification.
- Docker installs often work because the whole container has the variables, but forward them anyway for identical behaviour.

Verify: re-run the task that clones the repository and confirm the clone succeeds.

## Checked

2026-11-04: checked against the environment variable and configuration pages. Every claim is stated there.

Method: documentation only; no commands were run.
