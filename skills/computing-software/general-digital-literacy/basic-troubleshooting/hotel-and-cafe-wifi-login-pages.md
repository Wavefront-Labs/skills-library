---
id: computing-software.general-digital-literacy.basic-troubleshooting.hotel-and-cafe-wifi-login-pages
name: hotel-and-cafe-wifi-login-pages
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, wifi, connectivity, captive-portal, public-wifi, hotel-wifi, login-page-not-showing, neverssl, public-wifi-safety]
level: intro
status: draft
description: "Get past public Wi-Fi sign-in (captive portal) pages that don't appear, and use hotel, café and airport Wi-Fi safely."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - http://neverssl.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hotel and café Wi-Fi login pages

**Goal:** get online on public Wi-Fi and stay safe while there.

## The sign-in page doesn't appear
Public networks show a "captive portal" (accept terms, room number, voucher) before allowing internet.
1. Wait a few seconds after connecting; Windows shows "Action needed / Open browser and connect",
   Mac/iPhone pop up a mini browser.
2. If not, open a browser and go to an **http** (not https) address: `http://neverssl.com` or
   `http://example.com`. The network redirects you to its login page.
3. Still nothing: turn off **VPN** and custom DNS (e.g. 1.1.1.1 / secure DNS in the browser) until
   you've logged in; they block the redirect.
4. Forget the network and rejoin; try the router's address shown on the hotel card.

## Staying safe
- Make sure the network name is the venue's real one (ask staff); attackers create look-alikes.
- Sites with **https** (padlock) are encrypted end to end; the Wi-Fi owner can still see which sites
  you visit. Avoid entering passwords on any site that shows a certificate warning.
- Set the network as **Public** (Windows: network properties › Network profile type: Public) so file
  sharing is off.
- For banking or work, use your phone's hotspot or a trusted VPN after logging in.

## Gotchas
- Sessions often expire (every 24 h or at midnight); repeat the login when pages stop loading.
- Certificate errors on every site right after connecting = you're being redirected to the portal.

## Verify
- [ ] After login, an https site loads without warnings.
