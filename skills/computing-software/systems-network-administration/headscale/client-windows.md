---
id: computing-software.systems-network-administration.headscale.client-windows
name: client-windows
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, windows, login-server, unattended-mode, reset]
level: intro
status: docs-checked
description: "Connect the Tailscale Windows client to Headscale, keep it running with unattended mode, and reset client state when registration keeps failing."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/connect/windows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows clients

Install the official Tailscale Windows client, then in Command Prompt or PowerShell:

```
tailscale login --login-server <YOUR_HEADSCALE_URL>
```

Finish the login in the browser window that opens. Your Headscale instance also serves instructions at `/windows`.

## Keep it running

By default the client runs only while you are logged in. Click the tray icon, select Preferences, enable "Run unattended" and confirm the "Unattended mode" message to keep it running.

## Troubleshooting failed registration

Symptom: Headscale output shows repeated `POST "/machine/..."` messages. With `DEBUG` logging on, look for "Machine registration has expired. Sending a authurl to register".

1. Stop the Tailscale service or the tray client.
2. Delete the Tailscale application data folder, `Tailscale`, under the user's AppData Local folder, and try to connect again.
3. Ensure the Windows node is deleted from Headscale (`headscale nodes list` to find it).
4. Start Tailscale and retry the login.

## Checked

2026-11-04. Confirmed against the Headscale docs page for Windows clients (login command, /windows endpoint, unattended mode, failing-registration reset steps). Removed the generic Gotcha about restoring the log level to `info`, which the page does not state.

Method: documentation only; no commands were run.
