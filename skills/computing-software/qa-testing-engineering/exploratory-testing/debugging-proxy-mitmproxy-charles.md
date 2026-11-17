---
id: computing-software.qa-testing-engineering.exploratory-testing.debugging-proxy-mitmproxy-charles
name: debugging-proxy-mitmproxy-charles
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [mitmproxy, charles-proxy, debugging-proxy, https-interception, bug-investigation, mobile-testing]
level: practitioner
status: docs-checked
description: "Inspect and modify app traffic with a debugging proxy such as mitmproxy: proxy and CA setup for browsers and devices, flow filters, interception and certificate pinning limits."
sources:
  - https://docs.mitmproxy.org/stable/
  - https://docs.mitmproxy.org/stable/concepts-certificates/
  - https://docs.mitmproxy.org/stable/concepts-modes/
  - https://docs.mitmproxy.org/stable/howto-install-system-trusted-ca-android/
  - https://developer.android.com/privacy-and-security/security-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting traffic with a debugging proxy (mitmproxy, Charles)

**Goal:** see exactly what the app sends and receives (especially mobile apps without devtools), and alter responses to test edge cases.

## Setup
- **mitmproxy:** `mitmweb` (browser UI) or `mitmproxy` (terminal). It runs as a regular proxy listening on port 8080 by default. Point the device's proxy settings at the computer, open the magic domain `mitm.it` in the device browser and install the CA certificate for that platform.
- **Charles** is an alternative debugging proxy; follow its own documentation for setup.
- **Android 7 and later:** apps ignore user-provided certificates unless they are configured to use them, and most apps do not opt in. Ask developers for a debug build that trusts user CAs, or install the mitmproxy CA in the system store (see the mitmproxy Android how-to).
- **Certificate pinning** stops mitmproxy intercepting traffic to the pinned domains unless the app is patched or the pinning is disabled in a test build.

## Use
- Filter flows to the API host with a flow filter expression (for example `~d api.example.com`; `~d` matches the domain).
- Inspect request headers, auth tokens, payloads, status codes and timings, and attach them to the bug report.
- **Modify:** mitmproxy's `set intercept` takes a flow filter expression; matching requests are paused so you can modify or discard them before they go on to the server. Scripted changes use mitmproxy addons (see the addons documentation).

## Hygiene
Remove the proxy and CA from devices after testing; never intercept traffic of real users or production accounts without authorisation.

## Verify
The relevant request/response pair is captured and attached, and modified-response tests show how the app handles errors and odd data.

## Checked
2026-11-01. Confirmed from the mitmproxy docs source (concepts/certificates, concepts/modes, overview/getting-started, cli-tutorials intercept, howto Android system CA): `mitm.it`, default port 8080, regular proxy mode, Android 7 user-CA behaviour, certificate pinning limit, `set intercept` with a filter, `~d` filter. Removed: Charles menu paths and ports, iOS trust-settings path, web UI port, the `network_security_config` snippet, HAR/curl export, throttling advice and the addon code sample, none of which could be confirmed from the pages read.
Method: documentation only; no commands were run.
