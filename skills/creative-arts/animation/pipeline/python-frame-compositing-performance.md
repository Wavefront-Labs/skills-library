---
id: creative-arts.animation.pipeline.python-frame-compositing-performance
name: python-frame-compositing-performance
category: creative-arts
field: animation
product: pipeline
tags: [performance, profiling, cprofile, pillow, opencv, opencl, umat, gpu, amd, multiprocessing, png, compositing, render-time, numpy]
level: advanced
status: draft
description: "Speed up a Python (PIL/numpy) per-frame compositor: profile first, swap PIL hot spots for OpenCV, work on the subject's box, fast PNG, parallel shots; when GPU offload pays."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Python frame-compositing performance

**Goal:** a 2D animation renderer written with Pillow and numpy that takes about a
second per 1080p frame. A full episode then needs hours, and long background jobs get
killed. Make it several times faster without changing a pixel, and decide on evidence
whether a GPU rewrite is worth it.

## 1. Profile one real shot

```python
render(shot)                                   # warm caches first
cProfile.run("render(shot)", "p.prof")
pstats.Stats("p.prof").sort_stats("tottime").print_stats(14)
```

Sort by `tottime`, not cumulative time. In one 72-frame rigged shot taking 80 s, the
breakdown was:

| Cost | Share | Cause |
|---|---|---|
| per-frame lighting | 49 % | numpy maths on the full 1920×1080 frame, plus `ImageFilter.MinFilter(9)` |
| `Image.rotate` / `Image.transform` | 29 % | full-canvas limb rotations and camera affine |
| PNG encode | 14 % | default zlib level |

## 2. Swap Pillow hot spots for OpenCV (same output)

Measured on a 1920×1080 RGBA frame:

| Operation | Pillow | OpenCV CPU |
|---|---|---|
| rotate about a point, bicubic | 138 ms | 6 ms (`warpAffine`) |
| `MinFilter(9)` on alpha | 866 ms | 1.6 ms (`cv2.erode`, 9×9 ones) |

- Rotation: `cv2.getRotationMatrix2D(center, angle, 1.0)` uses the same
  counter-clockwise-positive convention as `Image.rotate`. Pass
  `borderValue=(0, 0, 0, 0)` so transparent stays transparent.
- Camera zoom and pan: the output maps from input by scale `W/cw` about the crop
  origin. Use the matrix `[[W/cw, 0, -x0·W/cw], [0, H/ch, -y0·H/ch]]` with
  `BORDER_REPLICATE`.
- The frames matched the Pillow output, with a mean difference under 3 of 765.

## 3. Don't process empty pixels

Run per-character effects (lighting, rim, edge erosion) on `layer.getbbox()` padded
by about 12 px, then paste the result back. A character covers about a fifth of a
wide frame, so this alone removes most of the lighting cost.

## 4. Write frames cheaply

`img.save(path, compress_level=1)`: intermediate PNGs that ffmpeg reads once don't
need maximum compression.

## 5. Render shots in parallel

Shots are independent. Use a `multiprocessing.Pool(n).imap_unordered` over
(shot, location) pairs, with a top-level worker function because Windows uses spawn.
Size `n` by free RAM, at roughly 1 to 1.5 GB per worker, not by core count. On a
12-thread machine with about 3 GB free, 4 workers gave about 2.5× throughput. Too
many workers trigger low-memory kills of long jobs.

Together, steps 2 to 4 took one rigged shot from about 99 s to 38 s including
start-up, before parallelism.

## 6. When a GPU pays (and when it doesn't)

OpenCV's OpenCL path (`cv2.UMat`) runs on AMD cards on Windows:
`cv2.ocl.Device.getDefault().name()` reported gfx1030 on an RX 6900 XT. But one
`warpAffine` per frame with upload and download took 18 ms against 6 ms on the CPU.
Per-operation offload loses to transfer cost. A GPU wins only when the whole frame
stays on the card: parts uploaded once per shot, compositing, lighting and camera
done as shaders (moderngl or wgpu), and one download per frame. Prototype that on one
shot and adopt it only if it beats the parallel CPU path.

## 7. A per-pixel effect as a GPU shader (moderngl), and what the GPU was really for

`moderngl.create_standalone_context()` gives an OpenGL context on the AMD card under Windows, with no window.
A character lighting pass (key tint, ink kept, 9×9 alpha-erosion rim) as a fragment shader matched the CPU
version to within 1 level of 255 and took 8 ms against 147 ms on a 900×980 crop. A 16-shot batch went from
2 min 40 s to 2 min 7 s.

- Upload the crop as a texture with `GL_NEAREST`, draw a full-screen strip into a same-size framebuffer, read it
  back. No flip is needed if rows are treated the same way in and out.
- cv2.erode treats pixels outside the image as opaque. Reproduce that in a shader's min-filter loop.
- Compute bounds like the first and last column of alpha on the CPU and pass them as uniforms.
- Keep a CPU fallback, switched off by an environment variable, so a missing GL driver doesn't stop a render.

**Remember what the goal is.** If it is to offload system RAM and CPU, speed is the wrong measure. In practice
the largest memory win was not in the compositor at all: it was ComfyUI spilling 7 GB of GPU data into system
RAM (see `comfyui.anime-character-master-on-amd-directml`). Measure per-process RAM and GPU memory first.

**Dead end, recorded so it isn't retried blindly:** running a Llama-based TTS (Chatterbox) on the GPU through
torch-directml. DirectML aborts on complex tensors (`ComplexFloat`) in the vocoder; on the token generator it
rejected inference-mode tensors ("Cannot set version_counter"), zero-size `torch.cat` pieces, and rotary
buffers, one after another. Unwrap `@torch.inference_mode` decorators, clone buffers, and filter empty cats to
get further, but each fix revealed another unsupported op. A single-token decode loop is also dispatch-bound.
Keep TTS on the CPU; it uses about 4 GB for a short time.

## Verify

Re-profile the same shot, and diff a start, middle and end frame against the old
renderer: report the mean absolute difference and the share of pixels differing by
more than 30.

See `computing-software.computer-graphics-engineering.opencv.opencv-cuda-gpumat` for
the NVIDIA-only CUDA route.
