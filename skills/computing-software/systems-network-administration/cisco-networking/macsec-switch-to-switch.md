---
id: computing-software.systems-network-administration.cisco-networking.macsec-switch-to-switch
name: macsec-switch-to-switch
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, macsec, mka, 802-1ae, link-encryption, pre-shared-key, layer-2-security]
level: practitioner
status: draft
description: "Encrypt switch-to-switch links with MACsec (802.1AE) using MKA and a pre-shared key chain: cipher choice, key rollover, MTU overhead, and verifying secured sessions."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/macsec_encryption.html
  - https://standards.ieee.org/ieee/802.1AE/7176/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MACsec switch-to-switch

MACsec encrypts every frame hop by hop at line rate in the switch ASIC. Use it on links that leave
your physical control: inter-building fibre, leased dark fibre, colocation cross-connects.

## PSK-based MKA (no RADIUS needed)
```
key chain MKA-KC macsec
 key 01
  cryptographic-algorithm aes-256-cmac
  key-string 0 <64-hex-character-CAK>
  lifetime local 00:00:00 Oct 1 2026 infinite

mka policy MKA-POL
 key-server priority 0
 macsec-cipher-suite gcm-aes-xpn-256
 confidentiality-offset 0
 sak-rekey interval 0

interface TenGigabitEthernet1/1/1
 macsec network-link
 mka policy MKA-POL
 mka pre-shared-key key-chain MKA-KC
```
Same key chain (CKN = key ID `01`, CAK = key string) and policy on both ends. `xpn` (extended packet
numbering) cipher suites avoid frequent rekeys at 10G+.

## Key rollover
Add key 02 with a start time in the future on both switches; MKA switches when it becomes valid.
Then remove key 01. Overlapping lifetimes avoid an outage.

## MTU
MACsec adds 32 bytes (SecTAG 16 + ICV 16). Make sure the link and every L2 device in between
(media converters, provider NIDs) passes the larger frames; raise `system mtu` if you also carry
jumbo frames or QinQ.

## Verify
```
show macsec summary
show mka sessions
!  Interface  Local-TxSCI  Policy  Inherited  Key-Server  Port-ID  Peer-RxSCI  MACsec-Peers  Status  CKN
!  Te1/1/1    ...          MKA-POL NO         YES         1        ...         1             Secured 01
show mka sessions interface Te1/1/1 detail
show macsec statistics interface Te1/1/1
```
Status must be `Secured`. Statistics show encrypted/validated packet counters increasing.

## Gotchas
- Not all ports/optics support MACsec (check hardware: Catalyst 9300 uplink modules, 9500 ports,
  certain line cards) and licensing (Network Advantage on some platforms).
- Carrier Ethernet services that consume EAPoL frames (MKA uses EAPoL, ethertype 0x888E) break
  MKA; use `eapol destination-address broadcast-address` or a different EAPoL MAC.
- Mismatched cipher suites leave MKA stuck in `Rx Live Peer` without securing.

## Verify
- [ ] `show mka sessions` Secured on both ends and traffic passes at full rate with full-size frames.
