---
id: creative-arts.film-live-action.premiere-pro.essential-graphics-titles-and-mogrts
name: essential-graphics-titles-and-mogrts
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, essential-graphics, essential-graphics-panel, mogrt, motion-graphics-template, titles, lower-thirds, type-tool, text-layer, shape-layer, responsive-design, responsive-time, pin-to, text-styles, master-styles, caption-styles, font-licensing, adobe-fonts, after-effects-mogrt, export-mogrt, local-templates, creative-cloud-libraries, credits-roll, rolling-credits, end-crawl, safe-margins, title-safe, action-safe, graphics-track, templates, brand-kit, text-layer-use, text-style-presets, font-management, mogrt-customisation, mogrt-install, rolling-credits-use, credit-crawl, responsive-design-use, responsive-position]
level: practitioner
status: draft
description: "Titles and lower thirds in Premiere Pro's Essential Graphics: type and shape layers, responsive pinning, text styles, installing and editing After Effects MOGRTs, rolling credits, safe margins."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/essential-graphics-panel.html (Adobe - Essential Graphics panel)"
  - "https://helpx.adobe.com/premiere-pro/using/motion-graphics-templates.html (Adobe - Motion Graphics templates)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional - Premiere Pro exam objectives, Domain 4)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Essential Graphics, titles and MOGRTs in Premiere Pro

**Goal:** consistent, legible graphics built once and reused across a show, editable
by anyone on the team without opening After Effects.

## 1. Build a title from scratch
`Window > Essential Graphics` > **Edit** tab. With the Program Monitor active, the
**Type tool** (`T`) click-drag creates a text box (click = point text, drag = paragraph
text); the graphic clip appears on the timeline above the playhead. In the Edit tab:
- **Layers**: text, shapes (Rectangle/Ellipse/Pen tool), images (drag from a bin);
  reorder by drag; group with `Ctrl/Cmd+G`.
- **Align and Transform**: align to the frame/selection, position, scale, rotation,
  opacity; the anchor point controls scale/rotation origin.
- **Text**: font, style, size, tracking, leading, kerning, alignment; **Appearance**:
  fill, stroke (multiple), background box (padding), shadow, mask with shape.
- **Responsive Design - Position**: pin a layer to another (a background box to the
  text) so the box grows when the name gets longer. **Responsive Design - Time**: set
  intro/outro durations that stay fixed when the clip is trimmed (animations keep their
  in/out behaviour).
- Animate in **Effect Controls** (`Shift+5`) per layer: position, scale, opacity
  keyframes; ease via right-click > Temporal Interpolation > Ease In/Out.
Name the graphic clip in the timeline so the Project panel is searchable.

## 2. Text styles and consistency
Make a **Text Style** (Essential Graphics > Text > Styles dropdown > *Create Style*) from
a formatted text layer; styles live in the Project panel and apply to any text layer
(select layer > choose style). Changing the style updates every user. For a show:
styles for *Name*, *Title*, *Location*, *Subtitle-style caption*. Use fonts the whole
team has (Adobe Fonts via Creative Cloud syncs automatically; otherwise install on every
machine - missing fonts substitute silently on another workstation).

## 3. Export your title as a MOGRT
Select the graphic clip > Essential Graphics > **Export As Motion Graphics Template**
(or right-click clip). Choose *Local Templates Folder* or a Creative Cloud Library,
tick *Include Video Thumbnail*, add keywords. The MOGRT keeps all layers editable
(text, colours, position). Install others' `.mogrt` files via the Browse tab's `+`
button; they appear in *Local Templates*.

## 4. After Effects MOGRTs
AE-built templates (from a motion designer, Adobe Stock, or your own): in AE the
designer adds controls to the **Essential Graphics panel** (text source, colour,
sliders, dropdowns, media replacement) and exports a `.mogrt`. In Premiere, drag from
Browse to the timeline; edit exposed controls in the Edit tab. Heavy AE MOGRTs render
slowly on the Premiere timeline - render and replace (`Clip > Render and Replace`)
once approved, or ask for *Replace with After Effects Composition* only if you need to
change what wasn't exposed.

## 5. Rolling credits
Essential Graphics > *Roll* checkbox (in the Edit tab with the graphic selected):
*Start Offscreen*, *End Offscreen*, *Preroll/Postroll*, *Ease In/Out*. Paragraph text
with tab stops (`Window > Text` panel or tab stops in the Essential Graphics text
options) aligns roles and names. Speed = clip duration; for broadcast, keep roll speed
readable (around 1 line/second at 1080p is legible). Export credits as ProRes 4444 with
alpha if a finishing house needs them, with the roll rendered at the delivery frame
rate (rolls judder at mixed rates - keep the sequence at the delivery rate).

## 6. Safe margins and legibility
Program Monitor wrench > *Safe Margins* (action safe 90%, title safe 80% for broadcast;
streamers often 95/90). Minimum text sizes ~24 px at 1080 for lower thirds; contrast via
stroke/shadow/background box; avoid thin weights on moving backgrounds; keep lower thirds
under 5 seconds unless the name must be read twice.

## Gotchas
- Pinning not set: lengthening a name overflows the box.
- Fonts missing on the colourist's/assistant's machine; titles re-render in Arial.
- Text typed in the legacy Title Designer (older projects) - rebuild in Essential Graphics.
- MOGRT with dozens of exposed controls that nobody documents.
- Interlaced/rolling credits exported at a different frame rate; strobing.

## Verify
- [ ] Titles use responsive pinning and show-wide text styles.
- [ ] Reusable graphics exported as MOGRTs in a shared library/folder.
- [ ] Fonts available on every machine (Adobe Fonts or installed).
- [ ] Safe margins respected; credits roll legible at delivery frame rate.
