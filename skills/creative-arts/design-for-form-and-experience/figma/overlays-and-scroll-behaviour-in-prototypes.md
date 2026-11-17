---
id: creative-arts.design-for-form-and-experience.figma.overlays-and-scroll-behaviour-in-prototypes
name: overlays-and-scroll-behaviour-in-prototypes
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [prototype-overlays, scroll-behavior, figma-overlays, fixed-position, sticky-header, overflow-scrolling, prototype-scroll, figma]
level: practitioner
status: draft
description: "Prototype overlays (modals, menus, toasts) and scrolling in Figma: overlay position and dismissal, scroll direction, fixed elements, nested scroll and scroll-to actions."
sources:
  - "Figma Help Center - Overlays (help.figma.com/hc/en-us/articles/360039829753)"
  - "Figma Help Center - Scroll and overflow behaviour (help.figma.com/hc/en-us/articles/360040449873)"
  - "Figma Help Center - Fix position when scrolling (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overlays and scrolling in prototypes

## Overlays
- Create the overlay as a **separate frame** (modal, bottom sheet, menu, toast). Add a connection **Open overlay** on the trigger.
- **Position:** Manual (relative to trigger or fixed), **Top left, Top center, Top right, Center, Bottom left/center/right**; **Close when clicking outside** (dismiss on scrim click); **Add background** (colour and opacity) for a scrim.
- **Close overlay** action on buttons inside; **Swap overlay** replaces the current overlay (steps in a wizard sheet); animation (Move in from bottom, Dissolve, Smart animate) per overlay.
- **Nested overlays** are allowed but keep stack shallow; closing returns to the underlying frame.
- Overlays suit tooltips, dropdowns, dialogs and snackbars (`creative-arts.design-for-form-and-experience.interaction-design.designing-modal-dialogs`).

## Scrolling
- Select a frame, in Prototype tab **Overflow scrolling:** No scrolling, Horizontal, Vertical, or Both. The frame's **height must be smaller than its content** (children extend beyond the frame; clip content) for scrolling to occur in Present.
- **Fixed elements:** select a child layer, enable **Fix position when scrolling** (headers, bottom tab bars, FABs). Fixed layers stay on top of scrolling content; place them at the top of the layer order.
- **Nested scrolling:** a horizontal carousel (frame with overflow horizontal) inside a vertically scrolling page works; the parent and child both scroll in their directions.
- **Scroll to** action: jumps to a layer in a scrolling frame (anchor links, back to top, form validation jumps).
- **Sticky behaviour:** achieve section headers with fixed position or separate overlays.
- **Device presets:** use the correct frame height so the scroll viewport matches the device; set the device frame in prototype settings.

## Pitfalls
- Overlay not opening: the target frame must be a top-level frame, not nested; trigger layer must be inside a frame with the interaction.
- Fixed elements below the content in layer order disappear behind it.
- Scrolling frames cannot be inside **auto layout** for clipping unless sized correctly; use a fixed-height clipped frame.

## Verify
- [ ] Overlays open, position, dim and close as designed.
- [ ] Scroll directions, fixed elements and anchors work in Present.
- [ ] Tested on device viewport sizes.
