---
id: computing-software.systems-network-administration.headscale.client-android
name: client-android
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, android, alternate-server, auth-key, f-droid]
level: intro
status: docs-checked
description: "Connect the official Tailscale Android app to Headscale using an alternate server URL, with web authentication or a pre-authenticated key."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/connect/android.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android clients

Use the official Tailscale Android app, installed from the Google Play Store or F-Droid.

## Web authentication

1. In the app's account settings, choose the option to use an alternate server.
2. Enter your Headscale server URL and follow the login steps.
3. The client connects automatically once Headscale completes the node registration.

Until node registration completes on Headscale, nothing is visible in the server logs. Approve with:

```
headscale auth register --user <USER> --auth-id <AUTH_ID>
```

## Pre-authenticated key

1. Create a key: `headscale preauthkeys create --user <USER>`
2. Set the alternate server URL as above.
3. Choose the option to use an auth key and enter the key.
4. If needed, tap Log in on the main screen.

## Gotcha

The server certificate should contain the full chain, else some clients, like the Tailscale Android client, reject it (tls-own-certificate).

## Checked

2026-11-04. Confirmed against the Headscale docs pages for Android clients, registration methods (auth register and preauthkeys create commands) and TLS (full-chain note). Removed the wording that implied log output is never expected beyond what the page says.

Method: documentation only; no commands were run.
