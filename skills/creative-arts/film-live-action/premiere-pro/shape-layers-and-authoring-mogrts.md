---
id: creative-arts.film-live-action.premiere-pro.shape-layers-and-authoring-mogrts
name: shape-layers-and-authoring-mogrts
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, shape-layer-use, graphic-layers, shape-animation, mogrt-creation, after-effects-essential-graphics, mogrt-authoring, essential-properties, responsive-design]
level: practitioner
status: draft
description: "Build graphics with Premiere's shape and graphic layers, animate them, and author Motion Graphics templates in After Effects with exposed Essential Properties for editors."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/create-shapes-text.html (Adobe - Shapes and text in Premiere Pro)"
  - "https://helpx.adobe.com/after-effects/using/creating-motion-graphics-templates.html (Adobe After Effects - Creating Motion Graphics templates)"
  - "https://helpx.adobe.com/premiere-pro/using/responsive-design.html (Adobe - Responsive Design time and position)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shape layers and authoring MOGRTs

**Goal:** lower thirds, callouts and title cards built quickly in Premiere - and
reusable, brand-safe templates authored in After Effects that editors can change
without breaking.

## 1. Graphics and shape layers in Premiere
- **Rectangle/Ellipse/Pen** tools in the Program Monitor create a **graphic clip** with
  shape layers; the **Type** tool adds text layers. Layers stack inside one graphic clip
  (Essential Graphics panel > Edit tab).
- Properties: fill, stroke, shadow, mask with text, alignment; **Responsive Design -
  Position** (pin a shape to text so a background bar resizes with the words) and
  **Time** (protect intro/outro durations when the clip is stretched).
- Animate per layer in **Effect Controls** (Vector Motion / position, scale, opacity
  keyframes with easing).
- Save as a template: select the graphic > *Graphics > Export As Motion Graphics Template*
  (Premiere-authored MOGRTs, simpler than AE ones).

## 2. Authoring MOGRTs in After Effects
1. Build the composition (animation, styles) in AE.
2. Open **Essential Graphics** panel (Window > Essential Graphics), choose the master
   comp, name the template.
3. Drag properties into the panel to expose them: **Source Text**, colours, checkboxes
   (on/off elements), sliders (e.g. size), dropdown menus (layout variants - driven by
   expressions), media replacement placeholders.
4. Group controls, add comments; set **Responsive Design - Time** (protected regions) so
   editors can change duration without speeding up animations.
5. **Export Motion Graphics Template** to the local templates folder or a CC Library for
   the team.

## 3. Using them in Premiere
Essential Graphics > Browse: drag the template to the timeline; edit exposed controls in
the Edit tab. Replace fonts check: MOGRT fonts must be installed on editors' machines
(Adobe Fonts sync helps).

## 4. Template hygiene
Version names (`LowerThird_v3`), test with long names and different languages, keep
safe margins (title safe 90%), document what each control does.

## Gotchas
- Text overflowing because responsive design wasn't set.
- Missing fonts on other machines.
- Overexposed controls letting editors break brand rules.
- AE expressions slow to render in Premiere - pre-render or simplify.

## Verify
- [ ] Shapes pinned responsively; animation eased.
- [ ] MOGRT controls minimal and labelled; protected time regions set.
- [ ] Fonts available on all machines; library shared.
- [ ] Tested with extreme text lengths.
