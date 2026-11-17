---
id: creative-arts.animation.blender.channel-luminance-key
name: channel-luminance-key
category: creative-arts
field: animation
product: blender
tags: [blender, keying, keyer, mattes, channel-key, luminance-key]
level: practitioner
status: docs-checked
description: "Quick mattes in the compositor: Channel Key (Color Space, Key Channel, Limit Method) and Luminance Key (Minimum, Maximum), when to prefer Screen or Add instead, and tuning."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/channel_key.html
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/luminance_key.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# channel-luminance-key

Goal: quick mattes from channel or brightness differences.

## Channel Key node (Keying category)

Separates background from foreground by the levels of a selected channel.
- **Color Space**: RGB, HSV, YUV or YCbCr.
- **Key Channel**: the channel (defined by the colour space) used for the matte.
- **Limit Method**: **Max** limits by the maximum of the other two channels; **Single** limits by the chosen **Limit Channel**.
- **Minimum**: lowest value considered foreground (from this value to 1.0). **Maximum**: highest value considered background (0.0 to this value). A gap between them gives a gradient of transparency.
- Outputs: **Image** (with adjusted alpha) and **Matte** (black and white).
The manual's example use is stock footage of explosions, shot against a dark background, keyed in YUV.

## Luminance Key node (Keying category)

Separates by brightness. **Minimum** is the lowest value considered foreground (light, from this value to 1.0); **Maximum** the highest value considered background (dark, 0.0 to this value). Levels in between form a gradient of transparency. Outputs: Image and Matte.
The manual notes it suits smoke, debris and explosion footage on dark backgrounds, and sky replacement for overexposed or grey skies. For light-emitting elements such as fire on a dark background, a Mix Color node with Screen or Add often gives better results than a key. If the matte comes out inverted (for example a white background), invert it with a Color Ramp.

## Tips

- View the Matte output and sample values; tighten Minimum and Maximum until areas that must be 0 or 1 are exact.
- Combine with Dilate/Erode and Blur for edge control (see dilate-erode-matte-cleanup).
- Use a garbage matte (a mask) to exclude areas with similar values.

## Gotchas

- Scene-linear renders can hold values above 1, so set limits in the actual value range, not only 0 to 1.

## Verify

Overlay the keyed element on a contrasting background. Edges should be smooth and the keyed areas fully transparent.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Channel Key Color Space, Key Channel, Limit Method (Max, Single), Limit Channel, Minimum and Maximum semantics, outputs; Luminance Key Minimum and Maximum, uses, the Screen/Add tip and the Color Ramp inversion. Removed High/Low names, the compression-chroma claim and ordering notes not in the manual.
Method: documentation only; no commands were run.
