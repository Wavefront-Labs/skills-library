---
id: computing-software.general-digital-literacy.web-browsers.global-privacy-control-and-do-not-track
name: global-privacy-control-and-do-not-track
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-privacy, global-privacy-control, do-not-track, opt-out-signal]
level: intro
status: docs-checked
description: "Turn on Global Privacy Control in Firefox, Brave, DuckDuckGo or an extension, know where US law makes sites honour it, and why Do Not Track is largely ignored."
sources:
  - https://globalprivacycontrol.org/
  - https://globalprivacycontrol.org/faq
  - https://www.w3.org/TR/gpc/
  - https://support.google.com/chrome/answer/2790761
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Global Privacy Control and Do Not Track

## Global Privacy Control (GPC)
- A browser signal, sent as the HTTP header `Sec-GPC: 1`, that communicates a Do Not Sell or Share request under the California Consumer Privacy Act and similar state laws. Under the GDPR its intent is a general request that data controllers limit sale or sharing of your data.
- **Legal weight:** as of 15 January 2025 the GPC project's FAQ says four states (California, Colorado, Connecticut and New Jersey) had issued guidance that GPC must be treated as a legally binding opt-out request, and another eight states' laws entitle consumers to use universal opt-out mechanisms. Check the current state law; this changes.
- It does not block trackers by itself.

## Turn it on
- **Brave and the DuckDuckGo browser:** supported natively and on by default (per the GPC project).
- **Firefox:** available in its settings (the menu path could not be confirmed; search the settings for "privacy").
- **Other browsers:** the GPC project lists extensions that send it, including OptMeowt and Privacy Badger. Whether Chrome, Edge or Safari offer a built-in setting is not covered here.
- Check: visit **globalprivacycontrol.org**, whose page tells you whether your browser sends the signal.

## Do Not Track (DNT)
- Chrome's help says its "Do not track" request is **off by default**, and that most websites and web services, including Google's, do not change their behaviour when they receive it. Chrome does not say which sites respect it.
- Setting in Chrome: More > Settings > Privacy and security > Third-party cookies > **Send a "Do not track" request with your browsing traffic**.

## Complements
- Tracking prevention, third-party cookie blocking, ad personalisation off in your accounts and reject-all on cookie banners.

## Verify
- [ ] globalprivacycontrol.org reports that your main browser sends the signal.

## Checked
2026-10-27. The GPC project's home page and FAQ, the W3C GPC specification (Sec-GPC header) and Chrome Help (Turn Do Not Track on or off) were read. Confirmed the header, the browsers and extensions listed, the January 2025 legal status and Chrome's Do Not Track behaviour and menu path. The Firefox setting label and other browsers' built-in support are not covered because they could not be confirmed. Method: documentation only; no commands were run.
