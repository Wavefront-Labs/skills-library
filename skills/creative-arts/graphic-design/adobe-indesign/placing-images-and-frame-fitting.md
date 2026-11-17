---
id: creative-arts.graphic-design.adobe-indesign.placing-images-and-frame-fitting
name: placing-images-and-frame-fitting
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-graphics, frame-fitting, frame-fitting-options, fill-frame-proportionally, auto-fit, content-grabber, place-gridified, image-frames]
level: practitioner
status: draft
description: "Place images in InDesign efficiently: multi-place and gridified placing, frame vs content selection, fitting commands, Frame Fitting Options with Auto-Fit and crop reference."
sources:
  - https://helpx.adobe.com/indesign/using/placing-graphics.html
  - https://helpx.adobe.com/indesign/using/cropping-masking-graphics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Placing images and frame fitting

**Goal:** images placed, cropped and fitted consistently, and frames that refit automatically when resized.

## Placing
- Ctrl/Cmd+D, select one or many files. The cursor holds a thumbnail stack; arrow keys cycle.
- Click = place at 100%; drag = place into a frame of that size; click inside an empty frame = fill it.
- **Gridified placing:** while dragging, press arrow keys to make a grid of frames (Right/Left
  = columns, Up/Down = rows; Ctrl/Cmd+arrows changes gutter) and drop many images at once.
- Placeholder frames: draw frames on parent pages or with the Rectangle Frame tool (F), give
  them an object style with fitting options, then place.

## Frame vs content
A placed image is two objects: the **frame** (crop) and the **content** (image). The
Selection tool selects the frame; the **content grabber** (donut in the middle) or the
Direct Selection tool selects the image inside. Double-click toggles.

## Fitting commands (Object > Fitting, or Control panel buttons)
| Command | Shortcut | Use |
|---|---|---|
| **Fill Frame Proportionally** | Alt+Shift+Ctrl+C / Opt+Shift+Cmd+C | Default for photos: fills, crops excess |
| Fit Content Proportionally | Alt+Shift+Ctrl+E / Opt+Shift+Cmd+E | Show whole image (logos, diagrams) |
| Content-Aware Fit | Alt+Ctrl+X / Opt+Cmd+X | Sensei guesses the crop: check it |
| Center Content | Shift+Ctrl+E / Shift+Cmd+E | |
| Fit Frame to Content | Alt+Ctrl+C / Opt+Cmd+C | Frame hugs image |
| Fit Content to Frame | Alt+Ctrl+E / Opt+Cmd+E | **Distorts** - avoid for photos |

## Frame Fitting Options (Object > Fitting > Frame Fitting Options)
- **Auto-Fit** on: resizing the frame keeps the image fitted (great for responsive or adjusted layouts).
- **Fitting on Empty Frame:** Fill Frame Proportionally - then placed images fit automatically.
- **Align From** (reference point): top-centre for portraits keeps heads in frame.
- **Crop Amount** for trimming white borders on supplied images.
Put these in an **object style** so all image frames share them.

## Gotchas
- Scaling the frame with the Selection tool without Auto-Fit only crops; hold Ctrl/Cmd while
  dragging to scale frame and content together (add Shift for proportion).
- Check **effective ppi** after scaling (Info or Links panel): >= 300 for print photos.

## Verify
- [ ] No distorted images (horizontal and vertical scale equal in Control panel).
- [ ] Image frames use an object style with fitting options.
- [ ] Effective ppi acceptable for every image.
