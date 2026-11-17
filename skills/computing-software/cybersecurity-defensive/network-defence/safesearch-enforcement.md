---
id: computing-software.cybersecurity-defensive.network-defence.safesearch-enforcement
name: safesearch-enforcement
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [safesearch-enforcement, safesearch, dns-cname-enforcement, web-filtering, content-filtering]
level: practitioner
status: docs-checked
description: "Enforce Google and DuckDuckGo SafeSearch for a network or managed device with DNS CNAME mapping or a hosts-file entry, and verify the lock."
sources: ["https://support.google.com/websearch/answer/186669", "https://help.duckduckgo.com/duckduckgo-help-pages/features/safe-search/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SafeSearch enforcement

Common in schools, libraries and some workplaces (filtering obligations). Browser settings can be
changed by users; enforce at the network or on managed devices.

## Google
Google's "SafeSearch VIP" is a virtual IP that serves SafeSearch results for Google Search, image search and
video search, over HTTPS.
- **Network**: update your DNS so the entry for `www.google.com` (and every Google country or region domain
  your users may use, for example `www.google.co.uk`) is a CNAME for `forcesafesearch.google.com`. This
  applies to all browsers and devices on the network and cannot be undone at the browser level.
- **Single managed PC, Mac or Linux device**: `ping forcesafesearch.google.com`, note the IP address, and add a
  hosts-file line such as `<ip> www.google.com #forcesafesearch` for each domain (Windows
  `drivers\etc\hosts` under the system folder; macOS `/private/etc/hosts`; Linux `/etc/hosts`). Google notes users
  who are administrators on the device can undo this.
- **Chromebooks / Chrome**: Google points admins to Chrome policies set in the Google Admin console.
- **Family accounts**: Family Link for parents; Google Workspace for Education age controls for schools.

## DuckDuckGo
Map `duckduckgo.com` to `safe.duckduckgo.com` by setting the DNS entry for `duckduckgo.com` to a CNAME for
`safe.duckduckgo.com`. DuckDuckGo says this guarantees strict safe search for all queries on the network and
disables the client controls. Searches from `safe.duckduckgo.com` always use "strict".

## Close the gaps
- Clients that use their own DNS (public resolvers, DNS over HTTPS) sidestep internal DNS overrides; control
  that egress (see the proxy-bypass-detection skill).
- Search engines that offer no way to force safe search cannot be enforced: block them by category or list.
- Bing, YouTube Restricted Mode and browser policy names were not confirmed by a page read in this review;
  take them from the vendor's current documentation.

## Verify
- [ ] `nslookup www.google.com` on the internal resolver returns the forcesafesearch address.
- [ ] Google's safesearch page (google.com/safesearch) shows filtering on by default and not switchable off.
- [ ] A test search on DuckDuckGo shows strict results and the setting cannot be changed.

## Checked
Checked 2026-11-09 against the Google Search Help page "Lock SafeSearch for accounts, devices & networks you
manage" and the DuckDuckGo Help page on safe search, both read in full. Removed as unconfirmed: the Bing
`strict.bing.com` row (Microsoft page returned 404), the YouTube restrict hostnames and `YouTube-Restrict`
header, `X-GoogApps-Allowed-Domains`, the Windows DNS, BIND RPZ and Pi-hole recipes, named DNS filtering
vendors, and the Chrome/Edge policy names.
Method: docs-checked 2026-11-09 against the Google and DuckDuckGo help pages.
