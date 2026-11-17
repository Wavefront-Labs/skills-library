---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-github-forge
name: woodpecker-github-forge
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [github, oauth-app, forge-config]
level: practitioner
status: docs-checked
description: "Connect Woodpecker to GitHub or GitHub Enterprise with an OAuth app."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/forges/github"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker with GitHub

Built-in support covers GitHub and GitHub Enterprise. Set on the server:

```ini
WOODPECKER_GITHUB=true
WOODPECKER_GITHUB_CLIENT=YOUR_GITHUB_CLIENT_ID
WOODPECKER_GITHUB_SECRET=YOUR_GITHUB_CLIENT_SECRET
```

Create an OAuth2 app in GitHub: Settings, Developer Settings, then the OAuth app creation page. Do not use a GitHub App: it does not work correctly because user access tokens are not refreshed automatically.

App settings:

- Homepage URL: your Woodpecker instance URL.
- Callback URL: `https://<your-woodpecker-instance>/authorize`.

Generate a client secret after creation and use it as `WOODPECKER_GITHUB_SECRET`.

Other options:

- `WOODPECKER_GITHUB_URL` (default `https://github.com`) for GitHub Enterprise.
- `WOODPECKER_GITHUB_SKIP_VERIFY` (default false) skips SSL verification.
- `WOODPECKER_GITHUB_PUBLIC_ONLY` (default false) requests a token that can manage only public repositories.
- `WOODPECKER_GITHUB_MERGE_REF` (default true).
- `WOODPECKER_GITHUB_CLIENT_FILE` and `WOODPECKER_GITHUB_SECRET_FILE` read credentials from files.

GitHub is the only forge whose webhooks can trigger the `deployment` event.

After creating the app, copy the client ID to the client variable and keep the secret out of version control, using the file variants where possible. Set the homepage and callback to the exact public host so the login redirect succeeds.

## Checked

2026-11-03. Read the Woodpecker GitHub forge page and confirmed the WOODPECKER_GITHUB_* variables and registration steps. Nothing removed. 

Method: documentation only; no commands were run.
