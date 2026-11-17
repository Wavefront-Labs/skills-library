---
id: creative-arts.film-live-action.premiere-pro.proxy-workflow-and-export-settings
name: proxy-workflow-and-export-settings
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, adobe, film-live-action, proxies, proxy-workflow, ingest, ingest-settings, create-proxies, attach-proxies, toggle-proxies, prores-proxy, media-encoder, adobe-media-encoder, offline-edit, relink, project-manager, sequence-settings, export, export-settings, h264, hevc, prores-422-hq, bitrate, render-and-replace, smart-rendering, deliverables, nle, proxy-presets, proxy-format, attach-proxy, proxy-toggle, full-res-export, proxy-troubleshooting, proxy-mismatch, proxy-aspect, master-export, prores-export, h264-export, web-export, project-manager-use, consolidate-project, scratch-disks, export-quality, bitrate-choice, sequence-from-clip, sequence-settings-match]
level: practitioner
status: draft
description: "Edit heavy camera footage smoothly in Premiere Pro: ingest and attach proxies, toggle them safely, keep project structure and relinking clean, and export masters and web files correctly."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy workflow and export settings in Premiere Pro

**Goal:** cut 4K–8K camera originals (RAW, high-bitrate long-GOP) on an ordinary machine
by editing lightweight proxies, then export from the originals at full quality without
surprises. Menu names refer to recent Premiere Pro versions (2023–2025); Adobe moves
things — confirm in yours.

## 1. Project structure first
- One project folder: `/footage` (camera originals copied from verified offloads, never
  from cards), `/proxies`, `/audio`, `/graphics`, `/exports`, `/project`.
- Keep camera folder structures intact (especially for RAW and some camera formats with
  sidecar files) — import through the Media Browser so clips span correctly.
- Set Scratch Disks (Project Settings) to the project folder, not the system drive.

## 2. Create proxies
**At import:** in the Import/Media Browser ingest settings, enable *Ingest* › *Create
Proxies* and choose a preset. Adobe Media Encoder runs the transcode in the background.
**After import:** select clips › right-click › Proxy › Create Proxies.
- Codec: ProRes Proxy or ProRes 422 LT (Mac/Windows), or a low-res H.264 preset for small
  file size; intra-frame codecs (ProRes, DNxHR LB) scrub more smoothly than H.264.
- Resolution: e.g. 1/4 or 1/2 of source, **same aspect ratio as source** — a mismatched
  aspect ratio is the common reason proxies won't attach.
- Proxies inherit audio channel layout from the preset — check channel count matches the
  originals, or attach will fail/sound wrong.

**Attaching external proxies** (made elsewhere, e.g. by a DIT): right-click › Proxy ›
Attach Proxies, with matching names and durations.

## 3. Edit on proxies
Add the **Toggle Proxies** button to the Program Monitor (button editor "+") and switch
on. Toggle off to check focus, grain or a detail at full quality. Exports use full-res
media by default even if proxies are on (there is an export option to use proxies —
keep it off for finals).

## 4. Sequence settings
Create the sequence from a clip of the main camera (drag to the New Item icon) so frame
size, frame rate and pixel aspect match the originals. Mixed frame rates: decide the
project rate at the start (e.g. 23.976 or 25); conform or interpret footage deliberately.

## 5. Export
File › Export › Media (`Ctrl/Cmd+M`), or queue to Media Encoder for batches.
- **Master:** ProRes 422 HQ (or DNxHR HQX for 10-bit), same frame size/rate as the
  sequence, audio uncompressed PCM 48 kHz. This is the archive and the source for all
  other versions.
- **Web/review:** H.264 or HEVC, VBR 2-pass; typical starting bitrates are something like
  10–20 Mbps for 1080p and 35–50 Mbps for 4K (platforms re-encode anyway — check each
  platform's current spec).
- Check *Match Source* settings actually match; check "Render at Maximum Depth"/"Use
  Maximum Render Quality" when scaling or for 10-bit sources (slower, cleaner).
- Colour: check the sequence/export colour settings (newer versions add colour management
  options); watch the export on the target device, not just in Premiere.

## 6. Handover and archive
File › Project Manager › *Collect Files and Copy to New Location* (optionally trimmed with
handles) to package the project for a colourist or archive; or export XML/AAF/EDL for
Resolve/Pro Tools. Include originals, not proxies, unless the receiver asks.

## Gotchas
- Moving original media after proxies are made → offline clips; relink via right-click ›
  Link Media and point to one file; Premiere finds the rest if the structure is kept.
- Proxies of variable-frame-rate phone footage drift; transcode VFR to constant frame rate first.
- Exporting with "Use Proxies" ticked by accident — soft final file.
- Long-GOP H.264 from cameras edited natively on weak machines: the reason this workflow exists.

## Verify
- [ ] Project folder structure in place; scratch disks set.
- [ ] Proxies created/attached with matching aspect ratio and audio channels.
- [ ] Toggle Proxies tested both ways; originals link correctly.
- [ ] Sequence settings match the main camera.
- [ ] Master and web exports checked full screen on target devices, proxies off.
