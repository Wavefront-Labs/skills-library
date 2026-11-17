---
id: creative-arts.animation.editing.proxy-offline-workflow
name: proxy-offline-workflow
category: creative-arts
field: animation
product: editing
tags: [proxy-workflow, nle-project-setup, nle, offline-online, proxies, prores-proxy, dnxhr-lb, relink, premiere-proxies, resolve-proxies]
level: practitioner
status: draft
description: "Edit animation smoothly with proxies: generating ProRes Proxy/DNxHR LB versions of heavy renders, attaching them in Premiere/Resolve/Avid, and relinking to full-res for finishing."
sources:
  - https://helpx.adobe.com/premiere-pro/using/ingest-proxy-workflow.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://ffmpeg.org/ffmpeg-codecs.html#ProRes
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proxy and offline workflow

**Goal:** real-time playback of EXR sequences, 4K ProRes 4444 renders or long-GOP files in the edit, with
a guaranteed relink to full quality for the online/conform.

## Proxy formats

| Format | Use |
|---|---|
| ProRes Proxy / LT (1080p or half-res) | Mac/Premiere/Resolve shops |
| DNxHR LB / DNxHD 36 | Avid offline |
| H.264 all-intra | lightweight laptop editing |
Proxies must match the source's frame count, frame rate and start timecode; resolution may differ (same aspect).

## Making proxies

```bash
# render frames to a ProRes Proxy with matching TC and reel name
ffmpeg -framerate 24 -start_number 1001 -i sh010_v012.%04d.png -vf scale=1280:-2 \
  -c:v prores_ks -profile:v 0 -timecode 00:00:41:17 -metadata:s:v reel_name=sh010_v012 \
  proxies/sh010_v012_proxy.mov
```
Or let the NLE do it:
- **Premiere**: Ingest settings - Create Proxies (Media Encoder), or right-click clips - Proxy - Create
  Proxies; toggle with the Toggle Proxies button.
- **Resolve**: right-click - Generate Proxy Media; Playback - Proxy Handling - Prefer Proxies. Resolve also
  has Optimized Media.
- **Avid**: Consolidate/Transcode to DNxHD/DNxHR LB; relink back to AMA/full-res for finishing.

## Names and metadata

Keep the same base filename (plus `_proxy`) and the same timecode and reel/tape name; relinking matches on these.
Folder structure mirroring the full-res tree makes relinking a path swap.

## Gotchas

- Proxies with a different frame count (e.g. dropped frames from a broken encode) relink "successfully" but
  slip sync; check counts.
- Colour: proxies made with a display transform look right in the edit but the full-res EXR needs the same
  transform in the online; document it.
- Effects keyed to proxy resolution (crops, position in pixels) can shift when relinked if the NLE doesn't scale
  them; use percentage-based settings.

## Verify

Toggle proxies off on a cut with transforms: frames, positions and sync identical to proxy playback; the conform
reports zero offline clips.
