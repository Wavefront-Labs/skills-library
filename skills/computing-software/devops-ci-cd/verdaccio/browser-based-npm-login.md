---
id: computing-software.devops-ci-cd.verdaccio.browser-based-npm-login
name: browser-based-npm-login
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [web-login, browser-login, weblogin-flag, weblogin, login-url, done-url, npm-login-web]
level: advanced
status: docs-checked
description: "Enable the webLogin flag so npm login authenticates through the Verdaccio web UI, the three endpoints, the two-minute session, and the reverse proxy port limitation."
sources:
  - https://verdaccio.org/docs/web-login/
  - https://verdaccio.org/docs/setup-npm/
  - https://verdaccio.org/docs/cli-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
flags:
  webLogin: true
```
Restart. With the flag off, the endpoints are not registered and `npm login` falls back to the terminal prompt.

Endpoints:
| Endpoint | Role |
|---|---|
| `POST /-/v1/login` | npm starts here; gets `loginUrl` and `doneUrl` |
| `POST /-/v1/login_cli/:sessionId` | browser hands its result to the session |
| `GET /-/v1/done/:sessionId` | npm polls until the token is ready |

`doneUrl` answers `202` with `Retry-After: 5` until you sign in. The session expires after two minutes (poll answers 401 session-expired; run `npm login` again). The token is single use.

Gotcha behind a reverse proxy: the URLs are built from the request protocol and hostname plus the port Verdaccio listens on, not the client port. With TLS terminated on 443 and Verdaccio on 4873 the browser is sent to `https://your-registry:4873/...`. Keep public and listening ports the same for this flow.

Client note: the npm setup page says web login is not supported for Verdaccio and recommends `npm login --registry http://localhost:4873 --auth-type=legacy`; Yarn 4 needs `--auth-type=legacy` as well.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Browser-based login, Setup npm and Using a private registry (cli-registry). Confirmed: the webLogin flag, the three endpoints, 202 with Retry-After: 5, the two-minute single-use session, the reverse proxy port limitation, the npm note that web login is unsupported, and Yarn 4 needing --auth-type=legacy. Removed or corrected: the unconfirmed `web.login: false` sentence; the example host now matches the page (your-registry).

Method: documentation only; no commands were run.
