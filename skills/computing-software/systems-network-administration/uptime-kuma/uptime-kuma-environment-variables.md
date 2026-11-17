---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-environment-variables
name: uptime-kuma-environment-variables
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [uptime-kuma-env, data-dir, ssl-key, ssl-cert, node-extra-ca-certs, notification-proxy, ws-origin-check]
level: practitioner
status: docs-checked
description: "Configure Uptime Kuma through environment variables and server arguments: host, port, data dir, TLS, proxy and self-signed CA."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Environment-Variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma environment variables

Set as container env vars, in a `.env` file at the repo root (non-Docker, since 1.20.0), or as server arguments.

Server:
- `DATA_DIR` / `--data-dir=`: where data is stored.
- `UPTIME_KUMA_HOST` (or `HOST`) / `--host=`, `UPTIME_KUMA_PORT` (or `PORT`) / `--port=`.
- `UPTIME_KUMA_SSL_KEY`, `UPTIME_KUMA_SSL_CERT`, `UPTIME_KUMA_SSL_KEY_PASSPHRASE` (since 1.21.1) for built-in HTTPS.
- `UPTIME_KUMA_CLOUDFLARED_TOKEN` (1.14.0): Cloudflare Tunnel token.
- `UPTIME_KUMA_DISABLE_FRAME_SAMEORIGIN`: by default Uptime Kuma refuses iframes from other origins (anti-phishing); setting this true allows other pages to embed it.
- `UPTIME_KUMA_WS_ORIGIN_CHECK`: websocket ORIGIN header check against the server hostname; set to `bypass` to disable it (default `cors-like`).
- `UPTIME_KUMA_ALLOW_ALL_CHROME_EXEC` (1.23.0): allow any executable as Chromium.
- `UPTIME_KUMA_SQLITE_SINGLE_CONNECTION` (2.3.2): set `false` for multiple connections, with the risk of `SQLITE_BUSY: database is locked`.
- `NODE_EXTRA_CA_CERTS=/cert/path/CAcert.pem` to trust self-signed CAs; `NODE_TLS_REJECT_UNAUTHORIZED` ignores all TLS errors; `NODE_OPTIONS=--insecure-http-parser` for `Invalid header value char` errors behind a WAF.
- `NOTIFICATION_PROXY` (2.0.0): full proxy URL for sending notifications, e.g. `http://proxy.example.com:8080`.
- `UPTIME_KUMA_DISABLE_LEAK_PWD_CHECK` (3.0.0).

Logging and development: `UPTIME_KUMA_LOG_FORMAT=json` (2.2.0), `UPTIME_KUMA_HIDE_LOG` (e.g. `debug_monitor,info_monitor`), `UPTIME_KUMA_LOG_RESPONSE_BODY_MONITOR_ID`, `SQL_LOG=1`, `NODE_ENV`.

Variables marked with a version need at least that release. For a MariaDB backend see uptime-kuma-mariadb-database-backend.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Environment Variables page (names, server arguments, versions, defaults, .env file since 1.20.0, proxy and CA variables). Removed: Unsupported clickjacking and proxy-rewrite advice, the (avoid) opinion, and the generic verify line.

Method: documentation only; no commands were run.
