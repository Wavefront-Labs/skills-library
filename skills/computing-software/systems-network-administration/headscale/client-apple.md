---
id: computing-software.systems-network-administration.headscale.client-apple
name: client-apple
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, ios, macos, tvos, custom-coordination-server]
level: intro
status: docs-checked
description: "Point Tailscale on iOS, macOS and tvOS at a Headscale server, including the tvOS rule to set the server URL before signing in."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/usage/connect/apple.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/registration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apple clients

Your Headscale instance serves these instructions at `/apple`.

## iOS

Install Tailscale from the App Store. Click the account icon in the top-right corner, select *Log in*, tap the top-right options menu button, choose *Use custom coordination server*, enter your Headscale URL, then log in.

## macOS

Choose one of the Tailscale macOS client variants, install it, then either:

```
tailscale login --login-server <YOUR_HEADSCALE_URL>
```

or Option-click the Tailscale menu icon, hover over the Debug menu, choose *Add Account...* under *Custom Login Server*, enter the URL, press *Add Account* and follow the login procedure in the browser.

## tvOS

1. Install the Tailscale tvOS client, open it, click *Install VPN configuration* and confirm with *Allow*, but do not sign in yet.
2. In tvOS Settings go to Apps, Tailscale, and under *ALTERNATE COORDINATION SERVER URL* select *URL* and enter your Headscale URL.
3. Return to the Home screen, open Tailscale, scan the QR code and follow the login procedure.

The docs warn: do not sign in to the Tailscale app before the Headscale URL is configured.

## Verify

After login, approve the node if web authentication is used (`headscale auth register --user <USER> --auth-id <AUTH_ID>`) and check `headscale nodes list`.

## Checked

2026-11-04. Confirmed against the Headscale docs pages for Apple clients (iOS, macOS, tvOS steps, /apple endpoint, tvOS warning) and registration methods (auth register command, nodes list). Corrected menu wording to match the page.

Method: documentation only; no commands were run.
