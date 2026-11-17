---
id: computing-software.it-support-helpdesk.desktop-support.browser-troubleshooting-edge-chrome
name: browser-troubleshooting-edge-chrome
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, browser-troubleshooting, microsoft-edge, google-chrome, browser-cache, extensions, certificate-errors, edge-policy, chrome-policy, browser-profile, comptia-a-plus]
level: practitioner
status: draft
description: "Fix Edge and Chrome problems fast: cache and cookie clears per site, extension isolation, new profile tests, certificate warnings, policy conflicts (edge://policy) and sync issues."
sources:
  - "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-policies"
  - "https://support.google.com/chrome/answer/2765944"
  - "https://support.google.com/chrome/a/answer/9037717"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# browser-troubleshooting-edge-chrome

Goal: decide in five minutes whether a "website doesn't work" ticket is the
site, the network, the profile, an extension or policy.

## Five-minute isolation
1. **InPrivate / Incognito** (Ctrl+Shift+N): works there → cache, cookies or
   an extension (extensions are off in private mode by default).
2. **Other browser** on the same PC: fails too → network/proxy/DNS/site.
3. **Other PC/user**: works → this profile.
4. Site status for others in the org → if all fail, it's the site or proxy.

## Fix by cause
- **Cache/cookies for one site**: padlock → Site permissions / Cookies and site
  data → delete for that site only. Full clear (Ctrl+Shift+Del) signs the
  user out of everything — warn them.
- **Extension**: `edge://extensions` / `chrome://extensions`, disable all,
  re-enable one at a time. Malicious "PDF converter"/"coupon" extensions →
  remove and add to the blocklist policy.
- **Corrupt profile**: create a new browser profile; if it works, migrate
  favourites via sync or export. Profile path:
  `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default` (Chrome: `Google\Chrome\User Data`).
- **Hardware acceleration** (blank/black pages, video flicker):
  Settings → System → turn off "Use graphics acceleration".

## Certificates
`NET::ERR_CERT_AUTHORITY_INVALID` on every site with your company as issuer
= TLS inspection root CA missing; on one site = site's cert problem (don't
tell users to click through). `ERR_CERT_DATE_INVALID` everywhere = system
clock wrong. Click the warning → certificate details → read issuer and
validity.

## Policies
`edge://policy` / `chrome://policy` shows every applied policy and its
source (GPO, Intune, cloud). Users can't change a setting that shows
"Managed by your organisation" — fix in policy. `edge://management` shows the
management state. Reload policies on that page after a gpupdate.

## Other internals
`edge://net-internals/#dns` → clear host cache; `#sockets` → flush;
`edge://settings/help` → version (old builds = update blocked by policy
or by missing admin rights).

## Gotchas
- Sync conflicts can restore a broken extension to a new profile — turn off
  sync before testing.
- Clearing "Cached images and files" alone fixes most stale-page issues and
  keeps sign-ins.

## Verify
The user's original action works in their normal (non-private) window after
a browser restart, and `edge://policy` shows no errors.
