---
id: computing-software.cybersecurity-defensive.dex.dex-example-app-test-login
name: dex-example-app-test-login
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [example-app, testing, login, development]
level: intro
status: docs-checked
description: "Run the bundled example-app against a local Dex to test a login end to end, including the mock and static-password options."
sources:
  - https://dexidp.io/docs/getting-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex ships an example client app, built with `make examples`, for testing and demos. By default it uses the OAuth2 credentials defined in `examples/config-dev.yaml`, so it works against a Dex started with that file.

```bash
./bin/dex serve examples/config-dev.yaml
./bin/example-app
```

When the app starts it queries Dex's discovery endpoint to learn the OAuth2 endpoints. Then:

1. Open `http://localhost:5555/` in a browser.
2. Click login to be redirected to Dex.
3. Choose "Login with Example" for mocked user data, or "Login with Email" to use the static credentials `admin@example.com` and `password`.
4. Approve the app's request.
5. The app shows the resulting token claims.

## Checked

2026-11-08: Read the Dex Getting Started page in full. Confirmed the example client built with make examples, its default credentials from examples/config-dev.yaml, discovery endpoint use, the localhost:5555 login steps and the two login options with admin@example.com. Removed the app flags, redirect URI and groups scope claims, which that page does not state.
Method: documentation only; no commands were run.
