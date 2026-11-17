---
id: creative-arts.animation.blender.bpy-images-api
name: bpy-images-api
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-images-api, image-pixels, image-api, foreach-get, numpy, image-save]
level: practitioner
status: verified
description: "Create, load, read and write images from Python: images.new, pixels with foreach_get and NumPy, colour space, and saving and packing."
sources:
  - https://docs.blender.org/api/current/bpy.types.Image.html
  - https://docs.blender.org/api/current/bpy.types.BlendDataImages.html
  - https://docs.blender.org/api/current/info_best_practice.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-images-api

Goal: generate or process image data inside Blender fast enough for 4K textures.

## Create and load

```python
import bpy
img = bpy.data.images.new("mask", width=2048, height=2048, alpha=True, float_buffer=False)
tex = bpy.data.images.load("//textures/albedo.png", check_existing=True)
tex.colorspace_settings.name = "Non-Color"     # for data maps (normal, roughness, masks)
```
`float_buffer=True` creates a floating-point buffer (for HDR or displacement data; its colour space was Linear Rec.709 in 4.5.14); `is_data=True` creates the image with a non-color data colour space (reported as Non-Color).

## Pixels, the fast way

`img.pixels` holds the image buffer as floating-point values (a flat RGBA array, `w*h*4` long). Indexing it element by element in Python is slow. Use `foreach_get/foreach_set` with NumPy:

```python
import numpy as np
w, h = img.size
buf = np.empty(w * h * 4, dtype=np.float32)
tex.pixels.foreach_get(buf)                 # read
px = buf.reshape(h, w, 4)                   # rows x columns x RGBA
px[..., 0] = 1.0 - px[..., 0]               # invert red
img.pixels.foreach_set(px.ravel())          # write (flat, exactly w*h*4 floats)
img.update()                                # refresh viewport/GPU texture
```

## Save, pack, reload

```python
img.filepath_raw = "//textures/mask.png"
img.file_format = 'PNG'
img.save()                                  # writes to filepath_raw
img.pack()                                  # or embed in the .blend
tex.reload()                                # re-read from disk
img.scale(1024, 1024)                       # resample in place
```
`img.save_render(path, scene=None)` instead saves using a scene's render settings (including its colour management): use it for display images, not data maps.

## Gotchas

- A generated image that is never saved or packed is lost on reload.
- `pixels` is always a float array, even for 8-bit images (an 8-bit image given 0.5 reads back 0.502). The values are not colour-managed for you: write values in the image's own colour space.
- `bpy.data.images.load` of a file that cannot be read raises RuntimeError ("Cannot read '//nope.png'"); a readable file reports its real `size` straight away. A 2-D array passed to `foreach_set`, or one of the wrong length, raises TypeError ("expected sequence size 128").
- `bpy.data.images.remove(img)` removes the image; `img.buffers_free()` frees the image buffers from memory. Both help in big batch jobs.

## Verify

Write a gradient into a new image, save it, open it in an external viewer: orientation and values match what you wrote.

## Checked

2026-10-27 against the Blender 5.2 Python API (BlendDataImages.new/load/remove signatures, Image.pixels, filepath_raw, save, save_render, scale, reload, pack, update, buffers_free). Removed unconfirmed claims (pixel origin and row order, size-zero behaviour, 8-bit conversion detail). Run check, 2026-11-01, Blender 4.5.14 LTS headless: `images.new` parameters (name, width, height, alpha, float_buffer, stereo3d, is_data, tiled) and `load(filepath, check_existing, image)`; a new 8x4 image had 128 pixel floats, `channels` 4 and started opaque black; the NumPy `foreach_get`, edit, `foreach_set` and `update()` code ran; a PNG written with `filepath_raw`, `file_format` and `save()` loaded back with the same size and first pixels, `check_existing=True` returned the same datablock and `False` made a second one; the colour-space list contains Non-Color and sRGB; `scale(4, 2)`, `pack()`, `reload()`, `buffers_free()`, `save_render(filepath, scene=None)` and `images.remove` ran; `img.packed_file` was set after `pack()`. Unrun: pixel row order against an external viewer, viewport refresh from `update()`, behaviour of an unsaved generated image after a file reload.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
