---
id: computing-software.it-support-helpdesk.desktop-support.peripheral-and-display-troubleshooting
name: peripheral-and-display-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, peripherals, docking-station, usb-c, thunderbolt, multi-monitor, displaylink, dp-alt-mode, audio-drivers, webcam, bluetooth, device-manager, driver-conflict, power-delivery, hdmi, display-settings, peripheral-troubleshooting, multi-monitor-setup, display-cables, audio-troubleshooting]
level: practitioner
status: draft
description: "Troubleshoot docks, multi-monitor setups, audio, webcam and Bluetooth peripherals on managed laptops: USB-C/Thunderbolt quirks, driver conflicts, power delivery."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# peripheral-and-display-troubleshooting

Goal: resolve the "works at home, not in the office" and "second monitor
went black" class of tickets, which is mostly about USB-C/dock arbitration
and driver conflicts, not the peripheral itself.

## Docking stations and USB-C/Thunderbolt
- Identify the dock's video path first: **DisplayPort Alt Mode** (native
  USB-C carries video, no driver needed beyond GPU driver) vs
  **DisplayLink** (USB signal converted to video by a chipset, needs its
  own driver — check Device Manager for a DisplayLink adapter entry). A
  laptop that only has DP Alt Mode support cannot drive a DisplayLink dock
  at full resolution/refresh without the DisplayLink driver installed and
  up to date — check the dock vendor's compatibility list before assuming
  the laptop is faulty.
- **Power delivery negotiation**: a dock not charging the laptop is
  usually a wattage mismatch (65W dock, 90W laptop) or a cable that's
  USB-C data-only (no PD pins) — swap the cable before replacing the dock.
- One dock, two users, different results: docks can get into a bad
  firmware/negotiation state that only a full power-cycle (unplug dock
  from wall, not just laptop, for 10+ seconds) clears — a laptop restart
  alone often doesn't reset the dock's own state.
- Thunderbolt-specific: check Thunderbolt/USB4 firmware and the vendor's
  Thunderbolt control app (Intel Thunderbolt Control Center on some
  machines) — a device the user hasn't "authorized" in Thunderbolt
  security settings will enumerate but not pass data.

## Multi-monitor and display issues
- **Display not detected**: Windows Settings → Display → Detect, but also
  check it isn't a cable/port issue by swapping ports on the dock/laptop
  — many docks have one port that's DP-only and won't do HDMI-via-adapter.
- **Resolution/refresh rate drops after a driver update**: roll back the
  GPU driver via Device Manager → Display adapter → Driver → Roll Back (if
  available) before a full reinstall; Windows Update-pushed generic GPU
  drivers sometimes regress vendor-specific scaling.
- **Extend vs duplicate confusion**: Win+P is the fast path users forget;
  half of "my second monitor won't work" tickets are duplicate-mode set to
  the wrong primary, not a hardware fault.
- **DPI/scaling mismatch across monitors** (text huge on one, tiny on
  another): per-monitor scaling in Settings → Display, and note some older
  Win32 apps still render blurry regardless — that's an app limitation,
  not a setting to keep chasing.

## Audio
- Wrong default device after a dock disconnect/reconnect: Windows doesn't
  always revert the default playback device cleanly — check Settings →
  Sound → Output before assuming the headset is broken.
- Bluetooth audio choppy/robotic: often a codec fallback (SCO instead of
  A2DP) when the mic is in use simultaneously — explain to the user this
  is a Bluetooth profile limitation on some headsets, not fixable by driver
  update alone; a wired/USB headset is the workaround for calls needing
  mic+quality audio together.
- "No sound" after Windows Update: check Device Manager for a yellow-bang
  audio device first, then Services.msc for Windows Audio service status
  (stopped/disabled) before reinstalling drivers.

## Webcams
- Privacy/permission block: Settings → Privacy & Security → Camera — app
  not listed or toggle off is the most common "camera doesn't work in
  Teams but works in Camera app" cause.
- Conferencing app camera lock conflicts: only one app can hold the camera
  at a time; a crashed app (check Task Manager) can leave the device
  "in use" after closing — kill the process rather than rebooting as a
  first step.

## Bluetooth
- Pairing failures: remove the device from both ends (Settings →
  Bluetooth & devices → Remove device, and the peripheral's own reset,
  usually a long button-hold) rather than just "pair again" — a stale
  pairing record on either side causes silent failures with no error.
- Driver vs radio: Device Manager → Bluetooth adapter → Disable/Enable
  resets the radio without a reboot; useful before escalating as hardware
  failure.

## Gotchas
- Docking station firmware updates are vendor-specific utilities (Dell,
  Lenovo, HP each have their own) — check for one before replacing a dock
  that intermittently drops displays.
- A monitor that works fine on a different port/cable but not the
  original one is a cable/port fault, not a settings issue — swap first,
  diagnose software second.

## Verify
- Dock/monitor combination holds the expected resolution and refresh rate
  through a sleep/wake cycle and a full reboot (not just immediately after
  the fix), audio defaults to the expected device, and camera/mic are
  available to the conferencing app without a restart.
