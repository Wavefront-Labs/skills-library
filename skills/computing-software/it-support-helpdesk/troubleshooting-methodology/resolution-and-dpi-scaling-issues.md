---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.resolution-and-dpi-scaling-issues
name: resolution-and-dpi-scaling-issues
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, dpi-scaling, resolution, high-dpi, blurry-apps, mixed-dpi, remote-desktop]
level: practitioner
status: draft
description: "Fix blurry or tiny apps and wrong resolutions: native resolution, Windows scale settings, per-app high DPI overrides, mixed-DPI multi-monitor quirks and RDP scaling."
sources:
  - "https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows"
  - "https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-properties"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# resolution-and-dpi-scaling-issues

## Start with the basics
- Settings > System > Display: Display resolution should say "(Recommended)", which is the
  panel's native resolution. Non-native looks soft everywhere.
- Scale (100/125/150/175%) changes size without blur. Recommended values are usually
  right; users with sight needs may go higher (see accessibility skill).
- Sign out after big scale changes; some apps only pick them up at sign-in.

## Blurry single apps
Older apps that are not DPI-aware get bitmap-stretched.
1. Settings > Display > Scale > "Let Windows try to fix apps so they're not blurry" on.
2. Per app: right-click the EXE > Properties > Compatibility > Change high DPI settings >
   tick "Override high DPI scaling behavior", Scaling performed by:
   - **Application**: sharp, but may be tiny or have overlapping UI.
   - **System**: consistent size, blurry.
   - **System (Enhanced)**: sharp text for GDI apps; can break some layouts.
3. Deploy a working choice at scale with the `AppCompatFlags\Layers` registry value
   (`HIGHDPIAWARE`, `DPIUNAWARE`, `GDIDPISCALING DPIUNAWARE`).

## Multi-monitor mixed DPI
Laptop at 150% plus external at 100%: windows dragged between screens can be blurry or
jump in size. Options: same scale on both, set the external as main display before
sign-in, or keep the problem app on one screen.

## Remote Desktop
- mstsc uses the client's scale by default; `desktopscalefactor:i:` and
  `smart sizing:i:1` in the .rdp file adjust it.
- Tiny text in RDP from a 4K laptop: set Display > "Use all my monitors" off and pick a
  scaled resolution, or set the scale factor property.

## Gotchas
- Docking and undocking changes DPI; some apps need restart to redraw correctly.
- Fonts look thin? Run ClearType Text Tuner (`cttune`).

## Verify
At native resolution and chosen scale, the problem app is sharp and correctly sized on
each monitor after sign-out/in and a dock cycle.
