---
id: computing-software.digital-privacy-hygiene.vpn-tools.choosing-a-private-search-engine
name: choosing-a-private-search-engine
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, private-search-engine, duckduckgo, brave-search, startpage, searxng, mullvad-leta, search-history, privacy-browser]
level: intro
status: draft
description: "Pick and set a search engine that doesn't build a profile from your queries (DuckDuckGo, Brave Search, Startpage, SearXNG), and set it as default everywhere."
sources:
  - "https://www.privacyguides.org/en/search-engines/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a private search engine

**Goal:** search queries are some of the most revealing data you produce (health,
money, relationships). Send them to an engine that doesn't tie them to you.

## Options (see Privacy Guides for current list)
| Engine | Index | Notes |
|---|---|---|
| Brave Search | Own independent index | Anonymous by default; optional ads |
| DuckDuckGo | Mostly Bing plus own crawlers | Default in many privacy browsers; `!bangs` |
| Startpage | Google results via proxy | Google-quality results without Google profile; owned by an ad company |
| Mullvad Leta | Proxied results, cached | For Mullvad VPN users |
| SearXNG | Metasearch, self-hostable | Public instances vary in trust; self-host for control |

## Set as default
- Desktop browsers: Settings > Search > default engine. Remove Google from address bar
  suggestions if desired.
- iOS Safari: Settings > Apps > Safari > Search Engine.
- Android Chrome/Brave/Firefox: browser settings > Search engine.
- Disable **search suggestions** (sends each keystroke) if you want less leakage.

## If you keep Google
Signed out, or in a container/profile; Web & App Activity paused or auto-deleted
(see `computing-software.digital-privacy-hygiene.privacy-configuration.account-privacy-and-tracking-review`).

## Gotchas
- Private engines still see your IP unless you use a VPN/Tor; they promise not to store it.
- Clicking through to a site gives that site the usual tracking; the engine only protects
  the query.

## Verify
- [ ] Typing a query in the address bar on each device goes to the chosen engine.
