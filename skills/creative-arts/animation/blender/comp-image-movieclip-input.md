---
id: creative-arts.animation.blender.comp-image-movieclip-input
name: comp-image-movieclip-input
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, image-sequence-input, movie-clip-node, image-input-node, mask-node]
level: practitioner
status: docs-checked
description: "Bring footage and renders into the Blender compositor: Image node (Frames, Start Frame, Offset, Cyclic), multilayer EXR sockets, Movie Clip node outputs and the Mask node."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/input/image.html
  - https://docs.blender.org/manual/en/latest/compositing/types/input/movie_clip.html
  - https://docs.blender.org/manual/en/latest/compositing/types/input/mask.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# comp-image-movieclip-input

Goal: composite previously rendered passes and live-action plates.

## Image node (Add > Input > Image)

- **Image** and **Source** (Single Image, Movie, and so on; options are the Image Editor's image settings).
- **Frames**: how many frames of a movie-type image to play; past this the video pauses unless **Cyclic** is on. The Image Editor sidebar's *Match Movie Length* gives the value to copy.
- **Start Frame**: the scene frame at which the video starts playing.
- **Offset**: how many frames at the start of the video to skip (an offset to an earlier point in time).
- **Cyclic**: start over after the last frame.
- **Auto-Refresh**: updates the video texture in the 3D Viewport when moving through the timeline.
- **Color Space**: the colour space the file was saved in. **Alpha**: how the image uses its alpha channel.
- Outputs: *Image* and *Alpha*. With a multi-layer format such as EXR, each layer is made available as a socket.
- Blender plays video textures at the scene frame rate, not the original frame rate. The manual suggests a driver on Offset when the rates differ.

## Movie Clip node (Add > Input > Movie Clip)

Takes a Movie Clip data-block and links footage camera and tracking values to the outputs. Outputs: *Image*, *Alpha*, and, from the footage camera or tracking, *Offset X*, *Offset Y*, *Scale* and *Angle*. For an image sequence only Image and Alpha have values. Start and end frames are defined in the Movie Clip Editor. The Movie Clip data-block also holds the clip's Start Frame, Frame Offset and Color Space.

It pairs with Movie Distortion, Stabilize 2D and Plane Track Deform nodes (see `creative-arts.animation.blender.object-tracking-stabilization`).

## Mask node (Add > Input > Mask)

Selects a Mask data-block from the Mask editor, with Feather, Size Source and Motion Blur options (see `creative-arts.animation.blender.masking-rotoscoping`).

## Re-comp workflow

Render to multi-layer EXR with the passes you need, then load it with Image nodes and rebuild the comp without re-rendering (practice).

## Gotchas

- Match the scene frame range, the node Start Frame and the first frame number so the comp does not run offset (practice).

## Verify

Scrub the timeline: the frame shown by the Image node follows the scene frame as intended.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: compositing/types/input/image, movie_clip, mask; movie_clip/movie_clips) and the 5.2 source (node_add_menu_compositor.py Input menu). Fixed: the Movie Clip node outputs, the multilayer EXR statement (a socket per layer) and the Offset definition. Removed unconfirmed claims: proxy sharing, 4K playback advice and the Image Editor header frame readout.
Method: documentation only; no commands were run.
