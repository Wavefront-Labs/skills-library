---
id: computing-software.general-digital-literacy.web-browsers.page-will-not-load
name: page-will-not-load
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, page-not-loading, err-connection-refused, this-site-cant-be-reached, err-name-not-resolved]
level: intro
status: docs-checked
description: "Diagnose a web page that won't load from its Chrome error code (name not resolved, timed out, refused, certificate, too many redirects) and fix your side."
sources:
  - https://support.google.com/chrome/answer/95669
  - https://support.google.com/chrome/answer/6098869
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page will not load or shows an error code

**Goal:** tell quickly whether the problem is your connection, your browser or the website.

## First checks (Chrome's order)
1. Check the address for typing mistakes and reload the page.
2. Does the problem affect one site or many? Many sites: check the internet connection (Wi-Fi or ethernet; restart the modem and router, or contact the provider).
3. Update Chrome and restart it.
4. Try an Incognito window; if it works, turn off extensions and then delete browsing data.
5. Check a firewall or antivirus is not blocking the connection.
6. Free memory by closing unused tabs; as a last step, reset Chrome settings.

## Reading Chrome's error codes
| Message | What Chrome's help says |
|---|---|
| `ERR_NAME_NOT_RESOLVED` | The web address does not exist or now has a different IP address |
| `ERR_INTERNET_DISCONNECTED` | The device is not connected to the internet |
| `ERR_CONNECTION_TIMED_OUT` / `ERR_TIMED_OUT` | The page took too long: slow connection or a busy page |
| `ERR_CONNECTION_RESET` | Something interrupted the connection: unstable internet, outdated browser, VPN issue or security software |
| `ERR_NETWORK_CHANGED` | The device changed network while the page loaded |
| `ERR_CONNECTION_REFUSED` | The page did not let Chrome connect, or it is blocked |
| `ERR_CACHE_MISS` | The page needs information you entered earlier to be submitted again |
| `ERR_EMPTY_RESPONSE` | The page sent no data and might be down |
| "Your connection is not private" / `NET::ERR_CERT_...` | See below |
| "Your clock is behind/ahead" / `NET::ERR_CERT_DATE_INVALID` | The device date and time are wrong: correct them |
| "This webpage has a redirect loop" / `ERR_TOO_MANY_REDIRECTS` | Cookies may not be working: delete cookies for that site |

## "Your connection is not private"
Chrome's steps: sign in to the Wi-Fi portal (open an `http://` page such as http://example.com, at a cafe or airport); open the page in Incognito; update the operating system; temporarily turn off antivirus "HTTPS scanning" if that is the cause, and turn it back on afterwards. On a work computer with an HTTPS-inspecting proxy, contact the administrator; Chrome says installing a certificate yourself is usually a security risk. Do not bypass the warning on banking or shopping sites.

## Verify
- [ ] You can say which side the fault is on (your connection, your browser or the site) before asking for help.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Get help with common error messages in Chrome" and "Fix connection and loading errors in Chrome", read in October 2026. Confirmed: the code meanings in the table, the certificate and clock steps, the redirect-loop cookie fix and the order of first checks. Removed as unconfirmed: DNS_PROBE_FINISHED_NXDOMAIN, HTTP 403/404/5xx explanations, the flush-DNS command, outage-checker advice, Ctrl+F5, and the Edge and Firefox wording.
Method: documentation only; no commands were run.
