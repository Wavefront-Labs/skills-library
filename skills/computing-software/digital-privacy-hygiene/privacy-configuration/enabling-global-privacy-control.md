---
id: computing-software.digital-privacy-hygiene.privacy-configuration.enabling-global-privacy-control
name: enabling-global-privacy-control
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, global-privacy-control, gpc, ccpa, opt-out, browser-privacy, privacy-badger]
level: intro
status: docs-checked
description: "Turn on Global Privacy Control in a supporting browser or extension so sites receive an opt-out of sale/sharing that California law requires businesses to honour."
sources:
  - "https://globalprivacycontrol.org/"
  - "https://oag.ca.gov/privacy/ccpa"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling Global Privacy Control

**Goal:** send an opt-out of sale and sharing automatically to every site, instead of clicking "Do Not Sell or Share"
links site by site.

## What it is
- GPC is a proposed technical standard: a browser or extension setting that signals "stop selling or sharing my
  data". Development began at the W3C Privacy Community Group in April 2020; in November 2024 it became a work item of
  the W3C Privacy Working Group, still being standardised.
- Under the CCPA, the California Attorney General says a user-enabled global privacy control such as GPC is an
  acceptable opt-out method for online businesses and must be honoured by covered businesses as a valid request to
  stop sale or sharing. Globalprivacycontrol.org says similar state privacy laws also rely on it. Under GDPR it is
  intended to convey a general request to limit sale or sharing to other controllers (Articles 7 and 21).

## Turn it on
- Brave and the DuckDuckGo browser: on by default.
- Firefox: available in its settings.
- Other browsers: install a GPC extension. The sites list Privacy Badger (EFF), Disconnect, OptMeowt and lockrMail.
- The GPC site lists supported browsers and extensions; check it for mobile options.

## Limits
- It applies per browser and device. Opt out in account settings as well for sites where you are logged in.
- A refusal or failure is reportable: the Attorney General accepts reports about opt-out methods that do not work.
- A signal asks sites to stop selling or sharing; it does not itself block trackers.

## Verify
- [ ] Every browser you use has GPC on or a GPC extension installed.

## Checked
Date: 2026-11-08.
Confirmed against globalprivacycontrol.org (definition, W3C status dates, supported browsers and extensions, default
settings, GDPR intent) and the California Attorney General CCPA FAQ (opt-out via GPC must be honoured, Firefox, Brave,
DuckDuckGo, Privacy Badger, complaint route). Removed: the Sec-GPC header and JavaScript property names, the Sephora
enforcement case, named states other than California, the Firefox menu label, the claim that Chrome, Edge and Safari
have no native toggle, the verification test steps, and the uBlock Origin advice; none are on those pages. The Mozilla
support page was blocked and not read.
Method: documentation only; no commands were run.
