---
id: computing-software.computer-graphics-engineering.opengl.vulkan-gfxreconstruct-capture-replay
name: vulkan-gfxreconstruct-capture-replay
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-debugging, gfxreconstruct, gfxrecon-replay, api-capture]
level: advanced
status: docs-checked
description: "Capture Vulkan (and D3D12) API streams with GFXReconstruct, trim to frames, replay on other GPUs, convert to JSON and optimise traces for bug reports."
sources: ["https://github.com/LunarG/gfxreconstruct/blob/dev/USAGE_desktop_Vulkan.md", "https://github.com/LunarG/gfxreconstruct/blob/dev/USAGE_android.md", "https://vulkan.lunarg.com/doc/sdk/latest/windows/capture_tools.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GFXReconstruct capture and replay

GFXReconstruct records every Vulkan call (via a layer) into a `.gfxr` file that replays without
the application. Use it for driver bug reports, regression testing on a GPU farm, and capturing
issues that RenderDoc's single-frame model misses (multi-frame, compute-only, headless).

## Capture (desktop)
```sh
# Linux/macOS
VK_INSTANCE_LAYERS=VK_LAYER_LUNARG_gfxreconstruct \
GFXRECON_CAPTURE_FILE=/tmp/app.gfxr \
GFXRECON_CAPTURE_FRAMES=100-110 \          # trimmed capture: only these frames (+ state snapshot)
./app
# or the wrapper script from the SDK:
gfxrecon-capture-vulkan.py -o app.gfxr --capture-frames 100-110 ./app
```
Useful options: `GFXRECON_CAPTURE_TRIGGER=F12` (hotkey start/stop), `GFXRECON_CAPTURE_COMPRESSION_TYPE` (LZ4, ZLIB, ZSTD or NONE; default LZ4),
`GFXRECON_PAGE_GUARD_*` (how mapped memory writes are tracked), `GFXRECON_CAPTURE_FILE_TIMESTAMP=false`.

## Capture (Android)
Install the layer APK/so, then set properties:
```sh
adb shell setprop debug.vulkan.layer.1 VK_LAYER_LUNARG_gfxreconstruct
adb shell setprop debug.gfxrecon.capture_process_name <package name>
adb shell setprop debug.gfxrecon.capture_file /sdcard/Download/app.gfxr
adb shell setprop debug.gfxrecon.capture_frames 200-205
```

## Replay and inspect
```sh
gfxrecon-replay app.gfxr                          # windowed replay
gfxrecon-replay --screenshots 105 --screenshot-dir out app.gfxr
gfxrecon-replay -m rebind --surface-index 0 app.gfxr   # remap memory types for a different GPU
gfxrecon-info app.gfxr                            # summary of the capture file
gfxrecon-convert app.gfxr                         # convert the capture to another format (see its help)
gfxrecon-optimize app.gfxr app_opt.gfxr           # optimize the capture file
```
Cross-vendor replay needs memory-type remapping (`-m remap` or `rebind`) since memory type
indices differ; some extensions captured must exist on the replay GPU.

## Gotchas
- Mapped memory writes are tracked with `GFXRECON_MEMORY_TRACKING_MODE` (page_guard, userfaultfd, assisted or
  unassisted; default page_guard). If replay shows corrupted buffer contents, try
  `GFXRECON_PAGE_GUARD_ALIGN_BUFFER_SIZES=true` or another tracking mode; the GFXReconstruct memory capture
  document explains the trade-offs.
- Traces can be gigabytes; trimmed + compressed captures are the norm.

## Verify
- [ ] Replay on the original machine reproduces the frame (screenshot diff), and on the vendor's machine reproduces the bug.

## Checked

- Date: 2026-11-02.
- Confirmed against: GFXReconstruct USAGE_desktop_Vulkan.md and USAGE_android.md (VK_INSTANCE_LAYERS and layer name, GFXRECON_CAPTURE_FILE / _FRAMES / _TRIGGER, gfxrecon-capture-vulkan.py --capture-frames, compression types and default, GFXRECON_CAPTURE_FILE_TIMESTAMP, memory tracking modes and default, GFXRECON_PAGE_GUARD_ALIGN_BUFFER_SIZES, gfxrecon-replay -m remap and rebind, --screenshots, --screenshot-dir, gfxrecon-info/convert/optimize, Android debug.gfxrecon.capture_file and capture_frames properties).
- Fixed: the Android layer property is debug.vulkan.layer.1, not debug.vulkan.layers.
- Removed: tool output descriptions, assisted/unassisted behaviour detail and the RenderDoc remark (not stated in the fetched pages).

Method: documentation only; no commands were run.
