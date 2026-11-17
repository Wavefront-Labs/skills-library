---
id: computing-software.it-support-helpdesk.apple-device-management.content-caching-network-requirements
name: content-caching-network-requirements
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, content-caching, content-caching-network-requirements, caching-network, peers]
level: practitioner
status: docs-checked
description: "Plan Apple content caching across subnets and sites: public IP matching, peers and parents, selection policies and the proxy and port rules Apple recommends."
sources:
  - "https://support.apple.com/guide/deployment/depde72e125f/web"
  - "https://support.apple.com/guide/deployment/depe9b5c1aab/web"
  - "https://support.apple.com/guide/deployment/depc8f669b20/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# content-caching-network-requirements

Goal: design network and cache topology for multi-subnet and multi-site caching.

How clients find a cache
- Apple devices contact a nearby cache with no configuration, through a lookup service that maps client private and public IP addresses to cache configurations that Macs with caching turned on registered with Apple. This works on NAT networks, on publicly routable addresses and, optionally, for devices tethered to a Mac.
- "Cache content for" options: same public IP address, same local networks, custom local networks, or custom local networks with fallback to devices on the same public IP. "My local networks": one public IP (discovered automatically) or custom public IPs, which needs extra DNS configuration (a DNS TXT record).
- By default a cache serves a specific subnet; it can serve all subnets of the local network that share a public IP, or any combination of public subnets with extra DNS settings. Keys: `LocalSubnetsOnly` (default Yes), `ListenRanges`, `ListenRangesOnly`, `PublicRanges`.

Peers and parents
- Several caches on one network become peers automatically and share content. If an item is missing, a cache asks its peers, then its parents, then Apple over the internet. Caches at the top of a hierarchy are parents.
- Keys: `Parents`, `ParentSelectionPolicy` (default `round-robin`; others `first-available`, `url-path-hash`, `random`, `sticky-available`), `PeerLocalSubnetsOnly` (default Yes, overrides `PeerFilterRanges` and `PeerListenRanges`), `PeerFilterRanges`, `PeerListenRanges`, `MaxPeersToQuery`. Use `url-path-hash` to maximise combined cache size; peers at each level maximise sharing.
- User iCloud data is stored on one cache only and is not replicated across peers or parents.

Network best practice (Apple): allow all Apple push notifications; no manual proxy settings; do not put a proxy in front of caches to accept client requests; bypass proxy authentication for caches; specify a TCP port (`Port`, 0 means random; a hard-coded port is 49192 to 65535); manage inter-site traffic; enforce the MDM restriction "Prevent content caching" on all Macs to block rogue cache registration.

Capacity: use Gigabit Ethernet; if the `AssetCache` process in Activity Monitor sits near maximum CPU, add caches. Set a high enough cache size limit or content is purged and downloaded again.

Gotcha: to log which clients ask for content set `LogClientIdentity` (default No); by default Apple does not expose per-client asset detail.

Verify:
- A client on each subnet is served by the intended cache (check cache metrics in the Cache pane of Activity Monitor).
- Logs: `log show --predicate 'subsystem == "com.apple.AssetCache"'`.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Intro to content caching", "Plan for and set up content caching" and "Advanced content caching settings on Mac" (every key row used above, defaults and the logging example). Removed as unconfirmed: outbound HTTPS to a CDN, the `ClientPolicy` key (not a documented key), VPN public-IP conflict claim, per-VLAN caches, capacity-by-user-count and the "public address may shift" advice. Did not read the "Content caching from the command line on Mac" page (URL not found), so no `AssetCacheManagerUtil activate` or `status` claims are kept.
Method: documentation only; no commands were run.
