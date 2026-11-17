---
id: computing-software.systems-network-administration.duplicati.duplicati-server-access-and-security
name: duplicati-server-access-and-security
category: computing-software
field: systems-network-administration
product: duplicati
tags: [duplicati-server, webservice-password, signin-token, db-encryption-key, webservice-interface, https-configuration, pre-auth-tokens]
level: advanced
status: docs-checked
description: "Secure and expose the Duplicati Server with its password, sign-in tokens, field encryption key, listening interface, port and allowed hostnames."
sources: ["https://docs.duplicati.com/duplicati-programs/server", "https://docs.duplicati.com/detailed-descriptions/configuration-and-management/duplicati-access-password"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Duplicati Server access and security options

The Server is the long-running primary process that stores backup configurations, starts scheduled backups and hosts the web UI and API. It runs the same code as the CLI but also tracks each backup's local database via its server database. The TrayIcon usually hosts it on desktops.

Password: the first server start asks for a password in the UI; with the TrayIcon this is skipped because the TrayIcon signs you in with a short-term token over a secure in-process channel, and the random default password is preferred since it cannot leak. If you run headless, the log emits a temporary sign-in URL (find it with `journalctl --unit=duplicati` on systemd, Event Viewer on Windows or the Console app on macOS; pipe the output to see the whole token). Set or reset the password with `--webservice-password=<new>`; it is stored in the server database. `--webservice-reset-jwt-config=true` creates new token signing keys and immediately invalidates tokens, `--webservice-disable-signin-tokens=true` disables sign-in tokens, `--webservice-password-init=<password>` only sets it if none exists then exits (safe on every install), and `--webservice-token-duration` changes the refresh token lifetime (capped at 30 days).

Encryption: `--settings-encryption-key=<key>` encrypts sensitive fields in the server database. Without a key the server warns; if fields are already encrypted it refuses to start without it. `--disable-db-encryption=true` decrypts, and `--require-db-encryption-key` prevents starting without a key (exclusive with the former).

Network access: by default only the loopback interface is served on port `8200`, and only IP-based hostnames are accepted. `--webservice-interface=any` (or a specific address), `--webservice-port=<n>`, `--webservice-allowed-hostnames=host1;host2`, `--webservice-cors-origins=<full URLs>` and `--webservice-pre-auth-tokens=<tokens, at least 10 characters each>` for an authenticating proxy extend this. `--configure-https` generates a local CA and server certificate.

## Checked

2026-11-04. Confirmed against the Server page and Duplicati access password page. Nothing removed; all options, defaults and the 30 day cap confirmed.

Method: documentation only; no commands were run.
