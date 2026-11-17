---
id: computing-software.digital-privacy-hygiene.vpn-tools.pi-hole-or-adguard-home-on-the-lan
name: pi-hole-or-adguard-home-on-the-lan
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, pi-hole, adguard-home, dns-privacy, dns-blocklists, self-hosted-dns, dhcp-dns, upstream-doh, tracker-blocking, raspberry-pi]
level: practitioner
status: draft
description: "Run Pi-hole or AdGuard Home as the home network's DNS: install, encrypted upstream, router DHCP handoff, blocklists, and stopping devices that bypass it."
sources:
  - "https://docs.pi-hole.net/"
  - "https://github.com/AdguardTeam/AdGuardHome/wiki"
  - "https://www.privacyguides.org/en/dns/#self-hosted"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pi-hole or AdGuard Home on the LAN

**Goal:** block trackers and ads for every device at home, including smart TVs that
can't run blockers, with a resolver you control.

## Install (small Linux box or Raspberry Pi with a static IP)
```bash
# Pi-hole
curl -sSL https://install.pi-hole.net | bash        # review the script first if you prefer
pihole setpassword                                   # admin UI password (v6: pihole setpassword)
# AdGuard Home
curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v
```
Docker images exist for both. Reserve the box's IP in the router.

## Encrypted upstream
- **AdGuard Home**: Settings > DNS settings > Upstream DNS: `https://dns.quad9.net/dns-query`
  (DoH) or `tls://dns.quad9.net` (DoT) natively.
- **Pi-hole**: use `cloudflared`/`dnscrypt-proxy` as a local DoH forwarder, or **Unbound**
  as a recursive resolver (no third-party resolver; queries go to authoritative servers
  in plaintext, which is a different trade-off).

## Point the network at it
Router DHCP settings: DNS server = the Pi-hole/AdGuard IP, **no secondary** public DNS
(clients would bypass it). Or let Pi-hole/AdGuard be the DHCP server.

## Blocklists
Start with defaults + one curated list (e.g. OISD, HaGeZi). Too many lists = breakage
and maintenance. Use query log to allowlist.

## Bypassers
Some devices hard-code `8.8.8.8` or use DoH. Router firewall: redirect outbound
port 53 to the Pi-hole, block DoT (853) to the internet; DoH can't be fully blocked
this way.

## Gotchas
- If the box dies, the household loses DNS: keep a documented fallback (temporarily set
  router DNS to Quad9) or run two instances.
- Phones on mobile data or VPN don't use it; pair with NextDNS or a home VPN.

## Verify
- [ ] Query log shows requests from all household devices.
- [ ] `nslookup doubleclick.net <pihole-ip>` returns 0.0.0.0 / blocked.
