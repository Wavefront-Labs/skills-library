---
id: computing-software.systems-network-administration.wireshark.wpa2-psk-decryption
name: wpa2-psk-decryption
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan-capture, 802-11, wpa-decryption, wpa2-psk, eapol, four-way-handshake, wpa-pwd, wpa-psk, ieee-802-11-decryption-keys, wpa3-sae, ptk, monitor-mode]
level: practitioner
status: docs-checked
description: "Decrypt WPA2-Personal Wi-Fi captures in Wireshark: capture the 4-way EAPOL handshake, add wpa-pwd or wpa-psk keys, and why WPA2-Enterprise and WPA3 differ."
sources:
  - https://wiki.wireshark.org/HowToDecrypt802.11
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Decrypting WPA2-PSK traffic

Only possible for networks you are authorised to analyse; you need the passphrase and each
client's handshake.

## 1. Capture correctly
- WPA and WPA2 derive per-device keys from the EAPOL handshake that happens when a machine joins.
  Unless all four handshake packets are present for the session, Wireshark cannot decrypt that
  traffic. Locate them with the display filter `eapol`.
- Force the machine to (re-)join while the capture runs, for example put a phone or tablet to sleep,
  start the capture, then wake it. Repeat for every machine whose traffic you want.

## 2. Add the key
Edit > Preferences > Protocols > IEEE 802.11, tick "Enable decryption", then Edit next to
Decryption Keys and add a key (up to 64 keys are supported). Types:
- `wpa-pwd`: `MyPassword:MySSID`. The password and SSID create the raw pre-shared key. The SSID
  may be omitted (Wireshark then uses the last-seen SSID, unreliable in busy environments).
- `wpa-psk`: the raw pre-shared WPA key in hex.
- `wep`: hex string, with or without colons.
Passphrase and SSID accept URI-style percent escapes for troublesome characters: `%20` for a space,
`%25` for a percent sign, and `%3a` for a colon (needed to tell it from the separator).

## 3. Check
- Decrypted packets show their upper layers (for example IP) rather than opaque data. Filter on the
  client's address with `wlan.addr` or `ip.addr`.
- Depending on how the driver delivers frames you may need to toggle "Assume Packets Have FCS" and
  "Ignore the Protection bit".

## When it fails
| Cause | Fix |
|---|---|
| Handshake missing or any of the 4 messages absent | recapture while the client reconnects |
| Wrong SSID or passphrase | correct the key (percent-escape special characters) |
| Many devices joined during the trace | older Wireshark decrypts only the last device; newer handles up to 256 associations; filter to the relevant packets with `wlan.addr` and save a new file |
| EAPOL rekey mid-capture | Wireshark 2.0 or newer is needed to decode after a rekey |
| WPA2-Enterprise | extract the PMK from the client or the RADIUS server and configure it as a PSK; works up to the first EAPOL rekey |
| WPA3 | a different PMK per connection: the handshake plus password is not enough; obtain the PMK from the client or AP (wpa_supplicant or hostapd logging with `-d -K`); it decrypts only that client-AP pair |

## Verify
- [ ] `eapol` shows all four messages for the client.
- [ ] After adding the key, `ip.addr == <client IP>` shows decrypted packets.

## Checked
Method: docs-checked 2026-11-09 against the Wireshark wiki HowToDecrypt802.11 page, read in full. Dropped unconfirmed claims: monitor-mode and Cisco sniffer-mode specifics, wpa_passphrase and the PSK generator page, wlan.analysis.tk, the tshark uat command line, the "Decrypted CCMP data" tab, and the 802.11w/FT rows.
