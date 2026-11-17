---
id: computing-software.digital-forensics-incident-response.incident-response-process.emergency-perimeter-and-proxy-blocks
name: emergency-perimeter-and-proxy-blocks
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [emergency-firewall-block, containment, c2-blocking, dfir, egress-filtering]
level: practitioner
status: draft
description: "Push emergency firewall, proxy and DNS blocks during containment: what to block, rule placement, logging, expiry and verifying the block took effect."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Emergency perimeter and proxy blocks

**Goal:** cut attacker infrastructure off quickly and in a way that is logged, reversible and verifiable.

## What to block (in order of value)
1. Confirmed C2 domains and IPs (block at DNS and proxy as well as firewall; IP-only blocks fail when C2 rotates behind CDNs).
2. Exfiltration services seen in the incident (rclone endpoints such as MEGA, file-share sites) - block by category on the proxy.
3. Remote access tools abused by the attacker (AnyDesk, ScreenConnect relay domains) if not business-used.
4. Inbound: VPN/edge device management interfaces from the internet; attacker source IPs for brute force.

## Rule placement and hygiene
- Use a dedicated "IR-BLOCK" address group / External Dynamic List / DNS RPZ zone so blocks are
  added in one place and removed cleanly later.
- Place block rules above broad allow rules; log every hit (`log at session start` for denies).
- Name rules with the case ID and expiry date; review at case closure.
- DNS: RPZ or resolver block returning NXDOMAIN or a sinkhole IP; sinkhole gives you the list of infected hosts.

## Timing
- Coordinate with the containment plan: blocking C2 before isolating hosts tells the attacker
  they are seen. For a coordinated remediation event, push blocks at the same minute as account and host actions.

## Verify
- From a test host: `nslookup <c2-domain>` returns the sinkhole; `curl -v https://<c2-domain>` fails at the proxy.
- Firewall/proxy logs show deny hits; list the internal sources hitting the block and feed them back into scoping.
- Check for bypasses: direct-to-IP egress on 443, DoH to public resolvers (block known DoH endpoints), alternate egress paths (guest Wi-Fi, cloud NAT).

## Gotchas
- Blocking shared CDN or cloud IPs breaks business traffic; prefer domain/SNI blocks.
- Changes made directly on devices without change tickets get rolled back by config management.
- Blocks without expiry accumulate for years.
