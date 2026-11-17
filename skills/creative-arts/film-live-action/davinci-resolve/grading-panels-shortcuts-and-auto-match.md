---
id: creative-arts.film-live-action.davinci-resolve.grading-panels-shortcuts-and-auto-match
name: grading-panels-shortcuts-and-auto-match
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, grading-panel, resolve-shortcuts, micro-panel, mini-panel, auto-colour, shot-match-tool, colour-chart-match, color-match, keyboard-grading]
level: practitioner
status: draft
description: "Grade fast in Resolve: Micro/Mini/Advanced panel workflows, essential Color page shortcuts, Auto Balance, Shot Match and Color Match against charts."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Control panels; Color Match; Shot Match; keyboard shortcuts)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/panels (DaVinci Resolve Micro, Mini and Advanced panels)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grading panels, shortcuts and auto match

**Goal:** speed - hundreds of shots a day - by keeping hands on controls and letting
Resolve's automatic tools do first passes.

## 1. Panels
- **Micro Panel**: 3 trackballs/rings (lift, gamma, gain) + 12 knobs (contrast, pivot,
  saturation, hue, lum mix, etc.) + transport/navigation keys. Ideal for primaries.
- **Mini Panel**: adds screens and soft keys for node operations, windows, qualifiers,
  and palette switching.
- **Advanced Panel**: full control including trackers, memories, gallery.
- Trackballs = colour, rings = level; a gentle grip makes fine moves; panels let you
  adjust two ranges simultaneously.
- Third-party (Tangent Elements/Ripple, Loupedeck) via Resolve's control panel settings.

## 2. Keyboard shortcuts (Color page, default mapping)
- `Alt/Opt+S`: add serial node; `Alt+P` parallel; `Alt+L` layer; `Alt+O` outside node.
- `Ctrl/Cmd+D`: disable/enable current node; `Shift+D`: bypass all grading (before/after).
- `Down/Up` arrows: next/previous clip; `Ctrl/Cmd+W`: toggle wipe.
- Middle-click a clip thumbnail: copy its grade onto the current clip; `=` applies the
  grade from the previous clip; `Ctrl/Cmd+C` then `Ctrl/Cmd+V` on selected thumbnails
  copies/pastes a grade.
- Verify and remap in *DaVinci Resolve > Keyboard Customization* - mappings change
  between versions.
Print or customise a mapping and learn ten that cover 90% of moves.

## 3. Auto tools
- **Auto Balance** (`A` in Primaries): neutralises a shot automatically - start point.
- **Shot Match**: select target clips, right-click the reference > *Shot Match to This
  Clip* - matches overall balance/contrast; review and refine.
- **Color Match** palette: shoot a chart; choose the chart type (X-Rite ColorChecker,
  DSC SpyderCheckr...), source gamma/gamut and target, align the overlay on the chart in
  the viewer, **Match** - produces a balancing correction.
- **Magic Mask/ AI Scene tools** for secondary isolation (see secondaries skill).
Auto results go on a dedicated node labelled "auto" so you can disable/compare.

## 4. Workflow rhythm
First pass: balance every shot fast (Auto/ panel), then match scene by scene with stills
(Gallery) and split screens, then looks, then secondaries.

## Gotchas
- Trusting Auto Balance on images with a dominant colour (sunset, neon) - it neutralises
  the mood away.
- Color Match with the wrong source gamma/gamut - wild results.
- Shortcut maps different between suites; customise and export your layout.
- Panels not configured after an update - check control panel settings.

## Verify
- [ ] Panel connected and mapped; shortcuts practised.
- [ ] Auto tools on separate labelled nodes.
- [ ] Color Match settings match the footage's gamma/gamut.
- [ ] Every shot balanced before look work.
