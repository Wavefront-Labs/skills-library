---
id: creative-arts.animation.blender.resolution-aspect
name: resolution-aspect
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, resolution-aspect, resolution-percentage, pixel-aspect, frame-rate]
level: practitioner
status: verified
description: "Set Blender output format: resolution and percentage, Swap Dimensions, pixel aspect for non-square delivery, frame rate with Custom FPS/Base, render region and camera Sensor Fit."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/format.html
  - https://docs.blender.org/manual/en/latest/render/cameras.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# resolution-aspect

Goal: frames come out at the right size, shape and speed for the delivery.

## Output Properties > Format

- **Resolution X / Y** and **%** (`resolution_percentage`, labelled % in the panel; 200x100 at 50 rendered 100x50): the percentage scales the render relative to the Resolution values, useful for small test renders with the same proportions. Python: `scene.render.resolution_percentage`.
- Right-click the resolution fields > **Swap Dimensions** switches landscape and portrait.
- **Aspect X / Y**: pixel aspect. It pre-distorts images, which look stretched on a computer screen but display correctly on a device with non-square pixels. Use the correct ratio when rendering to avoid rescaling later. Leave at 1:1 otherwise.
- **Frame Rate**: pick from the menu or **Custom** (FPS and Base, rate = FPS / Base; 23.976 is 24 / 1.001).
- **Render Region** renders part of the frame; **Crop to Render Region** crops the output to that region instead of padding with transparency.
- The presets button in the Format panel header selects common resolution and frame-rate combinations for TVs and screens.

## Camera matching

Camera properties > Camera panel > **Sensor Fit**: Auto builds a square sensor from the larger of the Resolution dimensions; Horizontal sets the sensor Width and derives Height from the output aspect; Vertical does the reverse. When switching between landscape and portrait deliveries, choose Horizontal or Vertical explicitly so the field of view does not jump (practice; measured with a 50 mm lens and 36 mm sensor: Auto gave 39.6 degrees horizontal at 1920x1080 and 1440x1080 but 22.9 degrees at 1080x1920).

## Common deliveries (practice, check the delivery spec)

| Delivery | Resolution | FPS |
|---|---|---|
| HD | 1920x1080 | per spec |
| UHD | 3840x2160 | per spec |
| Vertical social | 1080x1920 | per spec |

## Gotchas

- Changing FPS on an animated scene does not retime keys; use Time Stretching (frame-rate-presets skill) or rescale keyframes.
- Some video codecs need common dimensions; check the codec limits before choosing unusual sizes.

## Verify

Render one frame and check the image size in the Image Editor sidebar (Image tab).

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/output/properties/format.rst (Resolution, Percentage, Swap Dimensions, Aspect, Render Region, Crop to Render Region, Frame Rate FPS/Base, presets) and render/cameras.rst (Sensor Fit modes). Removed: anamorphic 2x example, DCI resolutions, HD/UHD frame rates as fixed values, the viewport-camera-border percentage claim, and H.264 even-dimension rule. Run check, 2026-11-01, Blender 4.5.14 LTS headless: render size at 50 percent; fps 24 with fps_base 1.001 (24000/1001 evaluates to 23.976); changing fps from 24 to 30 left keys at frames 1 and 24; pixel_aspect_x/y, use_border (Render Region) and use_crop_to_border (Crop to Render Region) properties and labels, the Frame Rate preset menu with Custom FPS and Base in the Output panel source; Sensor Fit figures as above. Unrun (documentation only): Swap Dimensions, the format presets button, the delivery table, codec dimension rules, the Image Editor sidebar check.

Method: manual text confirmed from documentation; properties run headless in Blender 4.5.14.
