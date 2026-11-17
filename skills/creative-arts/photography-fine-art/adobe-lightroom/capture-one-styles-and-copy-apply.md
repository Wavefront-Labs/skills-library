---
id: creative-arts.photography-fine-art.adobe-lightroom.capture-one-styles-and-copy-apply
name: capture-one-styles-and-copy-apply
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, capture-one-styles, capture-one-workflow, copy-apply, presets, capture-one]
level: practitioner
status: draft
description: "Create and apply Capture One styles and presets, stack styles, use Copy and Apply with selective tool inclusion, and keep user styles organised."
sources: ["https://support.captureone.com/hc/en-us/articles/8808431952413-Using-Styles", "https://support.captureone.com/hc/en-us/articles/360002619458-Applying-Styles-and-Presets-to-Layers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture One styles and Copy/Apply

## Terms
- **Preset**: settings for a single tool (e.g. one Curve), saved from that tool's menu.
- **Style**: settings from several tools, like a Lightroom develop preset.

## Create a style
1. Edit an image. Styles and Presets tool > `+` > **Save User Style...**
2. Untick tools that should not be part of it: crop, white balance, exposure, metadata, keystone, and anything image-specific.
3. Name and group (sub-folders under User Styles).

## Apply
- Hover to preview, click to apply. Styles apply to the selected layer; recent versions can apply a style as a new layer, which then gets its own opacity.
- **Stack Styles** option (Styles tool menu) lets multiple styles accumulate; otherwise a new style replaces the old style's settings for the same tools.
- Only one style per layer when applying to layers; layers inside styles are supported in Capture One 23 and later.
- Apply at import: Import dialog > Adjustments > Styles.

## Copy and Apply
1. Select the edited image; Adjustments Clipboard tool or Ctrl/Cmd+Shift+C copies all adjustments.
2. In the clipboard, untick tools not to copy (crop, spot removal).
3. Select target images, Ctrl/Cmd+Shift+V to apply.
- **Edit Selected Variants** (toolbar toggle) applies slider changes to all selected images live, like Auto Sync.

## Sharing
- Styles are `.costyle` files; Import via the Styles tool menu. Location: Capture One support folder > Styles.

## Verify
- [ ] Applying the style to an unedited image changes only the intended tools (check the tools' reset arrows).
