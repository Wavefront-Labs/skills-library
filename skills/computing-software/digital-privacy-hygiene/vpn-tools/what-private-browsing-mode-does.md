---
id: computing-software.digital-privacy-hygiene.vpn-tools.what-private-browsing-mode-does
name: what-private-browsing-mode-does
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, private-browsing-mode, privacy-browser, cookie-management]
level: practitioner
status: draft
description: "Explain what incognito and private browsing do and don't protect against, and pick the right tool when the real need is anonymity or account separation."
sources:
  - "https://support.google.com/chrome/answer/9845881"
  - "https://support.mozilla.org/kb/common-myths-about-private-browsing"
  - "https://ssd.eff.org/module/what-fingerprinting"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# What private browsing mode does

**Goal:** use incognito/private windows for what they're good at and stop relying on them for things they don't do.

## It does
- Not save history, cookies, site data or form entries **on this device** after you close all private windows.
- Start with no cookies, so you're logged out and sites treat you as a new visitor (until you log in).
- In Firefox/Safari/Brave: stronger tracking protection by default in private mode.

## It doesn't
| Myth | Reality |
|---|---|
| Hides activity from ISP/employer/school | They still see domains (and more on managed devices) |
| Hides your IP | Sites see your IP; use a VPN/Tor |
| Anonymous on sites you log into | Logging in identifies you |
| Removes downloads and bookmarks | Files and bookmarks you save stay |
| Blocks fingerprinting | Mostly no (Tor/Mullvad Browser do) |
| Protects from malware or keyloggers | No |
| Disables extensions | Some extensions run if allowed in private |

## Good uses
- Using a shared or borrowed computer briefly.
- Logging into a second account side by side.
- Checking how a page looks logged out / without your cookies.
- Gift shopping on a shared family computer.

## Better tools
- Persistent separation: browser profiles or Firefox containers.
- Anonymity: Tor Browser.
- Hide IP: VPN or Private Relay.

## Gotchas
- Google settled a class action (2024) over data collection in incognito; Chrome's incognito screen now says sites
  and Google may still collect data.
- DNS cache and OS-level logs may retain visited domains until reboot.
