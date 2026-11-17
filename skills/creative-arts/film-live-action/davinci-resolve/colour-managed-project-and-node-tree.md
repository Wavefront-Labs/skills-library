---
id: creative-arts.film-live-action.davinci-resolve.colour-managed-project-and-node-tree
name: colour-managed-project-and-node-tree
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, color-page, colour-page, node-grading, node-tree, serial-node, parallel-node, layer-mixer, color-management, colour-management, davinci-yrgb-color-managed, davinci-wide-gamut, rcm, aces, color-space-transform, cst, log, rec709, gamma-2-4, timeline-color-space, groups, pre-clip, post-clip, shared-nodes, scopes, waveform, parade, vectorscope, deliver-page, render-settings, rcm-setup, input-colour-space, colour-space-tagging, group-grading, pre-clip-group, post-clip-group, cst-node, colour-space-transform-use, manual-colour-management, render-settings-detail, data-levels]
level: practitioner
status: draft
description: "Set up DaVinci Resolve for a clean grade: colour management choices, a repeatable node tree for log footage, groups and shared nodes for scene consistency, scopes, and delivery checks."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour-managed project and node tree in DaVinci Resolve

**Goal:** a Resolve project where every camera's footage is converted into one working
space, every shot is graded through the same predictable node structure, and the output
is transformed correctly for its delivery. Craft of the grade itself (look, matching) is
in `creative-arts.film-live-action.color-grading.matching-shots-across-cameras-and-skin-tones`.

Menu paths refer to Resolve 18–19; they move between versions. Not verified against every release.

## 1. Choose colour management up front
Project Settings › Color Management, *before* grading (changing later shifts every grade):
- **DaVinci YRGB Color Managed (RCM):** Resolve reads camera metadata and converts input
  to a timeline/working space (e.g. *DaVinci Wide Gamut / DaVinci Intermediate*), then
  to an output space (e.g. *Rec.709 Gamma 2.4* for broadcast/grading-suite SDR). Simple and
  robust; check each clip's input colour space (right-click clip › Input Color Space) is right.
- **ACES (ACEScct):** standard for VFX-heavy work and facilities exchange; set the IDT per
  camera and the ODT for delivery.
- **DaVinci YRGB (unmanaged) + manual CSTs:** full control: add **Color Space Transform**
  OpenFX nodes at the start (camera log → working space) and end (working → display).
  Common among colourists; easy to forget a node on one clip.
Pick one approach per project and write it down.

## 2. A repeatable node tree
A widely used serial structure (use as a starting template, adjust as needed):
1. **Input CST** (if unmanaged).
2. **Exposure/balance** — offset or printer lights to set exposure and neutral balance.
3. **Contrast** — contrast/pivot or curves.
4. **Saturation / colour** adjustments.
5. **Secondaries** — qualifiers/windows for skin, sky, specific objects (parallel nodes
   for independent isolations).
6. **Look** — the creative look node (often shared).
7. **Output CST** (if unmanaged) and any display LUT.
Add serial nodes with `Alt+S` (Option+S on macOS); **label** every node (right-click ›
Node Label). Save the tree as a still in the Gallery and apply it to new shots so every
shot starts identical.

Work in the working (scene-referred, log-like) space for primaries; it makes adjustments
behave more like exposure changes on set.

## 3. Consistency tools
- **Groups:** put shots of a scene in a group; use the **Group Pre-Clip** for
  scene-wide balance, **Clip** for per-shot matching, **Group Post-Clip** for the scene
  look. Change the scene look once, everywhere.
- **Shared nodes** (right-click node › Save as Shared Node): the same node in many
  clips across scenes — good for a film-wide look.
- **Timeline-level nodes** for global output treatments (film grain, final trim).

## 4. Scopes, not eyes
Open scopes (Workspace › Video Scopes): **waveform/parade** for levels and balance,
**vectorscope** for hue and saturation (skin tones cluster near the skin-tone indicator line
when that overlay is enabled). Grade on a calibrated reference monitor via a video I/O
device where possible; GUI viewers on computer displays are not reliable references.

## 5. Delivery checks
On the Deliver page choose a preset or custom settings: format/codec as specified
(e.g. ProRes 422 HQ master), resolution, frame rate matching the timeline, data levels
(Video vs Full — "Auto" usually right for standard codecs), and the output colour space
tags. Render a short test section, watch it in a player on a second device, and compare
gamma (Mac QuickTime gamma shifts are a well-known source of "it looks washed out" — tag
correctly and judge on the reference monitor).

## Gotchas
- Changing colour management mid-project.
- Double conversion: RCM on *and* manual CSTs/LUTs, or a camera LUT baked in plus a CST.
- Grading with a display LUT on the viewer but not in the render.
- Unlabelled 20-node trees nobody, including you next week, can read.

## Verify
- [ ] Colour management method chosen, documented, and input spaces checked per camera.
- [ ] Every shot uses the same labelled node template.
- [ ] Scenes grouped with pre/post-clip structure or shared nodes for the look.
- [ ] Levels and skin checked on scopes and a reference monitor.
- [ ] Test render watched on a second device; colour tags and levels correct.
