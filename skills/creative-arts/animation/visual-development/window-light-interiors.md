---
id: creative-arts.animation.visual-development.window-light-interiors
name: window-light-interiors
category: creative-arts
field: animation
product: visual-development
tags: [visual-development, light-sources, window-light, interior-lighting, light-falloff, bounce-light]
level: practitioner
status: draft
description: "Paint window-lit interiors: directional soft light with rapid falloff, light pools on floors, bounce filling the room, and exposure choices for the window."
sources:
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://en.wikipedia.org/wiki/Inverse-square_law
  - https://en.wikipedia.org/wiki/Chiaroscuro
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Window light interiors

Goal: interiors lit by daylight through windows - the Vermeer light - with correct falloff
and bounce.

## Characteristics (Gurney)
- **Directional but soft**: the window is a large source; light is soft-edged and directional.
- **Falloff**: brightness drops quickly with distance from the window; far side of the room is dark.
- **Sky vs sun**: north-facing/skylight windows give cool even light; direct sun through a window
  makes a sharp warm patch on the floor/wall in the window's shape.
- **Bounce**: sunlit floor patches bounce warm light up onto ceilings and nearby faces.
- **Exposure**: if the interior is exposed correctly, the window blows out to near white;
  if the view outside is visible, the interior is darker.

## Method
1. Decide whether direct sun enters; draw the sun patch by projecting the window through the room.
2. Grade the room from the window: brightest near, darkening to the back.
3. Light characters by orientation to the window; side-lit faces have a strong light/shadow split.
4. Add bounce from sun patches and light walls.
5. Pick the exposure: blown window (mood) or visible view (story information).
6. Add dust motes or light shafts only if there is enough atmosphere.

## Failure modes
- Even fill throughout the room (no falloff).
- Sun patch in the wrong shape or direction relative to the window.
- Interior and the view outside both perfectly exposed with no reason.

## Verify
- [ ] Clear falloff from the window.
- [ ] Sun patch geometry correct.
- [ ] Exposure choice deliberate.

Related: `creative-arts.animation.visual-development.reflected-light-and-bounce-color`,
`creative-arts.animation.blender.light-portals`.
