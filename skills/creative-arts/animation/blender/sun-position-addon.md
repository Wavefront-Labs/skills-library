---
id: creative-arts.animation.blender.sun-position-addon
name: sun-position-addon
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, sun-position-addon, sun-position, sky-texture, extensions]
level: practitioner
status: docs-checked
description: "Use the Blender Sun Position extension: Sun Object Mode and Environment Mode from the World Properties editor, place and animate the Sun from location, date and time."
sources:
  - https://extensions.blender.org/add-ons/sun-position/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sun-position-addon

## Install

Sun Position is an extension on extensions.blender.org (formerly bundled with Blender): drag the download into Blender, or use Install from Disk. The listing shows compatibility with Blender 4.2 LTS and newer and version 4.4.0 (3 Nov 2025) when checked; licence GPL 3 or later. Check the listing for the current version.

## Where and how

Set it up from the **World Properties** editor. It positions and animates the Sun from physical characteristics: geographic location, time and date. The calculations are based on NOAA's online calculator (itself based on Meeus, Astronomical Algorithms), so accuracy is "to a certain degree". Two modes:

- **Sun Object Mode** (the default): after choosing time and place you can set up a sun light, a sky texture and a collection used for visualisation; they are positioned or animated from the chosen date, time and place. Use this to animate the Sun realistically.
- **Environment Mode**: does not simulate a real location and time. It locks an environment texture and a sun light object together so they rotate at the same time; useful for adding contrast to an HDRI by adding a sun.

## Practice notes

- Match the scene's north to the site plan; do not assume the default orientation is correct.
- The add-on positions the Sun; set sun strength and sky brightness yourself, by eye or exposure.
- Add-on property names used in scripts may change between extension versions; test after updating.
- Sanity check (astronomy): at solar noon in the northern hemisphere the sun elevation is about 90 degrees minus latitude plus solar declination.

## Verify

Change the time and confirm the sun light and sky texture move together; in Environment Mode confirm the HDRI and the sun rotate together.

## Checked

Checked 2026-10-27 against the extensions.blender.org Sun Position listing (description, Sun Object Mode and Environment Mode, World Properties usage, version 4.4.0, compatibility 4.2 LTS and newer, GPL 3+). Removed the earlier "Normal / Sky Texture / HDRI" usage-mode names, property names such as North Offset and Distance, the N-panel View tab location, and the example coordinates, none of which the listing confirms. Method: documentation only; no commands were run.
