---
id: computing-software.cybersecurity-defensive.authelia.environment-variables-and-secret-files
name: environment-variables-and-secret-files
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, environment-variables, secrets, file-suffix, configuration-layers, kubernetes-secrets]
level: practitioner
status: docs-checked
description: "Configure Authelia through AUTHELIA_ environment variables and _FILE secret variables, including the mapping rule and which list sections cannot use them."
sources:
  - https://www.authelia.com/configuration/methods/environment/
  - https://www.authelia.com/configuration/methods/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environment variables apply after configuration files, so they override the files.

Rules:

- Every variable starting with `AUTHELIA_` is treated as configuration. A stray variable with that prefix will likely cause an error or misconfiguration.
- Keys map by name, with indentation replaced by underscores: `log.level` becomes `AUTHELIA_LOG_LEVEL=info` and `server.buffers.read` becomes `AUTHELIA_SERVER_BUFFERS_READ=4096`.
- Sections that are lists of objects cannot be set this way: access control `rules`, OpenID Connect `clients`, session `cookies`, and server `endpoints.authz`.
- On Kubernetes, the environment page points to a separate "Enable Service Links" note for specific requirements (not read here); the pod example on the files page sets `enableServiceLinks: false`, which suits the `AUTHELIA_` prefix rule because service links inject extra variables.

Secrets use the same name with a `_FILE` suffix, where the value is a path to a file Authelia can read:

```bash
AUTHELIA_SESSION_SECRET_FILE=/secrets/SESSION_SECRET
AUTHELIA_STORAGE_POSTGRES_PASSWORD_FILE=/secrets/STORAGE_PASSWORD
AUTHELIA_STORAGE_ENCRYPTION_KEY_FILE=/secrets/STORAGE_ENCRYPTION_KEY
```

A key is eligible when its name ends in `key`, `secret`, `password`, `token` or `certificate_chain`. Trailing newlines are removed from the file content.

Authelia will not start if a secret is defined through `_FILE` and also through any other method (for example the files method or the plain `AUTHELIA_..._SECRET` variable). Define each secret in exactly one place. Since 4.30.0 a secret can technically be set in a plain environment variable without `_FILE`, which the documentation strongly discourages. Only keys with the eligible suffixes load a file; any other key set through the environment takes the variable's value directly. If secrets must stay in the configuration file, its permissions should be 0600 or similar.

Check: start the container and confirm Authelia starts without a duplicate-secret startup error.

## Checked

2026-11-08. Read in full: configuration/methods/environment, secrets, files. Softened the Kubernetes service links claim to what the pages say; added plain-env secret caveat.

Method: documentation only; no commands were run.
