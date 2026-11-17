---
id: computing-software.systems-network-administration.cisco-networking.capwap-ap-join-troubleshooting
name: capwap-ap-join-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, wlc, wireless-lan-controller, catalyst-9800, lightweight-ap, capwap, ap-join, wlc-discovery, option-43, cisco-capwap-controller, dtls, primary-controller, ap-country-code]
level: practitioner
status: draft
description: "Get lightweight APs to join a Catalyst 9800 WLC over CAPWAP: discovery order (DHCP 43, DNS, broadcast, primed), ports, DTLS/cert and time issues, and the join-failure checklist."
sources:
  - https://www.cisco.com/c/en/us/support/docs/wireless/catalyst-9800-series-wireless-controllers/215661-troubleshoot-ap-join-issues-on-catalyst.html
  - https://www.cisco.com/c/en/us/support/docs/wireless-mobility/wireless-lan-wlan/97066-dhcp-option-43-00.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CAPWAP AP join and discovery

Lightweight APs build a CAPWAP tunnel to a WLC: UDP 5246 (control, DTLS) and 5247 (data).
They must first **discover** a controller, then **join**, then download image/config.

## Discovery methods (AP tries all, then picks)
1. Primed: previously joined controller / configured primary/secondary/tertiary.
2. Layer 2 broadcast on the local subnet (AP in the WLC's management VLAN).
3. **DHCP option 43**: list of WLC management IPs. For Cisco APs the value is TLV type
   `0xf1`, length = 4 x number of controllers, then IPs in hex.
   ```
   ip dhcp pool AP-VLAN
    option 43 hex f108.0a0a.0a0a.0a0a.0a0b      ! 10.10.10.10 and 10.10.10.11
   ```
4. **DNS**: `CISCO-CAPWAP-CONTROLLER.<domain-from-DHCP>` A record(s).
The AP then joins the least loaded controller unless primary/secondary is set (High
Availability on the AP: `ap name AP1 ... primary WLC1 10.10.10.10` or the AP join profile).

## Join failures, in order
| Check | How |
|---|---|
| AP has IP, gateway, DNS | AP console: `show ip interface brief`, or the switch DHCP binding |
| Reaches WLC | `ping` from AP console; firewall allows UDP 5246/5247 both ways |
| Discovery response | WLC: `show wireless stats ap join summary` / `show ap join stats summary` |
| DTLS / certificate | clock wrong (cert not yet valid), expired MIC on old APs, or SHA2 issues: set NTP on WLC; WLC log `DTLS handshake failed` |
| Regulatory domain | AP's domain (e.g. -E, -B) not allowed in WLC country config |
| Licence / AP count | platform AP limit reached |
| Image download | slow WAN: AP stuck downloading; use AP image predownload or local efficient image upgrade |
| MTU | CAPWAP path MTU issues on VPN: `show ap config general` path MTU; fragmentation |

WLC side:
```
show ap summary
show wireless stats ap join summary
show ap name <AP> config general
debug ra-trace (or Radioactive Tracing in the GUI) for the AP MAC
```
AP side (console, 9600 or 115200): `show capwap client rcb`, `show capwap ip config`,
`capwap ap primary-base <WLC-name> <ip>` to prime manually.

## Verify
- [ ] AP appears Registered in `show ap summary` with the expected tag policy/site.
- [ ] Join statistics show no repeated failures for the AP MAC.
- [ ] Option 43 / DNS discovery works for a factory-reset AP (test one).
