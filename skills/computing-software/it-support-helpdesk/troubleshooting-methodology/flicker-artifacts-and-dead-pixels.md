---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.flicker-artifacts-and-dead-pixels
name: flicker-artifacts-and-dead-pixels
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, display-artifacts, flicker, dead-pixels, panel-self-refresh, refresh-rate, gpu]
level: practitioner
status: draft
description: "Diagnose screen flicker, artifacts and dead pixels: firmware-vs-OS isolation, refresh rate, cable and PSR causes, lid-flex tests for laptop cables, and pixel warranty policies."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# flicker-artifacts-and-dead-pixels

## First split: hardware or software
Look at the BIOS/UEFI setup screen or boot logo.
- Artifacts or flicker there too = hardware (GPU, panel, cable).
- Only inside Windows = driver, refresh rate, or app.
- Screenshot test: artifacts visible in a screenshot = GPU/driver; not in the screenshot =
  panel or cable.

## Flicker
- Set the native refresh rate (Settings > Display > Advanced display); turn off dynamic
  refresh rate to test.
- Intel laptops: Panel Self Refresh can cause flicker; disable it in Intel Graphics Command
  Center (Power) to test, then update the driver.
- Low brightness flicker on some panels is PWM dimming; raise brightness to confirm.
- External monitors: swap cable, use a certified cable for the resolution/refresh, and
  try another input.
- Fluorescent or LED room lighting can show flicker on camera only.

## Artifacts
- Coloured blocks, lines across the screen, or sparkles: update/clean-install the GPU
  driver (DDU in Safe Mode for stubborn cases). If artifacts appear in BIOS too, the GPU or
  its memory is failing.
- Display driver resets (`Display driver stopped responding and has recovered`, event 4101)
  point to driver or overheating GPU.

## Laptop panel and cable
Slowly open and close the lid while watching: flicker or lines that change with the hinge
angle mean a worn display cable. Pressing near the bezel changing the image = panel or
connector.

## Dead and stuck pixels
- Show solid red, green, blue, black and white full-screen images to map them.
- Stuck (always one colour) may recover; dead (always black) will not.
- Warranty depends on vendor pixel policy (many follow ISO 9241-307 classes; some offer
  zero bright dot guarantees). Record count and position for the claim.

## Verify
No flicker or artifacts across BIOS, Windows and a 10-minute video, at native resolution
and refresh, after a full restart.
