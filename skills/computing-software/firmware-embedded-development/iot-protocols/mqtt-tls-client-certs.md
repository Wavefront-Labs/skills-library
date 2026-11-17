---
id: computing-software.firmware-embedded-development.iot-protocols.mqtt-tls-client-certs
name: mqtt-tls-client-certs
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mqtt-tls-client-certs, mqtt-security, mqtt, tls, client-certificate, mosquitto, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT TLS and client certificates: Secure MQTT with TLS 1.2 or 1.3 and per-device certificates."
sources:
  - https://mosquitto.org/man/mosquitto-tls-7.html
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT TLS and client certificates

**Goal:** Secure MQTT with TLS 1.2 or 1.3 and per-device certificates.

## Steps
1. Add a listener (for example `listener 8883`) with cafile, certfile and keyfile; cafile holds the CA certificates trusted for client certificates
2. Set require_certificate true so clients must present a valid certificate, and use_identity_as_username true to take the certificate CN as username (password_file is then not used on that listener); use_subject_as_username takes the full subject instead
3. tls_version is the minimum version: tlsv1.3 or tlsv1.2, and the default allows both
4. When creating the server certificate enter the broker hostname or domain as the CN; use different subject parameters for the CA, server and each client, or the broker and clients cannot tell them apart
5. mosquitto-tls(7) lists the openssl commands: CA with `openssl req -new -x509 ... -extensions v3_ca`, then a key, CSR and `openssl x509 -req` signing per server or client
6. certfile and keyfile are reloaded on SIGHUP, so renewed certificates load without restart; crlfile revokes client certificates

## Gotcha
Certificates carry validity dates and the broker checks client certificate dates; a device with no real-time clock may present a clock that fails this. The disable_client_cert_date_checks option exists to relax it but weakens security, so prefer setting the device clock before connecting.

## Verify
- [ ] `openssl s_client -connect host:8883` shows the chain
- [ ] Cert-less client rejected
- [ ] Expired cert rejected

## Checked

2026-11-03. Confirmed in the mosquitto.conf(5) and mosquitto-tls(7) man pages: cafile, certfile, keyfile, require_certificate, use_identity_as_username, use_subject_as_username, tls_version (minimum, tlsv1.3 and tlsv1.2), crlfile, disable_client_cert_date_checks, SIGHUP reload of certfile and keyfile, CN note and distinct subject note, and the openssl signing commands. Removed: SNI advice, "keep the CA key offline", and the client-side hostname check statement (not covered by these pages).
Method: documentation only; no commands were run.
