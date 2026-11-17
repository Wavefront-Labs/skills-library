---
id: computing-software.systems-network-administration.linux.wifi-with-nmcli-and-wpa-supplicant
name: wifi-with-nmcli-and-wpa-supplicant
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, wifi, wireless, nmcli-wifi, wpa-supplicant, wpa2, wpa3, 802-1x, eap, iw, rfkill, regulatory-domain, networkmanager, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Connect Linux to Wi-Fi with nmcli or bare wpa_supplicant: scanning, WPA2/WPA3-PSK and 802.1X profiles, hidden SSIDs, rfkill and regulatory domain, and diagnosing association failures."
sources:
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nmcli.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/src/libnmc-setting/settings-docs.h.in
  - https://github.com/masap/hostap/blob/main/wpa_supplicant/wpa_supplicant.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi with nmcli and wpa_supplicant

**Goal:** a laptop, kiosk or headless board joins the right network (PSK or enterprise),
reconnects on its own, and you can tell radio, auth and DHCP failures apart.

## 1. Radio state first
```bash
nmcli radio wifi on              # NetworkManager's Wi-Fi radio switch (see also: nmcli radio all)
```
Set the regulatory domain (`country=` in wpa_supplicant.conf, or your distribution's mechanism) before expecting all channels.

## 2. nmcli (NetworkManager hosts)
```bash
nmcli dev wifi list --rescan yes                      # SSID, channel, signal, security; --rescan auto|yes|no
nmcli dev wifi connect "Office" password '<PSK>'      # creates a profile named after the SSID
nmcli dev wifi connect "Hidden" password '<PSK>' hidden yes
# WPA3-SAE explicitly:
nmcli con add type wifi ifname wlan0 con-name office ssid Office \
  wifi-sec.key-mgmt sae wifi-sec.psk '<PSK>'          # sae = WPA3 personal only; wpa-psk = WPA2 + WPA3 personal
# 802.1X PEAP/MSCHAPv2 enterprise:
nmcli con add type wifi ifname wlan0 con-name corp ssid CorpWiFi \
  wifi-sec.key-mgmt wpa-eap 802-1x.eap peap 802-1x.phase2-auth mschapv2 \
  802-1x.identity '<user>' 802-1x.password '<password>' \
  802-1x.ca-cert /etc/pki/tls/certs/corp-ca.pem 802-1x.domain-suffix-match radius.corp.example
nmcli con mod office connection.autoconnect-priority 10   # prefer when several known networks are in range
```
Always set `ca-cert` + `domain-suffix-match` for EAP; the NM property docs say leaving the CA unset allows man-in-the-middle attacks and is not recommended.

## 3. Bare wpa_supplicant (minimal images, no NM)
```
# wpa_supplicant.conf for wlan0 (readable by root only)
ctrl_interface=DIR=/run/wpa_supplicant GROUP=<group-allowed-to-control>
update_config=1
country=GB
network={
    ssid="Office"
    psk="<passphrase, 8-63 chars>"      # or 64 hex digits; wpa_passphrase can generate the hex form
    key_mgmt=WPA-PSK
}
# WPA3-Personal only, instead of the psk lines:
#   key_mgmt=SAE
#   sae_password="<password>"
#   ieee80211w=2
```
```bash
wpa_supplicant -B -i wlan0 -c <config-file>     # start it; unit names and paths are distribution-specific
wpa_cli -i wlan0 status                         # wpa_state=COMPLETED means associated + authenticated
```
Then obtain an address with your DHCP client of choice.

## 4. Diagnose
- Watch the NetworkManager and wpa_supplicant logs while connecting (`nmcli general logging level DEBUG domains WIFI`, restore afterwards): wrong key, association rejected, EAP certificate or domain mismatch and DHCP failure show up as different stages; associated but no IP points at DHCP/VLAN on the AP side.
- Power saving can drop connections on some chipsets: the NM property `802-11-wireless.powersave` (alias `wifi.powersave`) takes 2 to disable it, 3 to enable, 1 to ignore, 0 for the global default.

## Verify
- [ ] `nmcli -f GENERAL.STATE,IP4.ADDRESS dev show wlan0` shows connected with an address (or `wpa_cli status` COMPLETED).
- [ ] Reboot / toggle the radio: it reconnects automatically to the preferred network.

## Checked
Checked 2026-10-25 against the NetworkManager source tree on GitHub (NetworkManager/NetworkManager main, last commit 2026-10-23): nmcli `radio wifi`, `device wifi connect` with `password` and `hidden yes`, `device wifi list --rescan auto|yes|no`, `general logging level ... domains`, property names and values `wifi-sec.key-mgmt` (sae, wpa-psk, wpa-eap), `802-1x.eap`, `802-1x.phase2-auth`, `802-1x.ca-cert`, `802-1x.domain-suffix-match`, `connection.autoconnect-priority`, `802-11-wireless.powersave` values 0-3; wpa_supplicant.conf options `ctrl_interface`, `update_config`, `country`, `psk` (8-63 character passphrase or 64 hex), `key_mgmt`, `sae_password`, `ieee80211w` (2 for WPA3-Personal-only) and the wpa_passphrase helper, read from a GitHub mirror of the hostap sources (masap/hostap, pushed 2026-05). Fixed: a hex `psk` was combined with `SAE`, which the config reference does not support (SAE uses `sae_password` or a passphrase). Removed unconfirmed claims: rfkill and iw regulatory commands, the regdom persistence advice, the `wpa_supplicant@wlan0` unit, log message strings, signal thresholds and `iw` power-save commands.

Method: documentation only; no commands were run.
