---
id: computing-software.general-digital-literacy.internet-navigation.online-privacy-and-tracking
name: online-privacy-and-tracking
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, online-privacy, tracking, cookies, third-party-cookies, vpn, ad-blockers, data-brokers, opt-out, do-not-track, tracking-protection, fingerprinting, incognito-limits]
level: intro
status: docs-checked
description: "Reduce everyday web tracking with cookie controls, tracking-protection settings and VPN basics, without overclaiming what any of them actually hides."
sources:
  - https://support.google.com/chrome/answer/95647
  - https://support.google.com/chrome/answer/95464
  - https://support.microsoft.com/en-us/microsoft-edge/learn-about-tracking-prevention-in-microsoft-edge-5ac125e8-9b90-8d59-fa2c-7f2e9a44d869
  - https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop
  - https://support.apple.com/guide/safari/prevent-cross-site-tracking-sfri40732/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online privacy and tracking — reduce it realistically, don't oversell it to yourself

**Goal:** cut down how much of your browsing gets tracked and profiled using the free
controls already in the browser, understand what a VPN does and doesn't do, and know
the honest limits of all of it — overclaiming privacy tools is how people end up with a
false sense of safety.

## 1. What's actually tracking you
- **First-party cookies** (a site remembering you're logged in) are mostly harmless and
  often necessary.
- **Third-party cookies and tracking pixels** let an ad network see you across many
  unrelated sites, building a profile of your browsing. This is the main target of
  "tracking protection."
- **Fingerprinting** (identifying a device by its exact combination of screen size,
  fonts, browser version, etc., without using cookies at all) works even with cookies
  fully blocked — this is why blocking cookies alone doesn't make you untraceable.

## 2. Built-in browser controls (free, already there)
- Chrome: More › Settings › Privacy and security › **Third-party cookies** › Block third-party cookies (they are blocked by default in Incognito). Sites may not work as expected if cookies are blocked; you can allow a specific site.
- Edge: Settings and more › Settings › Privacy, search, and services › **Tracking prevention** (Basic, Balanced (recommended) or Strict).
- Firefox: the shield icon next to the address bar opens the protection settings; under Privacy & Security › Enhanced Tracking Protection › Advanced settings choose **Strict**. If a site breaks, toggle protection off for that site from the shield icon.
- Safari: **Prevent Cross-Site Tracking** is the default on iPhone (Settings › Apps › Safari) and is a checkbox under Safari › Settings › Privacy on Mac.
- These reduce cross-site profiling noticeably but don't defeat fingerprinting or a
  site's own first-party tracking of your account activity.

## 3. Private/incognito windows — what they really do
Already covered operationally in browser-essentials; the privacy-specific point: a
private window stops that browser from **keeping** history and site data after you
close it. Chrome's own help says it does not make you invisible: sites you visit, and organisations that manage your network (school, employer, internet provider), may still see your activity, and signing in to a site identifies you to it.

## 4. VPNs — what they do and don't do
- A VPN routes your traffic through the VPN provider's server, hiding your browsing
  from your **internet provider and local network** (useful on public Wi-Fi, or to avoid
  an ISP logging/selling browsing data where that's a concern) and changes the
  **location** sites see you connecting from.
- A VPN does **not** hide your identity from sites you log into, does not stop
  fingerprinting, and shifts the "who can see my traffic" question to the **VPN
  provider itself** — you're trusting them instead of your ISP. Choose a provider with a
  genuinely audited no-logs policy if this matters, not just one that claims it in
  marketing copy.
- For most everyday users, a VPN is most useful specifically on **public Wi-Fi**
  (cafés, airports) where the local network itself is the risk, not as a general
  anonymity tool for everyday browsing.

## 5. Reducing exposure beyond the browser
- **Data broker opt-outs**: sites that compile and sell personal information may offer an opt-out form; this is manual, per-broker work with no single switch, so treat it as ongoing maintenance.
- **Ad blockers** such as uBlock Origin (a blocker for Chromium and Firefox) can reduce ads and some tracking; install from the browser's official extension store (see browser-essentials for vetting extensions).
- Review **app permissions** on your phone (location, microphone, contacts) periodically
  — mobile apps are a bigger everyday tracking surface for most people than desktop
  browsing.

## Verify
- [ ] Third-party cookie blocking / tracking protection is turned on in your main
      browser.
- [ ] You can state what a private window does and does not hide, without overclaiming it.
- [ ] If you use a VPN, you know specifically what risk it addresses for you (public
      Wi-Fi, location) rather than treating it as general invisibility.
- [ ] An ad blocker from the browser's official store is installed, if you want one.

## Checked

Checked 2026-10-27 against Chrome Help (cookies; Incognito), Microsoft Support (Edge tracking prevention), Mozilla Support (Enhanced Tracking Protection) and Apple's Safari guide (prevent cross-site tracking). Confirmed: Chrome Third-party cookies path and Incognito default, Edge Tracking prevention levels, Firefox shield and Strict setting with per-site exception, Safari default and paths, and Chrome's statement that Incognito does not hide activity from sites, networks or providers.

Method: documentation only; no commands were run.
