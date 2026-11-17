---
id: computing-software.systems-network-administration.network-design.ddos-and-rogue-ap-defence
name: ddos-and-rogue-ap-defence
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-attacks, ddos, volumetric-attack, syn-flood, amplification, rtbh, scrubbing, flowspec, rogue-ap, evil-twin, wips, rogue-containment, deauthentication-attack, pmf, 802-11w]
level: practitioner
status: docs-checked
description: "Plan for DDoS (volumetric, protocol, application) with upstream scrubbing, RTBH and rate limits, and handle rogue APs and evil twins with WIPS, wired-side tracing and 802.11w."
sources:
  - https://www.cisa.gov/resources-tools/resources/understanding-and-responding-distributed-denial-service-attacks
  - https://datatracker.ietf.org/doc/html/rfc7999
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_rogue_ap_detection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DDoS and rogue AP defence

## DDoS: types
| Type | Example | Where it hurts | Defence |
|---|---|---|---|
| Volumetric | UDP/DNS/NTP/memcached amplification | your internet links | upstream: ISP or cloud scrubbing, RTBH |
| Protocol / state exhaustion | SYN flood, fragment floods | firewalls, load balancers (session tables) | SYN cookies, firewall flood protection, scrubbing |
| Application (L7) | HTTP floods, expensive queries | web/app servers | CDN/WAF rate limiting, bot challenges, caching |
You cannot filter a flood that already saturated your link: plan upstream capacity first.

## Preparation (do before an attack)
- Contract: ISP DDoS service or always-on/on-demand scrubbing. Know the activation procedure and phone numbers.
- **RTBH**: agree a BGP blackhole community with the ISP (RFC 7999 `65535:666`) to drop all
  traffic to an attacked /32 at their edge (sacrifices that IP to save the rest).
- **Flowspec** where supported for finer upstream drops (by port/protocol).
- Baselines and alerts: NetFlow/sFlow volumes per destination.
- Don't be an amplifier: no open resolvers or other reflectable services, and filter spoofed source addresses at your edge.

## During
Identify vector from flow data (protocol, source port, packet size), engage
provider, apply ACLs/rate-limits at the edge for small attacks, RTBH the target if needed,
communicate.

## Rogue APs and evil twins
- **Rogue AP**: unauthorised AP connected to your wired network (bypasses NAC). **Evil twin**:
  attacker AP broadcasting your SSID to harvest credentials.
- Detect: WIPS / controller rogue detection (APs scanning off-channel or dedicated monitor
  APs), classify by "seen on wired network" (rogue detector, switch-port tracing via the rogue's
  wired MAC near its BSSID).
- Respond: trace and physically remove; rogue containment (sending deauths) can be a legal problem because it interferes with other networks: get legal advice first and prefer tracing and removal.
- Prevent: 802.1X/MAB on switch ports (rogue AP gets no access), WPA2/3-Enterprise with server
  certificate validation on clients (evil twins cannot complete EAP), **802.11w PMF** (protected management frames), user awareness of certificate prompts.

## Verify
- [ ] DDoS runbook with provider contacts, RTBH tested in a window.
- [ ] Rogue detection enabled; a test AP plugged into a port is detected and its port found.
- [ ] Clients configured to validate the RADIUS server certificate.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 7999 defines the BLACKHOLE community 0xFFFF029A (low-order octets 666, i.e. 65535:666) and says the blackhole prefix is typically /32 for IPv4.
- Removed: traffic-volume figure, vendor scrubbing list, flow-tool names, reflection port numbers, FCC fine claim, and the PMF behaviour claim (CISA, Cisco rogue-AP and IEEE pages were blocked or missing).
Method: documentation only; no commands were run.
