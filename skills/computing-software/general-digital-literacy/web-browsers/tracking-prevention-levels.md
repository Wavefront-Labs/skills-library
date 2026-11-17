---
id: computing-software.general-digital-literacy.web-browsers.tracking-prevention-levels
name: tracking-prevention-levels
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-privacy, safe-browsing, tracking-prevention, intelligent-tracking-prevention]
level: intro
status: docs-checked
description: "Choose tracking protection levels in Edge, Safari and Chrome, fix sites that break under strict mode, and add per-site exceptions in Edge."
sources:
  - https://support.microsoft.com/en-us/microsoft-edge/learn-about-tracking-prevention-in-microsoft-edge-5ac125e8-9b90-8d59-fa2c-7f2e9a44d869
  - https://support.apple.com/guide/safari/privacy-sfri35610/mac
  - https://support.apple.com/guide/safari/prevent-cross-site-tracking-sfri40732/mac
  - https://support.google.com/chrome/answer/95647
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tracking prevention levels

## Edge: Tracking prevention
Settings and more > Settings > **Privacy, search, and services** > **Tracking prevention**; make sure it is On, then choose:
- **Basic:** blocks potentially harmful trackers but allows most others, including ones that personalise content and ads.
- **Balanced (recommended):** blocks potentially harmful trackers and trackers from sites you have not visited; content and ads will likely be less personalised.
- **Strict:** blocks potentially harmful trackers and most trackers across sites; this blocks the most but could break sites, for example a video not playing or sign-in failing.
- **Exceptions:** Add a site and type its full URL. For one site, select **View site information** at the left of the address bar and turn **Tracking prevention for this site** off; **Trackers** there shows which were blocked.

## Safari (Mac)
Safari > Settings > **Privacy**:
- **Prevent cross-site tracking:** deletes third-party providers' cookies and data unless you visit them directly, blocks Share/Like/Comment button tracking unless you give permission, and presents a simplified system configuration to reduce fingerprinting.
- **Hide IP address from trackers:** "from Trackers only" or "from Trackers and Websites"; the second option requires iCloud Private Relay (iCloud+).
- **Advanced Settings:** advanced tracking and fingerprinting protection. It is on by default in private browsing and can be turned on for all browsing.

## Chrome
Settings > Privacy and security > **Third-party cookies**: **Allow third-party cookies** or **Block third-party cookies**, with a list of sites allowed to use them. They are blocked by default in Incognito. Chrome's help does not describe graded tracking-protection levels.

## When a site breaks
Symptoms: login loop, a blank embedded video or map, a payment page that fails. Turn protection off for that site only (Edge exception, Safari's reload-with-reduced-protection option in private windows, or a Chrome exception), reload, then restore the setting when done.

## Firefox
Not covered here; its support site could not be read.

## Verify
- [ ] The Edge Trackers panel or Safari Privacy Report shows trackers blocked, and your main sites still work.

## Checked
2026-10-27. Microsoft's Edge tracking prevention page, Apple's Safari User Guide (Privacy settings; Prevent cross-site tracking; Browse privately) and Chrome Help (cookies) were read. Confirmed the Edge levels and exceptions, the Safari Privacy options and Chrome's cookie options. Firefox Enhanced Tracking Protection is not covered because it could not be confirmed. Method: documentation only; no commands were run.
