---
id: computing-software.systems-network-administration.wireshark.wpa3-sae-handshake-analysis
name: wpa3-sae-handshake-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan, sae, wpa3, dragonfly, eapol, wireless-security]
level: practitioner
status: docs-checked
description: "Analyse WPA3-Personal SAE authentication in Wireshark: commit/confirm exchange, groups, anti-clogging tokens, status codes and AKM types."
sources:
  - https://www.wireshark.org/docs/dfref/w/wlan.html
  - https://www.wi-fi.org/discover-wi-fi/security
  - https://gitlab.com/wireshark/wireshark/-/raw/master/epan/dissectors/packet-ieee80211.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WPA3 SAE handshake analysis

WPA3-Personal authenticates with SAE (Simultaneous Authentication of Equals) carried in 802.11
Authentication frames. Wireshark's 802.11 dissector labels authentication algorithm 3 as SAE.

## Filters
```
wlan.fixed.auth.alg == 3                  # SAE
wlan.fixed.sae_message_type == 1          # Commit; 2 = Confirm
wlan.fixed.status_code != 0
wlan.fixed.finite_cyclic_group            # group id in the commit
wlan.rsn.akms.type == 8                   # AKM 8 = SAE (SHA256)
```

## Normal sequence
Authentication frames carrying SAE Commit, then SAE Confirm, then association and the EAPOL
4-way handshake. WPA3 networks require Protected Management Frames (Wi-Fi Alliance), so the RSN
capabilities should show Management Frame Protection Capable (`wlan.rsn.capabilities.mfpc`) and
Required (`wlan.rsn.capabilities.mfpr`) set.

## Reading the fields
- Group id values in Wireshark's table (taken from the IANA IKE registry): 19 = 256-bit random ECP
  group, 20 = 384-bit, 21 = 521-bit; 14 = 2048-bit MODP.
- AKM suite types: 8 = SAE (SHA256), 9 = FT using SAE (SHA256), 24 = SAE (GROUP-DEPEND), 25 = FT
  using SAE (GROUP-DEPEND).
- When the commit carries an anti-clogging token the dissector shows it in
  `wlan.fixed.anti_clogging_token`.

## Failure patterns
| Seen | Meaning |
|------|---------|
| Status 76 | Authentication rejected because an anti-clogging token is required; resend the commit with the token |
| Status 77 | Authentication rejected because the offered finite cyclic group is not supported; try another group |
| Status 126 | SAE authentication uses direct hashing (hash-to-element) instead of looping to obtain the PWE |

Look up other status codes in the Status Code field of the failing frame; Wireshark prints the
text.

## Verify
- [ ] Commit and confirm complete with status 0, then the EAPOL handshake finishes.

## Checked
2026-11-09. Read: Wireshark packet-ieee80211.c (auth algorithm 3 = SAE, SAE message type 1 Commit
and 2 Confirm, status codes 76, 77 and 126 texts, group id table, AKM types 8, 9, 24, 25, MFPC and MFPR
field names, anti-clogging token field), the Wireshark wlan display filter reference (field names
exist), and the Wi-Fi Alliance security page (WPA3 requires PMF). Removed: the claim that status
126 means unknown password identifier (the dissector says direct hashing), AKM 24 as SAE-EXT-KEY
(Wireshark labels it GROUP-DEPEND), "P-256 mandatory", the transition-mode row, and the PMK
decryption paragraph (not confirmed in the pages read).
Method: docs-checked 2026-11-09 against packet-ieee80211.c, the wlan dfref page and wi-fi.org security page.
