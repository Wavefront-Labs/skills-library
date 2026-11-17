---
id: creative-arts.design-for-form-and-experience.experiential-design.running-media-servers-and-content-playback
name: running-media-servers-and-content-playback
category: creative-arts
field: design-for-form-and-experience
product: experiential-design
tags: [media-server, content-playback, video-playback-servers, hap-codec, resolume, disguise, immersive-installations]
level: advanced
status: draft
description: "Run media servers for installations: choose a server, encode content for smooth playback, set output and resolution, add redundancy, schedule power, and monitor."
sources:
  - "Resolume documentation (resolume.com)"
  - "Vidvox HAP codec (hap.video)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Media servers and content playback

A media server plays video, audio and real-time content to displays and projectors, often controlled by a show system (see `...experiential-design.programming-show-control`).

## Choose
- **Install-grade servers** (for example Disguise, Pixera and Watchout) for multi-output, mapping and redundancy.
- **VJ and creative software** (Resolume, Millumin) for live and smaller installations.
- **Real-time engines** (TouchDesigner, Unreal Engine, Unity) for generative or interactive content.
- **Simple players** for single-screen loops.
Match to outputs, resolution, interactivity, budget, and who will maintain it.

## Content
1. **Know the target:** resolution (including canvas spanning several outputs), frame rate (match projector and content, commonly 30 or 60 fps), colour space.
2. **Choose the codec for smooth playback:** GPU-decoded intermediate codecs such as HAP are common for multi-layer, high-resolution playback at the cost of large files; H.264 and H.265 are smaller but need more decoding resources; ProRes is common for authoring and some servers. Check the server's recommended codec.
3. **Storage:** fast drives (SSD or NVMe), enough bandwidth for the bit rate; keep a clear folder and naming scheme and a content version.
4. **Test full-length playback** on the production machine, watching dropped frames and loop points.

## Reliability
- **Hardware:** industrial or workstation-grade, adequate cooling, UPS, remote access and monitoring.
- **Redundancy:** backup server with automatic fail-over where downtime is costly; spare projector, cables and media copies.
- **Displays:** use EDID emulators or managers to keep display settings stable; lock OS updates and screen savers; scheduled start and stop (wake on LAN, relay power).
- **Remote management** and logs, and a documented restart procedure.

## Verify
- [ ] A 24-hour soak test ran without dropped frames or crashes.
- [ ] A cold start brings the show up automatically.
- [ ] Content and project files are backed up off the machine.
