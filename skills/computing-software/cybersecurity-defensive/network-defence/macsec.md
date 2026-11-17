---
id: computing-software.cybersecurity-defensive.network-defence.macsec
name: macsec
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [macsec, ieee-802-1ae, mka, link-encryption, switch-to-switch-encryption, network-access-control, layer2-security]
level: advanced
status: docs-checked
description: "Deploy MACsec (802.1AE) for link encryption: switch-to-switch MKA with pre-shared CAK, host-to-switch with 802.1X, cipher suites, replay windows and troubleshooting."
sources: ["https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/macsec_encryption.html", "https://standards.ieee.org/ieee/802.1AE/7101/", "https://www.juniper.net/documentation/us/en/software/junos/security-services/topics/topic-map/understanding_media_access_control_security_qfx_ex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MACsec (IEEE 802.1AE)

Hop-by-hop Layer 2 encryption and integrity at line rate in switch ASICs. Protects links you do not
physically control (between buildings, colocation cross-connects, dark fibre, DCI) and access ports.

## Switch-to-switch (MKA with PSK) - Cisco IOS-XE example
```
key chain DCI-KC macsec
 key 01
  cryptographic-algorithm aes-256-cmac
  key-string <64 hex chars CAK>
  lifetime local 00:00:00 Jan 1 2026 infinite
mka policy DCI-POL
 key-server priority 0
 macsec-cipher-suite gcm-aes-xpn-256
 confidentiality-offset 0
interface TenGigabitEthernet1/1/1
 macsec network-link
 mka policy DCI-POL
 mka pre-shared-key key-chain DCI-KC
```
Use XPN cipher suites (GCM-AES-XPN-256) on high-speed links to avoid frequent rekeying (PN exhaustion).

## Host-to-switch
802.1X with EAP-TLS derives the MKA keys; `macsec` on the access port plus `authentication linksec policy must-secure` (or should-secure during rollout). The endpoint supplicant must support MACsec.

## Operations
- Key rollover: add the next key in the key chain with overlapping lifetime before the current expires.
- Monitor: `show mka sessions` (state Secured) and MACsec counters.
- Hardware support required on both ends (and for some optics/line cards); check feature licences.

## Gotchas
- MACsec is hop-by-hop: frames are clear inside each switch. Intermediate carrier L2 services may not pass MACsec frames; check support with the carrier.
- MACsec adds header overhead, so MTU changes; adjust or see silent drops.
- `should-secure` falls back to clear traffic - fine for rollout, not as end state.

## Verify
- [ ] MKA session Secured on all target links with the intended cipher.
- [ ] Packet capture on the link shows no clear payload.

## Checked
2026-10-28. Confirmed against official pages: IOS-XE key chain, aes-256-cmac, gcm-aes-xpn-256, mka policy, macsec network-link, mka pre-shared-key, linksec must-secure, should-secure on switch-to-switch with PSK (Cisco Catalyst 9300 MACsec guide); XPN for high-speed links.
Removed or rewritten: show macsec summary, the EtherType value, the 32-byte figure, endpoint supplicant products and the EoMPLS/VPLS claim.
Method: documentation only; no commands were run.
