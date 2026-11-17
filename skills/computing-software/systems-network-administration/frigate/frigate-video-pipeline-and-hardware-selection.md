---
id: computing-software.systems-network-administration.frigate.frigate-video-pipeline-and-hardware-selection
name: frigate-video-pipeline-and-hardware-selection
category: computing-software
field: systems-network-administration
product: frigate
tags: [video-pipeline, detect-stream, camera-selection, server-hardware, wifi-cameras, feed-acquisition]
level: intro
status: docs-checked
description: "Understand Frigate's five-stage video pipeline and the camera and server hardware guidance in the official docs."
sources: ["https://docs.frigate.video/frigate/video_pipeline/", "https://docs.frigate.video/frigate/hardware/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Video pipeline and hardware selection

The pipeline has five stages. Feed acquisition connects with FFmpeg (RTSP over TCP, for example) or through go2rtc for other protocols, and a camera can supply main and sub streams. Decoding usually uses the sub stream, optionally downscaled and sampled at a fixed frame rate. Motion detection compares frames to find motion boxes, which merge into motion regions. Object detection runs a model only on those regions; results go through object filters and zones, then tracking. Recording and retention take video segments (all, motion only, or detection clips) while snapshots are stored per tracked object. Birdseye gets decoded frames and motion and object events.

Cameras: H.264 video with AAC audio gives the best compatibility with Frigate and Home Assistant, and multiple substreams help. The author lists Dahua, Hikvision and Amcrest in that order. WiFi cameras are not recommended because their streams are unreliable. For Reolink stay at 5 MP or lower and use the Reolink-specific configuration.

Server: the author's favourite is a Beelink EQ13 (N100 CPU, dual NICs so cameras can sit on an isolated network without internet). The table sizes Intel 1120p-class machines for many busy 1080p cameras and Intel 125H for a significant number. The EQ14 has known compatibility issues. Many mini PCs ship with Windows; install Linux per the getting-started guide.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/frigate/video_pipeline, docs.frigate.video/frigate/hardware (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
