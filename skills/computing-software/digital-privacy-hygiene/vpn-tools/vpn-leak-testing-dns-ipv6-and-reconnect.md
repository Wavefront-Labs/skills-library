---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-leak-testing-dns-ipv6-and-reconnect
name: vpn-leak-testing-dns-ipv6-and-reconnect
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-leak-test, dns-leak-test, dns-leak, ipv6-leak, vpn-reconnect-leak, webrtc-leak, kill-switch, browserleaks, mullvad-connection-check]
level: practitioner
status: draft
description: "Test a VPN for DNS, IPv6, WebRTC and reconnect/boot leaks with browser checks and a packet capture, and fix each class of leak."
sources:
  - "https://mullvad.net/en/check"
  - "https://browserleaks.com/"
  - "https://www.privacyguides.org/en/basics/vpn-overview/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VPN leak testing

**Goal:** confirm that nothing reveals your real IP or DNS queries while the VPN is on,
including at the moments it isn't fully up.

## 1. Baseline (VPN off)
Note your real IPv4, IPv6 (if any) and ISP's DNS servers at `browserleaks.com/ip` and
`/dns`.

## 2. Static tests (VPN on)
- **IP**: `mullvad.net/check` (works for any provider for IP; full checks for Mullvad) or
  `browserleaks.com/ip`: only the VPN IP appears.
- **DNS leak**: `browserleaks.com/dns` or `dnsleaktest.com` extended test: only the VPN's
  (or your chosen encrypted) resolvers; no ISP resolvers.
- **IPv6 leak**: test page shows no IPv6 address from your ISP. If it does and the VPN
  doesn't support IPv6, enable the client's IPv6 blocking or disable IPv6 on the adapter.
- **WebRTC**: `browserleaks.com/webrtc` shows no public non-VPN IP. Fix: browser setting
  or extension; Firefox `media.peerconnection.enabled=false` disables WebRTC entirely.

## 3. Dynamic tests (reconnect and boot)
Capture traffic on the physical interface while forcing transitions:
```bash
sudo tcpdump -ni <wifi-interface> 'not (host <VPN_SERVER_IP>)'   # expect silence
```
Then: switch servers, toggle Wi-Fi, sleep/wake the laptop, reboot. Any packets to other
hosts are leaks. Fix: enable the client's **kill switch / lockdown mode**
("Always require VPN", "Block connections without VPN" on Android) and
"launch at startup". On Windows use Wireshark the same way.

## Gotchas
- Browser tests only see browser traffic; other apps can leak independently.
- Some leak tests show the provider's partner DNS; check it isn't your ISP's.
- DoH configured in the browser bypasses the VPN's DNS (goes inside the tunnel, but to a
  different resolver). Not a leak of IP, but a choice to be aware of.

## Verify
- [ ] No ISP IP/DNS in any static test.
- [ ] tcpdump silent during server switch, Wi-Fi toggle and reboot.
