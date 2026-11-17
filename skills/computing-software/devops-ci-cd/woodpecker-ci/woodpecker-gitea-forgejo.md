---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-gitea-forgejo
name: woodpecker-gitea-forgejo
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [gitea, forgejo, webhook-allowlist]
level: practitioner
status: docs-checked
description: "Connect Woodpecker to Gitea or Forgejo, including same-host networking and webhook settings."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/forges/gitea", "https://woodpecker-ci.org/docs/administration/configuration/forges/forgejo"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker with Gitea and Forgejo

Gitea:

```ini
WOODPECKER_GITEA=true
WOODPECKER_GITEA_URL=YOUR_GITEA_URL
WOODPECKER_GITEA_CLIENT=YOUR_GITEA_CLIENT
WOODPECKER_GITEA_SECRET=YOUR_GITEA_CLIENT_SECRET
```

Forgejo uses `WOODPECKER_FORGEJO`, `WOODPECKER_FORGEJO_URL`, `WOODPECKER_FORGEJO_CLIENT` and `WOODPECKER_FORGEJO_SECRET`. Defaults for the URL are `https://try.gitea.io` and `https://next.forgejo.org`, so always set it.

Register an OAuth application, either per user at `https://gitea.<host>/user/settings/` or system-wide as admin at `https://gitea.<host>/admin/settings/applications`. The callback URL must match scheme and hostname exactly, with path `https://<host>/authorize`.

Same host in containers: the agent clones using the URL the forge reports. Put the agent on the forge's Docker network (`WOODPECKER_BACKEND_DOCKER_NETWORK=gitea`), or go through the `docker0` gateway (usually 172.17.0.1).

Local connections: when Woodpecker runs on the same host as Gitea (since v1.16), webhooks fail unless `app.ini` has:

```ini
[webhook]
ALLOWED_HOST_LIST=external,loopback
```

The API page size must allow a fixed length of 50. The default maximum is 50; a lower value breaks some features.

`WOODPECKER_GITEA_SKIP_VERIFY` (false) skips SSL verification; client and secret have `_FILE` variants.

Register the application with the exact callback URL, because a scheme or host mismatch breaks login. Restart the forge after editing app.ini so webhook settings apply.

## Checked

2026-11-03. Read the Woodpecker Gitea and Forgejo forge pages and confirmed WOODPECKER_GITEA_* and WOODPECKER_FORGEJO_* variables, default URLs, OAuth callback path /authorize, system-wide application path, same-host Docker network and docker0 gateway, ALLOWED_HOST_LIST=external,loopback, page length 50, SKIP_VERIFY and _FILE variants. Nothing removed. 

Method: documentation only; no commands were run.
