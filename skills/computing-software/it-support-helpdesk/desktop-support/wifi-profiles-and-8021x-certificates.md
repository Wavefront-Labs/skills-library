---
id: computing-software.it-support-helpdesk.desktop-support.wifi-profiles-and-8021x-certificates
name: wifi-profiles-and-8021x-certificates
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-networking, wifi-8021x, eap-tls, peap, wpa2-enterprise, wpa3, netsh-wlan, wlan-report, radius, nps, client-certificate, wifi-profile, wifi-profile-intune, certificate-manager]
level: practitioner
status: draft
description: "Deploy and fix corporate Wi-Fi: netsh wlan profiles, WPA2/WPA3-Enterprise with EAP-TLS or PEAP, missing client/root certificates, and reading the WLAN report and NPS logs."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-wlan"
  - "https://learn.microsoft.com/en-us/intune/intune-service/configuration/wi-fi-settings-windows"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/802-1x-authentication-issues-troubleshooting"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wifi-profiles-and-8021x-certificates

Goal: the laptop joins the corporate SSID silently with a certificate, and
when it doesn't, you know whether the failure is RF, profile, certificate or
RADIUS.

## Inspect
```cmd
netsh wlan show interfaces            :: SSID, BSSID, signal %, radio type, auth
netsh wlan show profiles
netsh wlan show profile name="CorpWiFi" key=clear
netsh wlan show wlanreport            :: HTML report of 3 days of sessions and disconnect reasons
netsh wlan export profile name="CorpWiFi" folder=. key=clear
netsh wlan add profile filename="Wi-Fi-CorpWiFi.xml" user=all
```
Report path: `%ProgramData%\Microsoft\Windows\WlanReport\wlan-report-latest.html`.

## EAP-TLS (certificate) flow — what must exist on the device
1. A **client certificate** with Client Authentication EKU, delivered by SCEP
   or PKCS profile (Intune) or autoenrolment (GPO). Check `certlm.msc`
   (device cert) or `certmgr.msc` (user cert) — which store depends on the
   profile's authentication mode (machine vs user).
2. The **root (and intermediate) CA** that issued the RADIUS server's
   certificate, trusted and named in the Wi-Fi profile's "trusted root" list.
3. The Wi-Fi profile itself, referencing both. In Intune, the Wi-Fi profile,
   trusted cert profile and SCEP/PKCS profile must target the **same group
   type** (device vs user) or the dependency never resolves.

## PEAP-MSCHAPv2 (password)
Fails after password change until the user re-enters credentials; expiring
passwords on a phone can lock out the AD account repeatedly. Credential
Guard on Windows 11 blocks MSCHAPv2 single-sign-on — a common reason to move
to EAP-TLS.

## Where it fails
- Event Viewer → Applications and Services → Microsoft → Windows →
  WLAN-AutoConfig/Operational: reason codes for association vs auth.
- RADIUS/NPS server: Security log Event 6273 (denied) gives the Reason Code
  — 16 bad creds, 22 cert can't be validated, 48 no matching network policy,
  265 untrusted root on server side.

## Gotchas
- Server cert renewed with a new intermediate → every client failing at once
  if the profile pins the old chain.
- Machine-auth only profiles don't work before the device cert is issued
  (first boot during Autopilot) — keep a provisioning SSID or wired path.
- Weak signal (< 40 % in `show interfaces`) masquerades as auth failure
  through repeated timeouts.

## Verify
`netsh wlan show interfaces` → State connected, Authentication
WPA2-Enterprise/WPA3-Enterprise, IP obtained; NPS logs Event 6272 (granted)
for the device; reconnects automatically after reboot before user sign-in
(machine auth).
