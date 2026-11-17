---
id: computing-software.systems-network-administration.wireshark.wlan-deauth-and-reason-codes
name: wlan-deauth-and-reason-codes
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, 802-11, reason-codes, deauthentication, disassociation, wifi-troubleshooting]
level: practitioner
status: verified
description: "Interpret 802.11 deauth and disassoc frames: sender, common reason codes, protected management frames, and telling client faults from AP policy or attacks."
sources:
  - https://www.wireshark.org/docs/dfref/w/wlan.html
  - https://standards.ieee.org/ieee/802.11/7028/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deauthentication, disassociation and reason codes

Requires a monitor-mode (802.11) capture on the client's channel.

## Filters
```
wlan.fc.type_subtype == 0x000c        # deauthentication
wlan.fc.type_subtype == 0x000a        # disassociation
wlan.fixed.reason_code
wlan.fc.type_subtype in {0x0a, 0x0c} && wlan.addr == aa:bb:cc:dd:ee:ff
```
Sender: `wlan.sa`; if it equals the BSSID the AP kicked the client, otherwise the client left.

## Common reason codes
| Code | Meaning | Typical cause |
|---|---|---|
| 1 | Unspecified | vendor catch-all |
| 2 | Previous authentication no longer valid | AP lost state (reboot, roam handling) |
| 3 | Station leaving (deauth) | client turned Wi-Fi off, roaming, sleeping |
| 4 | Inactivity | idle timeout on AP/controller |
| 6 / 7 | Class 2/3 frame from nonauthenticated/nonassociated station | client sending data the AP has no state for (AP rebooted, client confused) |
| 8 | Station leaving BSS (disassoc) | client roaming away |
| 15 | 4-way handshake timeout | wrong PSK, slow client, or RADIUS key delivery delay |
| 23 | IEEE 802.1X authentication failed | RADIUS reject |
| 34 | Poor channel conditions / too many unacked frames | RF problem, client out of range |

Controllers log their own reason too; correlate by timestamp.

## Attack or fault?
- Bursts of deauth frames to broadcast `ff:ff:ff:ff:ff:ff` or to many clients from the BSSID,
  often with sequence numbers that do not fit the AP's sequence, at a rate no AP would use:
  spoofed deauth attack (or a WIPS containing a "rogue").
- Protected Management Frames (802.11w, mandatory in WPA3) make spoofed deauths ineffective:
  check RSN capabilities `wlan.rsn.capabilities.mfpc`/`mfpr`.

## Context frames
Look just before the deauth: EAPOL key messages repeating (handshake failure), Action frames
(BSS transition requests 802.11v), or retries climbing (RF).

## Verify
- [ ] For each disconnect you know sender (AP or client), reason code, and the preceding frames
  that explain it.

## Checked
Run on Wireshark 4.4.1 with a scapy radiotap capture (AP-to-client deauth reason 15, broadcast deauth reason 7,
client disassociation reason 8, beacons with and without the MFPC/MFPR bits): the filters matched the expected frames,
the comma form of the set is required (`{0x0a 0x0c}` fails to parse), `wlan.sa == wlan.bssid` separated AP-sent from
client-sent frames, and `wlan.rsn.capabilities.mfpc`/`mfpr` read the RSN capability bits. The reason-code text in the
table matches Wireshark's value strings for codes 1, 2, 3, 4, 6, 7, 8, 15, 23 and 34 (IEEE 802.11 names). The Wi-Fi
Alliance security page lists PMF as required for WPA3 networks. Typical-cause column is practitioner guidance.
