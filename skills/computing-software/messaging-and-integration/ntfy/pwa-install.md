---
id: computing-software.messaging-and-integration.ntfy.pwa-install
name: pwa-install
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, pwa, install, desktop, web-push]
level: intro
status: docs-checked
description: "Install the ntfy web app as a PWA on desktop and mobile, per browser, and what changes for background notifications."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/pwa.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing the ntfy PWA

There is no native desktop app; ntfy is a progressive web app. Installing adds a launcher, standalone window, push notifications and an unread-count badge.

## Steps by browser

- Chrome desktop: click the "install app" icon.
- Safari on macOS (14 Sonoma or higher): Share menu, Add to Dock.
- Chrome on Android: "Add to Home Screen" banner, or "Install app" in the menu.
- Firefox on Android: menu, Install, then Add.
- Safari on iOS (16.4+): Share menu, Add to Home Screen.
- Firefox on Windows or Linux: only through an extension.
- Edge: supported on Windows (the page gives no steps).

## Background notifications

Web push is on by default and cannot be turned off once installed; mute individual topics instead. On desktop the browser or web app must be running (the ntfy tab itself can be closed). On mobile the app need not be open.

## Self-hosted requirement

Web Push must be configured on the server for the PWA to work; see web-push-config.

## Checked

2026-11-04. Confirmed against the ntfy PWA page (supported browsers, install steps per browser, background notifications behaviour). Removed: the Verify step.
Method: documentation only; no commands were run.
