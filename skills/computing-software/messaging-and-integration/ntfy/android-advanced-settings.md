---
id: computing-software.messaging-and-integration.ntfy.android-advanced-settings
name: android-advanced-settings
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, android, certificates, custom-headers, mutual-tls]
level: advanced
status: docs-checked
description: "Configure ntfy Android custom headers, trusted self-signed certificates, client certificates (mTLS) and log recording."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android advanced settings

## Custom headers (Settings, Advanced, Custom headers)

Sent with every request to a server; useful behind authenticated proxies or tunnels. You cannot add an `Authorization` header for a server where a user is configured, and cannot add a user where a custom `Authorization` header exists.

## Manage certificates (Settings, Advanced, Manage certificates)

- Trusted certificates in PEM format, for self-signed servers.
- Client certificates in PKCS#12 format, for mutual TLS.
- When a server is untrusted, a warning dialog lets you review and trust the certificate.

## Logs

Settings, Advanced, "Record logs" stores up to 1,000 entries you can copy or upload. When sharing, you can censor logs: topics and hostnames (except ntfy.sh) are replaced with fruit names.

For live logs use adb with wireless debugging:

```
adb connect <ip:port>
adb logcat --pid=$(adb shell pidof -s io.heckel.ntfy)
```

## Connection errors

The warning icon in the app bar opens details. Common: connection refused (server down or wrong address), WebSocket not supported (server or proxy), 401/403 (credentials or access), untrusted certificate.

## Language

Settings, General, Language; only languages more than 80% translated are listed.

## Checked

2026-11-04. Confirmed against the ntfy phone page (custom headers, certificates, language, connection errors) and the troubleshooting page (log recording, 1,000 entries, censoring with fruit names, adb commands, wireless debugging). Removed: the Verify step.
Method: documentation only; no commands were run.
