---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.no-image-black-screen-isolation
name: no-image-black-screen-isolation
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, no-display, black-screen, post, graphics-driver, display-troubleshooting, backlight]
level: practitioner
status: draft
description: "Isolate a black screen in order: power and POST signs, monitor, cable and port, external display, graphics driver reset and Safe Mode, and black screen with cursor after login."
sources:
  - "https://www.comptia.org/en/certifications/a/core-1-v15/"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# no-image-black-screen-isolation

## Split the problem: no POST, no signal, or no Windows
1. **Signs of life**: power LED, fans, keyboard Caps Lock toggling, beep or diagnostic LED
   codes. No signs = power problem. Codes = look them up for that model (often RAM).
2. **POST but no picture**: you hear startup/feel disk activity, but the screen is dark.
3. **Logo shows, then black**: Windows/driver side.

## Hardware path
- Monitor on, correct input selected, brightness up; try the monitor with another device.
- Swap cable; reseat both ends. Try another port type (DP vs HDMI).
- Desktop with a graphics card: cable must go to the card, not the motherboard port.
- Laptop: connect an external monitor and press `Win`+`P` > Duplicate. External works and
  internal is dark = panel, backlight, or cable; shine a torch at the panel to see a faint
  image (dead backlight).
- No POST picture on any display: reseat RAM, remove add-in cards, clear CMOS.

## Windows path
- `Win`+`Ctrl`+`Shift`+`B` restarts the graphics driver (beep and flash means it ran).
- `Win`+`P` pressed blindly then Enter cycles projection mode if output went to a missing
  display.
- Boot to WinRE > Startup Settings > Safe Mode (or low-resolution video). Picture in Safe
  Mode = driver; roll back or reinstall via Device Manager / vendor driver.
- Black screen with a mouse cursor after login: `Ctrl`+`Shift`+`Esc` > Run new task >
  `explorer.exe`. If that works, look at shell replacements, startup items, or a corrupt
  profile.

## Gotchas
- Docks are a frequent culprit; test direct to the laptop.
- Fast Startup can resume a broken display state; do a full restart (Shift+Restart).
- 4K at 60 Hz needs HDMI 2.0 or DisplayPort; older adapters output nothing at that mode.

## Verify
Picture from POST through login on the intended display, after a full restart and a
sleep/wake cycle.
