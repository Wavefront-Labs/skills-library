---
id: natural-sciences.amateur-astronomy.stellarium.planning-an-observing-session
name: planning-an-observing-session
category: natural-sciences
field: amateur-astronomy
product: stellarium
tags: [stellarium, planetarium-software, observing-plan, session-planning, location-settings, light-pollution, bortle, landscape, time-controls, ocular-plugin, oculars, field-of-view, eyepiece-simulation, telescope-control, ascom, indi, goto, observing-list, object-search, night-mode]
level: intro
status: docs-checked
description: "Use Stellarium to plan a night: set location and light pollution, scrub time to find when targets are high, simulate your eyepiece with Oculars, optionally drive a GoTo mount."
sources: ["https://stellarium.org/guide/", "https://github.com/Stellarium/stellarium/blob/master/guide/app_hotkeys.tex", "https://github.com/Stellarium/stellarium/blob/master/guide/ch_interface.tex", "https://github.com/Stellarium/stellarium/blob/master/guide/ch_plugins.tex"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning an observing session in Stellarium

**Goal:** arrive at the telescope knowing what will be well placed, when, and what it will
look like in your eyepiece or sensor, and optionally let Stellarium point the mount.
Menu names and keys follow the current User Guide; check the guide for your installed version.

## 1. Set it up once
- **Location:** press F6 for the Location window. To keep a location, tick "use as
  default" and untick "Get location from Network". Wrong location means wrong rise/set times.
- **Time zone:** locations carry a time zone; daylight saving applies when "Enable daylight
  saving time" is selected, and "Use custom time zone" offers others (zones starting UTC
  have no daylight rules). If times look an hour off, check this.
- **Landscape:** View settings window (F4 is "Sky and viewing options") > Landscape tab.
  Custom landscapes are installed from ZIP files through "Add/remove landscapes".
- **Light pollution:** three modes: automatic from the locations database, manual slider
  (a tooltip shows the Bortle class and naked-eye limiting magnitude), or manual from a
  Sky Quality Meter reading.

## 2. Find when targets are well placed
- Search with F3 (Object tab: type a name, press Enter to centre on it).
- Time controls: J slows, L speeds, K returns to normal rate, 8 sets time to now; = and -
  add or subtract a solar day; ] and [ add or subtract 7 solar days. Scrub through the
  night to see when each target is highest.
- Check the Moon's phase and position against your targets.
- Comets and asteroids: the guide has a Solar System Editor plugin section; update orbital
  data before a session as that section describes.

## 3. Simulate the view: Oculars plugin
1. Plugins are enabled in Configuration > Plugins tab: select the plugin, tick "Load at
   startup", restart Stellarium.
2. Enter your telescopes and eyepieces in the plugin's configuration (see the guide's
   Oculars section).
3. Ctrl+O is the Ocular view hotkey; Alt+O opens the Oculars popup menu.

## 4. Observing lists
The guide lists Observing Lists (Bookmarks) as a feature; enable the dialog from the
Extras tab of the configuration. Check the guide for what it can save.

## 5. Telescope control
- The TelescopeControl plugin section of the guide lists RTS2, INDI, ASCOM (Windows only)
  and StellariumScope as ways to connect.
- Ctrl+1 to Ctrl+9 move telescope number 1 to 9 to the selected object; Ctrl+0 moves a
  telescope to coordinates you enter.
- Align the mount with its own routine first, and check its location and time match Stellarium's.

## 6. At the eyepiece
Ctrl+N toggles night mode. A laptop screen still glows: dim it as far as it goes.

## Gotchas
- Default location left at the wrong place.
- Ocular field of view wrong because the eyepiece data was mis-entered.
- Stale comet and asteroid elements.

## Verify
- [ ] Location, elevation and time zone checked against a known rise or set time.
- [ ] Each target's best time noted; running order planned around the Moon.
- [ ] Ocular view matches what you see in the eyepiece.
- [ ] A GoTo slew lands the target in the field (if using telescope control).

## Checked
2026-11-01. Confirmed in the Stellarium User Guide (table of contents) and its source files
app_hotkeys.tex, ch_interface.tex and ch_plugins.tex: F6, F3, F4, Ctrl+N, Ctrl+O, Alt+O,
Ctrl+0 to Ctrl+9, time hotkeys, location default and time zone options, Landscape tab, three
light pollution modes, plugin enabling steps, TelescopeControl connection list. Removed (not
stated in pages read): landscape.ini layout, altitude rules of thumb, Telrad overlay,
JSON export of lists, NexStar, LX200 and SynScan protocol names, red-mode wording, phone and
desktop alternatives.
Method: documentation only; no commands were run.
