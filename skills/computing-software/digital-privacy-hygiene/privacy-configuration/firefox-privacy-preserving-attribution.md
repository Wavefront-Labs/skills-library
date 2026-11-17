---
id: computing-software.digital-privacy-hygiene.privacy-configuration.firefox-privacy-preserving-attribution
name: firefox-privacy-preserving-attribution
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, privacy-preserving-attribution, firefox, ad-measurement, tracking]
level: practitioner
status: draft
description: "Understand Firefox's privacy-preserving ad measurement (PPA), decide whether to keep it on, and find the setting on desktop."
sources:
  - "https://support.mozilla.org/en-US/kb/privacy-preserving-attribution"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Firefox privacy-preserving attribution

**Goal:** know what this Firefox setting does and switch it off if you don't want to take part.

## What it is
Firefox 128 (July 2024) added **privacy-preserving attribution (PPA)**, an experimental ad measurement API. Sites can
ask Firefox to record that an ad was seen and later whether a conversion (a purchase) happened. Firefox sends
encrypted, aggregated reports via a multi-party computation service (Divvi Up) so the advertiser learns totals, not
which individual saw or bought. Mozilla shipped it **on by default** in a limited trial, which drew criticism.

## Turn it off
Settings > **Privacy & Security** > Website Advertising Preferences > uncheck **Allow websites to perform
privacy-preserving ad measurement**.
Or `about:config` > `dom.private-attribution.submission.enabled = false`.

## Should you?
- On: you help test an alternative to cross-site tracking; Mozilla says no personal data leaves Firefox in a linkable
  form.
- Off: you don't want any ad measurement, or prefer explicit opt-in. No site breakage results from turning it off.

## Related settings
Enhanced Tracking Protection (Strict), Global Privacy Control, and disabling Telemetry/Studies in the same settings
page.
