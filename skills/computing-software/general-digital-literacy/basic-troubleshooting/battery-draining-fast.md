---
id: computing-software.general-digital-literacy.basic-troubleshooting.battery-draining-fast
name: battery-draining-fast
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, mobile-devices, battery-drain, battery-health, low-power-mode]
level: intro
status: docs-checked
description: "Cut battery drain on a Mac laptop or check iPhone battery health: Low Power Mode, display timeout, Wi-Fi and Bluetooth, background apps, and when Apple says to service it."
sources:
  - https://support.apple.com/guide/mac-help/optimize-your-mac-battery-life-mh35848/mac
  - https://support.apple.com/en-us/101575
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Battery draining fast

**Goal:** a full day on one charge again, or a clear decision to replace the battery.

## Mac laptop (Apple's "Save energy on your Mac")
- System Settings > **Battery**: *Low Power Mode* can be Always, Only on Battery, or Only on Power Adapter. Next to *Battery Health* turn on **Optimized Battery Charging** and "Manage battery longevity". **Options** has "Put hard disks to sleep when possible" and "Automatic graphics switching".
- System Settings > **Lock Screen**: set *Turn display off on battery when inactive* (and the power-adapter equivalent).
- Dim the display to the lowest comfortable level (brightness keys or Displays settings).
- Turn off Wi-Fi and Bluetooth when not needed (they use energy even when idle).
- Disconnect unused accessories and external drives, and quit apps you are not using; apps can work in the background and use energy.
- Mac desktops use System Settings > **Energy** instead of Battery.

## iPhone (Apple's "iPhone battery and performance")
- Settings > **Battery** > **Battery Health** shows maximum battery capacity (capacity compared with when the battery was new) and peak performance capability.
- Apple designs iPhone 14 and earlier batteries to keep 80 percent of original capacity at 500 complete charge cycles, and iPhone 15 batteries at 1000, under ideal conditions; the real figure depends on use and charging.
- If Battery Health says the battery is significantly degraded, an Apple Authorized Service Provider can replace it. Battery service is covered by the one-year warranty if defective (two years in Turkiye) and otherwise Apple offers it for a charge.

## Other devices
Windows and Android battery screens differ by version and maker; check the maker's or Microsoft's support pages for your version.

## Verify
- [ ] The device's battery settings show the options above applied, and battery health has been checked.

## Checked
Checked 2026-10-27 against the Apple Mac User Guide "Save energy on your Mac" (macOS 27 Golden Gate page set) and Apple Support "iPhone battery and performance" (101575). Confirmed: Mac Battery, Lock Screen and Energy menu items and options, iPhone Settings > Battery > Battery Health, 80 percent at 500 or 1000 cycles, service wording. Removed unconfirmed claims (Windows Battery usage and powercfg battery report, Android menus and dial code, 70 percent laptop threshold, swollen-battery advice, Activity Monitor, background refresh and location advice, indexing after updates).
Method: documentation only; no commands were run.
