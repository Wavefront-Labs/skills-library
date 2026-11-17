---
id: computing-software.software-engineering.wails.wails-webview-security-and-context-menu
name: wails-webview-security-and-context-menu
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, context-menu, security, options]
level: practitioner
status: docs-checked
description: "Control the Wails default browser context menu in production, fraudulent-website scanning and panic recovery, and restrict binding origins."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails webview context menu and safety switches

Goal: decide what the webview exposes to users and what Wails recovers from.

## Default context menu

`EnableDefaultContextMenu` (bool) enables the browser context menu in production. By default it is available only in dev and in a `-debug` build (together with the devtools inspector). With the option on, the devtools inspector is still unavailable unless you build with the `-devtools` flag.

When enabled, the menu shows by default only for text contexts (Cut/Copy/Paste). Override per element with the CSS property `--default-contextmenu`:

| Value | Behaviour |
| --- | --- |
| `auto` | default: show only if contentEditable is true, text is selected, or the element is input/textarea |
| `show` | always show |
| `hide` | always hide |

The rule inherits like normal CSS, so nesting works (put it on `body` for the whole page). This filtering only applies in production; dev and debug builds always show the full menu.

Warning from the docs: this filtering is NOT a security measure. Assume the full menu (Download image, Reload, Save webpage) could leak; if that matters, do not enable the default context menu.

## Other switches on `options.App`

- `EnableFraudulentWebsiteDetection` (bool): turns on scanning for malware/phishing. This may send URLs navigated to, and possibly other content, to Apple and Microsoft cloud services.
- `DisablePanicRecovery` (bool): by default Wails recovers from panics during message processing and logs them; set `true` to handle panics yourself.
- `BindingsAllowedOrigins` (string): comma-separated extra origins allowed for JS-to-Go bindings; `*` wildcards work in hostnames, e.g. `"https://*.myapp.com, https://example.com"`.

Related: `computing-software.software-engineering.wails.wails-bindings-options`.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), focusing on EnableDefaultContextMenu (table, inheritance note, production-only note, security warning), EnableFraudulentWebsiteDetection, DisablePanicRecovery and BindingsAllowedOrigins; no includes. All three CSS values, the -debug / -devtools build-flag statements, the Apple and Microsoft cloud-services wording and the wildcard example matched. No claims were trimmed.

Method: documentation only; no commands were run.
