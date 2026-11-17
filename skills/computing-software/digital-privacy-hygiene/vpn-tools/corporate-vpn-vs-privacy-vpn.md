---
id: computing-software.digital-privacy-hygiene.vpn-tools.corporate-vpn-vs-privacy-vpn
name: corporate-vpn-vs-privacy-vpn
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, corporate-vpn, vpn-selection, work-devices]
level: practitioner
status: draft
description: "Tell apart a work VPN (access to company systems, visible to the employer) from a consumer privacy VPN, and avoid mixing them on work or personal devices."
sources:
  - "https://ssd.eff.org/module/choosing-vpn-thats-right-you"
  - "https://www.cisa.gov/sites/default/files/publications/CSA-SELECTING-HARDENING-REMOTE-ACCESS-VPNS-20210928.pdf"
  - "https://www.privacyguides.org/en/basics/vpn-overview/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Corporate VPN vs privacy VPN

**Goal:** know who sees your traffic when a VPN is on, and keep work and personal use separate.

## Two different tools
| | Corporate (remote-access) VPN | Consumer privacy VPN |
|---|---|---|
| Purpose | Reach internal company systems, apply company security policy | Hide traffic from local network/ISP, change apparent IP |
| Who sees your traffic | Your employer (logging, TLS inspection, DLP) | The VPN provider |
| Typical clients | Cisco Secure Client, GlobalProtect, FortiClient, Zscaler, WireGuard/Tailscale for work | Mullvad, Proton VPN, IVPN, etc. |
| Split tunnel | Often only company subnets, sometimes all traffic | Usually all traffic |

## Practical rules
- Assume anything done on a work device or through a work VPN is visible to the employer. Do personal banking,
  health searches and job hunting on a personal device.
- Do not install a consumer VPN on a work laptop: it usually breaks policy, can conflict with the corporate client
  and may be flagged as data-exfiltration risk.
- A corporate VPN does not anonymise you to websites; sites see the company's egress IP.
- On a personal device enrolled for work (BYOD), check whether the work VPN is per-app (work profile only) or device
  wide before using it for personal browsing.

## Conflicts
Two VPN clients fight over routes and DNS. Disconnect the privacy VPN before starting the work client, or use the
privacy VPN on the router so the work client tunnels inside it (ask IT; some corporate VPNs refuse nested tunnels).

## Verify
With the work VPN on, visit an IP-check site: if it shows the company's IP, all traffic is tunnelled to work.
