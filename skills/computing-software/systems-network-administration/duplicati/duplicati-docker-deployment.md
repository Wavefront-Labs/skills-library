---
id: computing-software.systems-network-administration.duplicati.duplicati-docker-deployment
name: duplicati-docker-deployment
category: computing-software
field: systems-network-administration
product: duplicati
tags: [docker-image, data-folder, allowed-hostnames, settings-encryption-key, docker-secrets, preload-settings]
level: practitioner
status: docs-checked
description: "Run Duplicati in Docker with the /data volume, the settings encryption key, hostname access and secrets supplied through a preload file or the file secret provider."
sources: ["https://docs.duplicati.com/detailed-descriptions/platform-specific-guides/using-duplicati-from-docker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Duplicati in Docker

The images (DockerHub `duplicati/duplicati`) are minimal and hold only the binaries needed. Configuration and anything that must survive restarts is stored in `/data` inside the container, so mount a volume there (for example `./data:/data`).

Sign-in: either watch the container log for the temporary sign-in URL with a token that expires a few minutes after start, or provide the UI password through configuration. Set the database encryption key so secrets in the Server database are not stored in plain text.

Data folder permissions: from version 2.3.1.0 Duplicati refuses a data folder without exactly the expected permissions. If your mount cannot set them, opt out with `DUPLICATI__ALLOW_INSECURE_DATAFOLDER: "true"`.

Hostname access: the server accepts IP-based requests but rejects requests that use a hostname (a defence against DNS attacks). Allow names with `DUPLICATI__WEBSERVICE_ALLOWED_HOSTNAMES: host1;host2`. The special `*` disables the protection and is not recommended.

Secrets: at minimum supply `SETTINGS_ENCRYPTION_KEY`, and perhaps `DUPLICATI__WEBSERVICE_PASSWORD`, as environment variables. Safer approaches since Duplicati cannot read these from files directly:
- A preload file: a `preload.json` with an `env.server` object holding those two values, mounted as a Docker secret and referenced with `DUPLICATI_PRELOAD_SETTINGS: /run/secrets/preloadsettings`.
- The file secret provider: a `secrets.json` with keys such as `settings-key` and `ui-password`, `DUPLICATI__SECRET_PROVIDER: file-secret:///run/secrets/secretprovider`, and references written as `$$settings-key` in the environment values. Other secret providers (such as a key vault) avoid the file entirely.

## Checked

2026-11-04. Confirmed against the Using Duplicati from Docker page. Nothing removed.

Method: documentation only; no commands were run.
