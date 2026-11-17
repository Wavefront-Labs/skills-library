---
id: creative-arts.film-live-action.premiere-pro.remote-editing-with-proxies-and-cloud-media
name: remote-editing-with-proxies-and-cloud-media
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, remote-proxies, cloud-proxies, remote-editing, proxy-workflow, attach-proxies, reconnect-full-resolution, frame-io, camera-to-cloud, lucidlink, cloud-storage, proxy-relink, offline-online]
level: practitioner
status: draft
description: "Edit remotely in Premiere Pro on proxies only: proxy specs that attach cleanly, shipping proxies via cloud storage or Frame.io, and relinking to camera originals for the online."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/ingest-proxy-workflow.html (Adobe - Ingest and proxy workflow)"
  - "https://helpx.adobe.com/premiere-pro/using/proxy-workflows.html (Adobe - Proxy workflow, attach and reconnect)"
  - "https://frame.io/c2c (Frame.io Camera to Cloud)"
  - "https://www.lucidlink.com/ (LucidLink - streamed cloud filesystem for editorial)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote editing with proxies and cloud media

**Goal:** an editor at home cuts a show on small proxy files, and the online relinks
the finished sequence to camera originals with no offline clips and no sync drift.

## 1. Who makes the proxies
- **Facility/DIT makes them, editor never sees originals** (most common). The assistant
  ingests camera originals into a master project, creates proxies, then ships a
  **proxy-attached project + proxy folder** to the editor.
- **Camera to Cloud**: supported cameras/recorders upload proxies to Frame.io during
  the shoot; the editor pulls them into Premiere through the Frame.io panel and the
  originals arrive later by drive.
- **Streamed cloud filesystem** (LucidLink, Suite, similar): proxies sit on a cloud
  volume every editor mounts at the same drive letter/path; only touched blocks download.

## 2. Proxy spec that will attach
Premiere attaches a proxy only if it matches the original's **frame rate, duration and
audio channel count/layout**; resolution and codec may differ.
- Make them with *Project panel > right-click > Proxy > Create Proxies* or an *Ingest
  Settings* preset; the ProRes Proxy and H.264 low-res presets are safe defaults.
- Keep the **same aspect ratio** (1/4 res of UHD = 960x540) so masks, scale and
  stabilisation keyframes translate to full res.
- Keep source **file names** plus the `_Proxy` suffix; never rename originals after.
- Burn in nothing: burn-ins become part of the image if the proxy is ever used as media.
- Multichannel audio: if originals carry 8 tracks, the proxy must too, or attach fails.

## 3. Shipping
- Send the project file and proxy folder, never loose clips; zip the folder or sync it.
- Editor sets *Media Cache* and scratch disks local; relinks proxies once with
  *Link Media* pointing at the proxy root.
- Toggle the **Toggle Proxies** button (add it to the Program monitor button bar) and
  leave it on.

## 4. Returning the cut and onlining
- Editor returns only the `.prproj` (or a Production project) via cloud sync.
- Assistant opens it on the facility machine where originals are online; Premiere
  points master clips at full res (*Proxy > Reconnect Full Resolution Media* if links
  were lost), proxies toggle off, check in the Program monitor.
- If the editor imported new media (music, temp VFX), those files must travel back too.

## Gotchas
- Proxies made in another app (Resolve, DIT software) with different timecode or a
  missing audio channel: attach fails or audio shifts. Spot-check timecode on 5 clips.
- Exporting from the proxy timeline by accident: final files at proxy quality. Toggle
  proxies off before export; Media Encoder uses originals unless "Use Proxies" is ticked.
- Cloud volumes caching on a nearly full system drive: playback stalls.
- Variable-frame-rate phone/screen recordings: transcode to constant rate before proxy.

## Verify
- [ ] Five sample clips attach; timecode and audio channels match originals.
- [ ] Editor's project relinks to proxies in one Link Media pass.
- [ ] Returned project relinks to originals with zero offline media.
- [ ] Export checked with proxies off.
