---
id: computing-software.game-programming.godot.runtime-loading-images-audio-gltf
name: runtime-loading-images-audio-gltf
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, runtime-loading, image, audio, gltf, mods, game-programming, runtime-file-loading]
level: practitioner
status: docs-checked
description: "Load user files at runtime in Godot 4: Image.load_from_file, AudioStreamOggVorbis, GLTFDocument scenes, fonts, ZIP archives and resource packs."
sources: ["https://docs.godotengine.org/en/stable/tutorials/io/runtime_file_loading_and_saving.html", "https://docs.godotengine.org/en/stable/classes/class_gltfdocument.html", "https://docs.godotengine.org/en/stable/classes/class_image.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Runtime loading of images, audio and glTF

**Goal:** load screenshots, user music, avatars or mod models from disk at runtime, as described in the
"Runtime file loading and saving" page.

## Images
```gdscript
var image := Image.load_from_file(path)       # detects the format from the file extension
$TextureRect.texture = ImageTexture.create_from_image(image)
image.save_png("user://shot.png")             # also save_jpg, save_webp and *_to_buffer variants
```
For bytes in memory use `Image.load_jpg_from_buffer`, `load_webp_from_buffer` and the sibling `load_*_from_buffer` methods.

## Audio
```gdscript
$AudioStreamPlayer.stream = AudioStreamOggVorbis.load_from_file(path)
```
The page shows Ogg Vorbis; check the class reference of any other audio stream class before relying on a load method.

## glTF (and FBX)
`GLTFDocument` and `GLTFState` load and save glTF 2.0 (`.gltf` text, `.glb` binary; binary is faster to write and
smaller, text is easier to debug) in exported projects.
```gdscript
var doc := GLTFDocument.new()
var state := GLTFState.new()
if doc.append_from_file(path, state) == OK:
    add_child(doc.generate_scene(state))
```
Use `append_from_buffer` for bytes; set `GLTFState.base_path` first when external resources must resolve. Save with
`append_from_scene(node, state)` then `write_to_filesystem(state, path)` (`generate_buffer()` saves to memory).
Since Godot 4.3, FBX scenes can be loaded (not saved) at runtime with `FBXDocument` and `FBXState`, same code.

## Other formats
- `FontFile.load_dynamic_font` supports TTF, OTF, WOFF, WOFF2, PFB, PFM; `load_bitmap_font` supports BMFont.
- `ZIPReader` and `ZIPPacker` read and write ZIP archives.
- `ProjectSettings.load_resource_pack` loads PCK or ZIP packs exported by Godot; the page prefers it for DLC because
  it gives a virtual filesystem.

## Safety
Treat any user-supplied file as untrusted: validate sizes and fail gracefully on malformed data. Prefer the
data-only loaders above over loading arbitrary project resources, and load resource packs only from sources you trust.

## Verify
- [ ] Files dropped into the user data folder load in an exported build, not just the editor.
- [ ] Malformed files fail with an error, not a crash.

## Checked
2026-10-28. Confirmed on the runtime loading tutorial (Godot 4.7 docs) and class references: Image.load_from_file,
save_png/jpg/webp, buffer loaders, AudioStreamOggVorbis.load_from_file, GLTFDocument methods, FBX since 4.3, font
formats, ZIPReader, load_resource_pack. Removed (not on the pages): the Image extension list, MP3 and WAV loading
code (including the "4.4+" WAV claim), mipmap generation, the load()/ResourceLoader explanation, and the claim
that PCKs and .tres files execute scripts (kept only as a general caution).
Method: documentation only; no commands were run.
