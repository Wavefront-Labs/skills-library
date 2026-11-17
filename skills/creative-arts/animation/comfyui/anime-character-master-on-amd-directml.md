---
id: creative-arts.animation.comfyui.anime-character-master-on-amd-directml
name: anime-character-master-on-amd-directml
category: creative-arts
field: animation
product: comfyui
tags: [comfyui, directml, amd, radeon, windows, animagine-xl, sdxl, anime, character-design, master-drawing, sampler, dpmpp-2m, karras, stripe-artifact, torch-directml, api, txt2img, stable-diffusion, consistency]
level: practitioner
status: verified
description: "Run ComfyUI on an AMD GPU under Windows (torch-directml, pinned v0.3.59) and get clean modern-anime character stills from Animagine XL 4.0; the sampler settings that fix the stripe artifact."
sources: [https://github.com/comfyanonymous/ComfyUI, https://huggingface.co/cagliostrolab/animagine-xl-4.0]
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Anime character master stills: ComfyUI on AMD/DirectML

Verified on a Radeon RX 6900 XT, Windows 11, Python 3.10. ~50 s per 832×1216 image.

## Install (the parts that bit)
- Python **3.10** venv. `pip install torch-directml` (gives torch 2.4.1+cpu +
  the DirectML device). Then `torchvision==0.19.1 torchaudio==2.4.1 torchsde` and
  the ComfyUI requirements **minus the torch lines**.
- **Pin ComfyUI to tag `v0.3.59`.** Current `master` imports `comfy_kitchen`, whose
  CUDA backend fails to import on DirectML (`infer_schema ... unsupported type
  list[int]`), and removing the package just moves the error into `attention.py`.
- Start: `python main.py --directml --fp32-vae --listen 127.0.0.1 --port 8188
  --disable-auto-launch`. Check `GET /system_stats` returns JSON.
- Checkpoint: `animagine-xl-4.0.safetensors` (6.9 GB) in `models/checkpoints`.

## The workflow (API JSON, 7 nodes)
CheckpointLoaderSimple → CLIPTextEncode ×2 → EmptyLatentImage (832×1216) →
KSampler → VAEDecode → SaveImage. POST to `/prompt`, poll `/history/<id>`.

## Settings that matter
- **Sampler `dpmpp_2m`, scheduler `karras`, cfg 5, 28 steps.**
  `euler_ancestral` + `normal` on this checkpoint produced a full-frame vertical
  stripe/hatch artifact over the character and background on every seed, regardless
  of `--fp32-vae`. Switching sampler fixed it outright.
- Positive prompt ends with the model's quality tags: `masterpiece, high score,
  great score, absurdres`. For the painted look do NOT add `flat color, cel shading,
  clean lineart` (they pushed it toward a striped "ink wash"). For a true cel master
  (closed outlines, flat fills) use them WITH the style tags in
  `creative-arts.animation.comfyui.dbz-line-and-flat-character-master`.
- Negative: `lowres, bad anatomy, bad hands, text, error, missing fingers, extra
  digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature,
  watermark, blurry, 3d, realistic, photo`.
- For a master to trace: `simple white background, full body, standing straight,
  arms at sides, facing viewer, front view`.

## Memory: stop it spilling into system RAM (measured 26 Oct 2026)

Left on defaults, a ComfyUI process that had run ControlNet-union + IP-Adapter + SDXL drawings held **7.6 GB of
RAM, 10.2 GB of video memory, and 7.2 GB of "shared" GPU memory**, which is the card borrowing system RAM
because the models together exceed the 16 GB card. Windows then had 3.6 GB free and everything else slowed.

| Launch flags | ComfyUI RAM | spill into RAM | free system RAM | speed |
|---|---|---|---|---|
| defaults | 7.6 GB | 7.2 GB | 3.6 GB | 80-110 s per drawing |
| `--highvram --cache-none` | **2.0 GB** | **1.5 GB** | **13.4 GB** | same |

- **Prefer `--cache-lru 2` over `--cache-none` for batches (verified 10 Nov 2026).** `--cache-none` reloads the model
  set through system RAM on every drawing, and two queued jobs with different model sets (ControlNet+IP-Adapter, then
  ControlNet only) spiked RAM and got the jobs killed. With `--cache-lru 2` a 6-drawing batch (ControlNet union +
  IP-Adapter plus, 1344x768) kept free RAM between 2.5 and 6.4 GB on a 32 GB machine and finished in 19 m 43 s with no
  kill; four batches in a row ran clean. Still one job at a time.
- `--highvram` keeps models resident on the GPU instead of shuttling them through system RAM. `--cache-none`
  stops ComfyUI caching node outputs in RAM; models reload from disk only when evicted, and drawing time was
  unchanged.
- **Do not use `--gpu-only`.** On DirectML it returned images that were blank below the head, with the same
  deterministic result every run. The fp16 flags were not the cause; bisecting showed `--gpu-only` was.
- The driver does not give video memory back while the process lives. `POST /free` returns 200 and changes
  nothing. To free the card for Blender or GL work, kill the process (VRAM 14.5 GB to 0.7 GB, free RAM to
  15.7 GB) and start it again for the next drawing batch.
- Measure with the Windows counters `\GPU Process Memory(pid_N_*)\Dedicated Usage` and `\Shared Usage`, per
  process id, plus the process working set. Task Manager's totals hide which process is spilling.
- ComfyUI started from a venv shows two python processes, a launcher and the real interpreter. Measure the
  larger one.

## What this does and does not give you
- It gives a **master**: one still per character with appeal, line and cel shading at
  2020s TV-anime level. Describe hair, eyes, outfit colours exactly.
- It does NOT give consistency: four seeds of the same detailed prompt gave four
  different faces, hairlines and outfits. Pick ONE, trace it, and never regenerate —
  see `creative-arts.animation.vector-graphics.parametric-features-over-traced-master`.

## Verify
Generate 4 seeds. Each must be stripe-free at 100 % zoom. Pick the one whose
silhouette and face you would sign off as the design; it becomes the only source.
