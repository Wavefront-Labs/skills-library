---
id: computing-software.digital-privacy-hygiene.device-hardening.home-security-camera-hardening
name: home-security-camera-hardening
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, security-camera-hardening, smart-home, end-to-end-encryption, iot-security]
level: practitioner
status: draft
description: "Harden home security and doorbell cameras: account 2FA, end-to-end encrypted video, local storage, shared users, network isolation and placement."
sources:
  - "https://support.ring.com/"
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-says-ring-employees-illegally-surveilled-customers-failed-stop-hackers-taking-control-users-cameras"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Home security camera hardening

**Goal:** cameras that protect your home without becoming a window into it for strangers or employees.

## Account
- Unique password, two-factor (authenticator app) on the camera account; the 2023 FTC Ring case cited weak access
  controls and credential stuffing that let attackers view and talk through cameras.
- Review **shared users** and remove ex-partners, past tenants, contractors.
- Check active sessions/devices in the app.

## Video privacy
- Turn on **end-to-end encryption** where offered (Ring Video End-to-End Encryption; Apple HomeKit Secure Video is
  E2EE by design). Some features (AI search, sharing to web) turn off.
- Prefer **local storage** (microSD, NVR, Home Assistant/Frigate) for indoor cameras.
- Indoor cameras: use privacy mode/shutters or schedules when people are home.

## Network
- Put cameras on an IoT network/VLAN; block their access to your main LAN.
- Disable UPnP and P2P remote access you don't use; never port-forward camera RTSP to the internet.
- Auto firmware updates on.

## Placement and law
Point outdoor cameras at your property, not neighbours' windows or gardens; audio recording may be illegal without
consent in some places. Post a notice if required.

## Gotchas
- Cheap cameras with cloud relays from unknown vendors have had flaws exposing streams; choose vendors with a security
  track record and support period.
