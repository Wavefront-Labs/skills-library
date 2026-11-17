---
id: computing-software.messaging-and-integration.ntfy.troubleshooting-debug
name: troubleshooting-debug
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, troubleshooting, debug, logs, adb]
level: practitioner
status: docs-checked
description: "Get debug logs from the ntfy server, Android app, web app and iOS app when notifications misbehave."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding out what ntfy is doing

## Server

- `log-level: debug` or `trace` in `server.yml`
- `NTFY_LOG_LEVEL=debug`
- `ntfy serve --debug` or `--trace`
- systemd: `journalctl -u ntfy -f`

## Android app

Settings, "Record logs" stores up to 1,000 entries to copy or upload. Sharing can censor logs (topics and hostnames other than ntfy.sh become fruit names).

Live logs with adb over wireless debugging:

```
adb connect <ip:port>
adb logcat
adb logcat --pid=$(adb shell pidof -s io.heckel.ntfy)
```

## Web app

Logs go to the browser developer console (F12).

## iOS app

No way to get logs yet other than running the app in Xcode.

## Gotchas

- If the page does not help, it points to the contact page for support channels.
- `adb logcat` may need `-s <ip:port>` when several devices are connected.

## Checked

2026-11-04. Confirmed against the ntfy troubleshooting page (server log settings, journalctl, Android Record logs, 1,000 entries, fruit censoring, adb commands, web console, iOS). Removed: the log-level-timing gotcha and the Verify step.
Method: documentation only; no commands were run.
