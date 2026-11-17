---
id: computing-software.devops-ci-cd.semaphore-ui.runner-registration-cli-and-security
name: runner-registration-cli-and-security
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [runner-register, runner-unregister, runner-token, tls, security, semaphore-ui]
level: advanced
status: docs-checked
description: "Register and unregister runners from the CLI and secure the runner connection with HTTPS and a CA file."
sources:
  - https://semaphoreui.com/docs/admin-guide/runners
  - https://semaphoreui.com/docs/faq/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runner registration and connection security

Goal: add or remove runners and keep their traffic safe.

Two ways to register: add the runner in the web UI or API, or use the command line, which needs `runner_registration_token` on the server:

```bash
semaphore runner register --config /path/to/config.json
```

Remove with the UI or:

```bash
semaphore runner unregister --config /path/to/config.json
```

When `semaphore runner setup` asks whether you have a Runner token, answer No before registering from the CLI. The page also shows `echo REGISTRATION_TOKEN | semaphore runner register --stdin-registration-token --config /path/to/config.json`, and says re-running `register` overwrites the token in the configured file.

Security model: a runner authenticates to the server with an opaque bearer token sent in the `X-Runner-Token` header, issued at registration. Store it in a restricted config file or a secret manager.

TLS:
- Use HTTPS between server and runner, especially across networks.
- For a self-signed or internal CA certificate set `runner.connection.server_ca_cert_file` on the runner.
- Do not use `runner.connection.skip_tls_verify` in production.

Troubleshooting: for a runner that prints error 404, the troubleshooting page only links the GitHub discussion titled "Getting 401 error code from Runner"; it gives no further cause.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): admin-guide/runners.md and faq/troubleshooting.md. Confirmed: the two registration routes, the runner_registration_token requirement, the register and unregister commands, the stdin variant, the X-Runner-Token bearer token, the HTTPS advice, runner.connection.server_ca_cert_file and the skip_tls_verify warning, and the troubleshooting entry. Removed: the claim that `semaphore runner --help` lists four subcommands, the claim that 404 or 401 usually means a wrong web_root or stale token (the page says neither), and the appears-in-UI Verify step.
Method: documentation only; no commands were run.
