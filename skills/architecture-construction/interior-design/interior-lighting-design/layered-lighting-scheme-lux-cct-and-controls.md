---
id: architecture-construction.interior-design.interior-lighting-design.layered-lighting-scheme-lux-cct-and-controls
name: layered-lighting-scheme-lux-cct-and-controls
category: architecture-construction
field: interior-design
product: interior-lighting-design
tags: [interior-lighting-design, lighting-design, layered-lighting, ambient-lighting, task-lighting, accent-lighting, decorative-lighting, lux, illuminance, lumens, lumen-method, cct, colour-temperature, kelvin, cri, ra, r9, tm-30, beam-angle, glare, ugr, downlights, linear-led, led-tape, dimming, triac, 0-10v, dali, casambi, lighting-scenes, lighting-controls, dialux, relux, rcp, wall-washing]
level: practitioner
status: draft
description: "Design a layered interior lighting scheme: target lux by task, lumen-method sanity checks, CCT and CRI choice, beam angles and glare, and dimming/control protocols that actually work."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Layered lighting scheme: lux, CCT and controls

**Goal:** a room lit for what happens in it, comfortable to the eye, flattering to
people and finishes, and controllable — not a grid of downlights.

## 1. Layers
1. **Ambient** — general light so you can move safely: indirect, wall-washing, or
   diffuse fittings. Lighting vertical surfaces makes rooms feel brighter than
   pouring light on the floor.
2. **Task** — where eyes work: kitchen worktops, desks, mirrors, reading chairs.
3. **Accent** — art, texture, joinery, feature walls; typically ~3–5× the ambient
   level on the target to read as emphasis.
4. **Decorative** — pendants and lamps seen as objects; they set mood but rarely do
   the work.
Plan each layer on its own circuit/control channel.

## 2. How much light
Typical maintained illuminance targets (from guidance such as EN 12464-1 and IES
recommendations — check the current edition for your use):
- Office desk work ~300–500 lux; kitchen worktops ~300–500 lux; corridors ~100 lux;
  living rooms ~50–150 lux ambient with task lamps; bathrooms mirror area ~300 lux
  on the face.
**Lumen-method sanity check:** lamp lumens needed ≈ (target lux × area) ÷ (utilisation
factor × maintenance factor). With UF ~0.5 and MF ~0.8 for a typical room, a 20 m²
kitchen at 300 lux needs ~15,000 lm installed. Confirm properly with DIALux or Relux
for commercial work.

## 3. Colour
- **CCT:** ~2700 K warm for homes and hospitality, 3000 K for most mixed residential
  and retail, 3500–4000 K for offices and task-heavy spaces. Keep one CCT per space
  unless contrast is intentional. Consider dim-to-warm for living and dining.
- **CRI ≥ 90** (Ra), with good **R9** (saturated red) for skin tones, food, timber and
  art. TM-30 Rf/Rg give a fuller picture if suppliers publish it.
- Check the colour consistency (MacAdam step ≤ 3) so adjacent downlights match.

## 4. Fittings, beams and glare
- **Beam angle:** narrow (10–25°) for accent, medium (35–40°) for general downlight,
  wide (60°+) for wash. Wall-wash fittings sit ~ one-third of ceiling height from the wall
  as a starting rule.
- **Glare:** deep-recessed or low-glare optics; avoid bare LEDs in sightlines from
  sofas and beds. Commercial: check UGR limits (e.g. ≤ 19 for offices).
- Don't centre a downlight over a bath, bed head or sofa where people look up.
- Wet-zone IP ratings in bathrooms (local regs, e.g. IP65 in zone 1 in the UK).

## 5. Controls
- Choose the protocol with the electrician and the driver spec: **trailing-edge/TRIAC**
  phase dimming for simple domestic, **0–10 V / 1–10 V** or **DALI / DALI-2** for
  commercial and scenes, wireless (e.g. Casambi, Zigbee-based) for retrofit.
  Mismatched dimmer and driver = flicker and buzz — get compatibility lists.
- Program scenes (e.g. "cook", "dine", "evening", "clean"); add presence/absence
  and daylight sensors in commercial spaces where codes require.

## Gotchas
- A ceiling grid of downlights: bright floor, dark walls, gloomy room.
- Mixed CCTs from different suppliers.
- Cheap drivers on "dimmable" LEDs flickering at low levels.
- Task lights placed behind the user, casting their shadow on the work.

## Verify
- [ ] Each layer is on its own control channel.
- [ ] Lux targets met for tasks (calc or meter after install).
- [ ] One CCT per space; CRI ≥ 90 where colour matters.
- [ ] No direct glare from main seating/bed positions.
- [ ] Dimming tested smooth from 100% to minimum with the actual drivers.
