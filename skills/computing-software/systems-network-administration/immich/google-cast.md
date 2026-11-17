---
id: computing-software.systems-network-administration.immich.google-cast
name: google-cast
category: computing-software
field: systems-network-administration
product: immich
tags: [chromecast, cast, https, dns, nest-hub]
level: intro
status: docs-checked
description: "Enable experimental Google Cast in Immich's web client and meet its prerequisites: HTTPS, public DNS reachable from Google, and compatible video formats."
sources:
  - https://docs.immich.app/features/casting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: cast photos and videos from Immich to a Chromecast or Nest Hub.

Status: experimental, with several limitations. It is supported only by the web client; Android and iOS support is planned.

Enable it per user: Account Settings, Features, Cast, Google Cast. It is off by default because the web UI loads Google-provided scripts from Google servers when the page loads, which is a privacy concern for some people, so it is opt-in.

Prerequisites:

1. The instance must be accessed over HTTPS, otherwise the casting menu does not show.
2. The instance must be publicly accessible over HTTPS, and a DNS record for the server must be resolvable by Google's DNS servers (`8.8.8.8` and `8.8.4.4`). Internal-only hostnames will not work.
3. Videos must be in a format compatible with Google Cast; see Google's Cast media documentation.

If the cast menu is missing, the first things to confirm are that you are on the HTTPS URL and that the setting above is switched on for your account.

Because the instance must be public, put it behind a properly configured reverse proxy with TLS; see the reverse proxy and remote access skills.

## Checked

2026-11-09. Confirmed against the Chromecast support page: experimental and web-client only, opt-in setting path, the privacy reason, the three prerequisites including Google's DNS servers 8.8.8.8 and 8.8.4.4. The advice about missing menu and reverse proxy is practice guidance, not from the page.
Method: documentation only; no commands were run.
