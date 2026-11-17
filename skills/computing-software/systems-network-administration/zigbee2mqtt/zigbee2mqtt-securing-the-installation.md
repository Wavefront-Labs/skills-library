---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-securing-the-installation
name: zigbee2mqtt-securing-the-installation
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, security, hardening, secret-yaml, network-key, mqtt-tls, frontend-auth, file-permissions, dedicated-user]
level: advanced
status: docs-checked
description: "Harden a Zigbee2MQTT installation: unprivileged user, file permissions, secret.yaml, MQTT and frontend exposure, auth, TLS, bind address and replacing the default network key."
sources: ["https://www.zigbee2mqtt.io/guide/installation/14_securing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Securing Zigbee2MQTT

Treat Zigbee2MQTT like router software: it controls a network and is only locally reachable by default. Untrusted access must never be allowed to MQTT, the frontend, or the data directory.

Host:
- Run under a dedicated unprivileged user, not root.
- Restrict the data directory to that user; it holds configuration, network state and device data.
- Keep OS, Node.js, the broker and Zigbee2MQTT updated.

Config files:
- `chmod 600 configuration.yaml` and `chmod 600 secret.yaml`.
- Put MQTT credentials, `network_key` and `auth_token` in `secret.yaml` and reference them with `'!secret.yaml key'`.

MQTT is the main control path (configuration, network, devices). Never expose the broker publicly without authentication, and do not use `reject_unauthorized: false` in production.

Frontend: same API over WebSocket, so full control to anyone who reaches it.
- Set `auth_token` and keep it like a password.
- Enable HTTPS and WSS with `ssl_cert` and `ssl_key`, or terminate TLS at a reverse proxy.
- Bind narrowly: `frontend.host: 127.0.0.1`, or a unix socket path for no network exposure. Check Docker and Home Assistant requirements first.

Zigbee network: traffic is encrypted with a 128-bit network key. If you still use the old default key shown in the docs, change it with `network_key: GENERATE` (requires re-pairing all devices; the onboarding flow can also generate one). PAN ID, extended PAN ID, IEEE and network addresses are identifiers, not security measures.

## Checked

2026-11-03. Confirmed against the Securing the installation page: dedicated user, data directory, updates, chmod 600 on both files, secret.yaml, MQTT and reject_unauthorized cautions, frontend auth_token, HTTPS/WSS, bind address and unix socket, 128-bit key, old default key, GENERATE, re-pairing, PAN IDs and addresses not being security. Removed: the unconfirmed verification line.
Method: documentation only; no commands were run.
