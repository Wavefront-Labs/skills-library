---
id: creative-arts.animation.blender.camera-background-images
name: camera-background-images
category: creative-arts
field: animation
product: blender
tags: [blender, camera, camera-background-images, camera-background, background-footage, matchmove]
level: practitioner
status: docs-checked
description: "Show reference images or footage behind Blender's camera view: background images for cameras, movie clips, alpha/depth, frame method and image sequence offsets."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# camera-background-images

Goal: match 3D to a plate, storyboard or reference through the camera.

## Setup
Camera Data > **Background Images** (enable checkbox) > Add Image:
- Source **Image** (stills, image sequences, movies) or **Movie Clip** (**Active Clip** uses the scene's active clip; **Render Undistorted** and **Proxy Render Size** use undistorted or proxy versions when they exist).
- **Opacity**, **Depth** (shown behind all objects, or in front of everything), **Color Space** (how the file is interpreted), **View as Render** (apply the scene's colour management to the display).
- **Frame Method**: Stretch, Fit, Crop to match aspect differences.
- **Offset** X/Y (in camera view relative to the camera bounds: 0.1 = 10% of the view width/height), **Rotation**, **Scale**, **Flip** X/Y.

## Visibility
Shown in camera view (Numpad 0). Movie Clips, and images with **View as Render**, are visible behind objects only when film transparency is enabled or the scene world is disabled in the viewport.

## Matchmove check
After a camera solve, the Movie Clip editor Solve tab > Scene Setup panel has **Set as Background** and **Setup Tracking Scene**.

## Rendering the plate
For the final image, bring the footage in through the compositor (Movie Clip/Image node + Alpha Over) with Film > Transparent.

## Gotchas
- Set **Color Space** per background image to match the footage.
- For heavy footage, build proxies in the Movie Clip Editor (Proxy settings), then pick a **Proxy Render Size**; without a built proxy the setting has no effect.

## Verify
Scrub: tracked features stay locked to 3D markers; plate frame numbers match scene frames.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Background Images) and movie_clip/tracking/clip/toolbar/solve (Scene Setup): confirmed source options, Active Clip, Render Undistorted, Proxy Render Size, Color Space, View as Render, Opacity, Depth, Frame Method, Offset units, visibility note, Set as Background and Setup Tracking Scene. Removed unconfirmed image-sequence frame fields, viewport-mode claims and the claim about plate undistortion.
Method: documentation only; no commands were run.
