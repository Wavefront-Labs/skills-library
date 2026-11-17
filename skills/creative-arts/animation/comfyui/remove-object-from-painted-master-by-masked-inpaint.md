---
id: creative-arts.animation.comfyui.remove-object-from-painted-master-by-masked-inpaint
name: remove-object-from-painted-master-by-masked-inpaint
category: creative-arts
field: animation
product: comfyui
tags: [comfyui, inpaint, masked-inpaint, setlatentnoisemask, loadimagemask, paint-out, remove-object, background, painted-background, master-plate, continuity, scenery, pre-fill, feather, composite, animagine-xl, anime, directml, sdxl, retouch]
level: practitioner
status: verified
description: "Paint an object (parked cars) out of a finished painted background master with a flat pre-fill, SDXL masked inpaint on a native-resolution crop and a feathered composite, plus what fails."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remove an object from a painted background master (masked inpaint)

Verified 28 Oct 2026 on a 2016x1152 anime street master (Animagine XL 4.0, ComfyUI on DirectML): four parked cars were
overlapping nose to tail (a continuity note). Two of them came out cleanly, one needed hand work, and the rest is a list of
what does not work, so you can skip it.

## When to use it
A finished master must change (an object contradicts the script, or objects collide) and re-painting the whole master would
break every shot already cut from it. Everything outside the mask stays pixel-identical.

## The method that worked
1. **Pick a native-resolution crop** around the object (about 1216x504 here, sides a multiple of 8, near 1 MP for SDXL). The
   crop gives the model context at the master's own scale; do not downscale the whole master.
2. **Pre-fill the mask with flat colour first.** For each thing that must exist behind the object, write it by hand into the
   pixels: wall = median of a clean lit patch of the same wall (times 0.95 so the model has room to add light); a door or pole
   the object hid = copy the last visible row down (vertical features stay vertical); kerb base = a flat stone grey;
   asphalt = median of the clean rows just below. Never sample the row at the mask top when an object's roof or hood is
   there (the sample was the cars' red/orange and the whole wall came out yellow).
3. **Inpaint the pre-fill at denoise 0.85.** Graph: LoadImage(crop) + LoadImageMask(mask PNG, channel `red`, white = repaint)
   -> VAEEncode -> `SetLatentNoiseMask` -> KSampler (dpmpp_2m, karras, cfg 5.5, 30 steps) -> VAEDecodeTiled -> SaveImage.
   0.55 leaves the flat slab as it is; 1.0 invents new buildings (a yellow shopfront appeared where a plain wall belonged).
   Prompt for what is behind the object ("white plaster building wall with a wooden doorway, grey stone foundation, grey
   concrete sidewalk, asphalt street"), put `no cars` in the prompt and `cars, vehicles, people, yellow, orange` in the
   negative.
4. **Composite back with a feather.** Paste the result over the crop only inside the mask, blurred 12 px (a 24 px feather),
   then paste the crop into a copy of the master. A grown mask (MaxFilter 9) stops edge pixels of the old object leaking in.
5. **Look at 100 %, then in a real shot.** Thumbnails hide seams. Render one wide and one medium shot with the new master.

## What does not work (stop trying)
- **Inpainting the back of a car** that the removed car was hiding: five seeds, three prompts; the model paints a second small
  car, a door, a yellow bonnet. Rebuild a hidden tail by hand: stretch one clean body column leftwards row by row (smooth it
  3 px vertically so it does not streak), feather the join over 14 px, give it a curved rear edge, then draw the tail light,
  bumper and trunk line at 4x and shrink.
- A mask that cuts through a painted feature (a window whose sill was behind the car) leaves a hard horizontal seam at the mask
  top; in a shot it reads as a low wall, which is acceptable. Start the mask at the lowest visible feature, not above it.
- Copying a patch from beside the mask repeats texture visibly if it is more than about 60 px wide; keep copies narrow.
- Asking the model to put in "a hedge" or "a fence" to hide a seam: it ignores the pole and door you pre-filled.

## Script shape (one file, about 60 lines)
`inpaint_bg.py <master> <out> <crop> <rect[;rect]> "<prompt>" [seed] [denoise]`: crop, build the mask from rects, POST the graph
to `127.0.0.1:8188`, poll `/history`, composite, save the full master and the crop. Pre-fills live in a separate small script
per master, so the full chain is reproducible. Stop ComfyUI afterwards (the driver never returns VRAM while it lives).

## Related
- `creative-arts.animation.comfyui.background-master-from-blockout`: how the master was made.
- `creative-arts.animation.pipeline.2d-shot-renderer-from-masters`: point the master table at the new file, keep the old one.
- `computing-software.computer-graphics-engineering.opencv.opencv-inpainting`: for scratches and small objects; it cannot
  invent a doorway.
