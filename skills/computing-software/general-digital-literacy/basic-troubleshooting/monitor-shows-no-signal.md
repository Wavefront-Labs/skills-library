---
id: computing-software.general-digital-literacy.basic-troubleshooting.monitor-shows-no-signal
name: monitor-shows-no-signal
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [no-display-signal, no-signal, monitor-troubleshooting, display-cable, hdmi]
level: practitioner
status: draft
description: "Fix a monitor reporting no signal: check cable and input, wake the graphics output, reseat connectors, test another cable or device, and isolate monitor versus PC."
sources: ["https://support.microsoft.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitor shows no signal

## Quick checks (2 minutes)
1. Is the PC actually on and awake? Press a key / move the mouse; check power LED and fans.
2. On the monitor choose the correct input (HDMI/DisplayPort/USB-C) from its menu; set to auto if available.
3. Reseat both ends of the cable; ensure the monitor is powered.
4. Desktop PC: the cable must be in the graphics card, not the motherboard port, if a graphics card is fitted.

## Isolate
5. Try a different cable and a different port on the monitor and PC.
6. Connect the monitor to another device (laptop, console): works there means the PC is the problem; still no signal means the monitor or cable.
7. Try another monitor or TV on the PC.

## PC-side fixes
- Windows: **Win + P**, select Duplicate/PC screen only (blindly press Down and Enter after a few seconds if you cannot see). **Win + Ctrl + Shift + B** restarts the graphics driver and beeps.
- Restart; boot into safe mode if the screen appears only at the sign-in stage, then roll back or reinstall the display driver.
- Desktop: power off, unplug, reseat the graphics card and memory, clear CMOS only if you are comfortable; laptops: hold power 30 seconds to drain, remove the charger and battery if removable.
- High refresh rate or resolution set too high for the cable: use a lower mode (boot with a different cable/monitor first).

## When to repair
No picture on any monitor and no POST beeps/lights after reseating suggests failed graphics, RAM or motherboard: seek repair or warranty service.

## Verify
Signal appears and stays through a restart.
