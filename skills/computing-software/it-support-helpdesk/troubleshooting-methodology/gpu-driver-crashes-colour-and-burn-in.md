---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.gpu-driver-crashes-colour-and-burn-in
name: gpu-driver-crashes-colour-and-burn-in
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, gpu-driver, color-calibration, burn-in, tdr, display-driver, image-retention]
level: practitioner
status: draft
description: "Fix GPU driver crashes and TDR resets, colour accuracy and calibration problems, and burn-in or image retention on OLED and LCD screens."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery"
  - "https://support.microsoft.com/en-us/windows/calibrate-your-display-49c27a43-d3d7-1a61-50f6-f1a8ab8a4f91"
  - "https://www.lg.com/us/support/help-library/oled-tv-image-retention-CT10000018-20150626646306"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# gpu-driver-crashes-colour-and-burn-in

## GPU driver crashes and TDR
- "Display driver stopped responding and has recovered", screen flashes black, apps
  crash with GPU errors: Timeout Detection and Recovery (TDR) reset the GPU after it hung
  (default 2 seconds). Event ID 4101 (Display) in the System log; LiveKernelEvent 141/117
  in Reliability Monitor.
- Steps:
  1. Install the OEM-supplied or current WHQL driver from the GPU vendor (laptops:
     OEM driver first, newer vendor driver if issues persist).
  2. Clean install for persistent corruption: Display Driver Uninstaller in safe mode,
     then install.
  3. Check temperatures and dust; laptop on a hard surface; GPU fans spinning.
  4. Turn off app-level hardware acceleration (browsers, Teams, Office) to confirm.
  5. Hybrid graphics: set the app to the right GPU in Settings > Display > Graphics.
  6. Stress test (vendor tool or a benchmark) to separate hardware from driver.
- Don't raise `TdrDelay` as a fix except for specific compute workloads advised by the
  vendor.

## Colour accuracy and calibration
- Wrong colours everywhere: check cable/input (limited vs full RGB range in the GPU
  control panel; YCbCr over HDMI can wash out text), monitor picture mode, Night light
  or blue-light filters, HDR on for SDR content.
- Calibrate: Windows Display Color Calibration (`dccw`) for basics; designers need a
  hardware colorimeter (Calibrite, Datacolor) creating an ICC profile; Windows Color
  Management (`colorcpl`) to set the profile per display; Auto Color Management on
  supported devices.
- One app wrong but others fine: app colour management settings or embedded profile.
- Check both screens of a dual setup are the same model/panel before chasing matching.

## Burn-in and image retention
- **Image retention** (temporary ghost of static elements) fades after showing other
  content; LCD and OLED. **Burn-in** (permanent) is mainly OLED: taskbars, logos, menu
  bars.
- Fix retention: display varied content or a full-screen white/colour cycle for a while;
  OLED panels run a pixel refresher (in the monitor menu or automatically on standby;
  don't unplug them immediately after turning off).
- Prevent: auto-hide taskbar, dark mode, screen saver / screen off after inactivity,
  moving static dashboards periodically (signage), lower brightness.
- Permanent burn-in under warranty: check vendor burn-in coverage (varies).

## Verify
No new 4101 events after a week of normal use; colours match the reference or profile;
retention gone after refresh, and prevention settings applied.
