---
id: computing-software.digital-privacy-hygiene.vpn-tools.running-a-snowflake-proxy
name: running-a-snowflake-proxy
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, snowflake-proxy, tor, censorship-circumvention, volunteer-proxy]
level: practitioner
status: docs-checked
description: "Help censored users reach Tor by running a Snowflake proxy as a browser extension or standalone server, and know what network setup the Tor Project recommends."
sources:
  - "https://snowflake.torproject.org/"
  - "https://community.torproject.org/relay/setup/snowflake/standalone/"
  - "https://support.torproject.org/censorship/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running a Snowflake proxy

**Goal:** donate bandwidth so people in censored countries can connect to Tor.

## What it is
Snowflake is a pluggable transport that routes a censored user's connection through volunteer proxies in uncensored countries. It uses WebRTC, so the traffic resembles a video or voice call, which the Tor Project presents as costly for censors to block. It is built into Tor Browser, Orbot and Ricochet-Refresh; users enable it in those apps' settings if Tor cannot connect.

## Ways to run one
| Method | Notes |
|---|---|
| Browser add-on (Firefox, Chrome, Edge) | Icon turns green when a blocked user connects through you. The add-on is for volunteers only; it does not circumvent censorship for you. |
| Embedded widget | A website operator embeds it; visitors act as proxies while the tab stays open. |
| Standalone proxy | For technical users on a desktop or server. Install via Ansible role, Docker, source, Debian packages or FreeBSD. |

## Standalone recommendations (Tor community page)
- Servers suit it: more bandwidth and reliability for users behind restrictive NATs and firewalls.
- Round-the-clock connectivity.
- Ideally a full-cone NAT (test with the stun-nat-behaviour tool: address-independent mapping, and address-independent or address-dependent filtering), or no/unrestricted NAT with incoming UDP open across the ephemeral port range (see `/proc/sys/net/ipv4/ip_local_port_range`, or set `-ephemeral-ports-range`).
- Help is on the Tor Project Forum.

## Gotchas
- The cited pages do not describe what a proxy operator or the censored user can see of each other, bandwidth use, or capacity settings; read the per-install pages and Snowflake technical overview before running one where your IP must stay unlinked from Tor-adjacent activity.

## Checked
Method: 2026-11-08 read all three cited pages. The Snowflake page and standalone setup page support the content above; the censorship page is only a landing page listing subtopics. Removed unsupported claims: the "not an exit relay / sites never see your IP" assertion, the Docker/Go-binary specifics, "no inbound port forwarding needed", extension NAT-type indicator, and log/user-count verification.
