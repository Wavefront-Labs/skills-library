---
id: creative-arts.animation.blender.vse-proxy-setup
name: vse-proxy-setup
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, proxies, vse-proxy-setup, proxy-sizes, proxy-timecode]
level: practitioner
status: docs-checked
description: "Set up VSE proxies for smooth editing: per-strip proxy sizes, storage location, building and rebuilding, timecode indices for long-GOP footage, and preview proxy size."
sources:
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/sidebar/proxy.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/preview/sidebar.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/system.html#video-sequencer
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-proxy-setup

Goal: real-time playback of high-resolution or long footage in the Video Sequence Editor.

## Quickest setup

In the View tab of the Sidebar (Preview or Sequencer & Preview mode) choose a **Proxy Render Size**. This enables that proxy resolution on all strips and starts generating the downscaled files.

## Detailed setup (Sidebar > Proxy tab)

- **Storage**: Per Strip (each strip chooses where to store proxies) or Project (one **Proxy Directory** for the project).
- **Set Selected Strip Proxies**: choose the resolutions to generate and whether to overwrite existing files, then confirm with Set. In Preview mode use View > Proxy > Setup instead.
- **Rebuild Proxy and Timecode Indices**: generates proxies and time indices for the selected strips. In Preview mode use View > Proxy > Rebuild.
- Preferences > System > Video Sequencer > **Proxy Setup**: Automatic builds proxies for added movie and image strips at each preview size, Manual leaves it to you.

## Strip Proxy & Timecode panel

- Header checkbox enables or disables proxy generation for the strip.
- **Custom Proxy**: Directory (default is `<path of original footage>/BL_proxy/<clip name>`) and File (use pre-existing proxies).
- **Resolutions**: one or more proxy sizes. **Overwrite**: replace existing proxy files. **Quality**: 0 percent is maximum compression, 100 percent is none.
- Image sequences can also get proxies through this tab.

## Gotchas

- The Proxy Render Size you view at should be one of the built resolutions.
- Moving the media breaks default proxy locations, so rebuild afterwards or use Project storage.

## Verify

Play a section of high-resolution footage with the proxy size selected: playback holds the scene frame rate.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Proxy Render Size quick setup, Proxy tab options (Storage, Proxy Directory, Set Selected Strip Proxies, Rebuild Proxy and Timecode Indices, Preview-mode View > Proxy menu paths), Strip Proxy & Timecode panel (default BL_proxy path, Resolutions, Overwrite, Quality meaning), Proxy Setup preference. Removed the timecode mode names, the variable-frame-rate advice and the ffmpeg command, which the manual does not cover.
- Method: documentation only; no commands were run.
