---
id: computing-software.cloud-infrastructure-engineering.aws.kinesis-video-streams-ingest-and-playback
name: kinesis-video-streams-ingest-and-playback
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, kinesis, kinesis-video-streams, kvs, hls-playback, webrtc, gstreamer-kvssink, video-ingest]
level: practitioner
status: docs-checked
description: "Ingest camera video into Kinesis Video Streams with the producer SDK or GStreamer kvssink, set retention, and play back with HLS or DASH."
sources: ["https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/gs-createstream.html", "https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producer-sdk-cpp-gstreamer.html", "https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/hls-playback.html", "https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/s3-real-time-image-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis Video Streams ingest and playback

**Goal:** stream video from cameras into AWS, keep it for a set time, and play it back live or archived.

## Create a stream
```bash
aws kinesisvideo create-stream --stream-name door-cam-1 --data-retention-in-hours 72 \
  --media-type video/h264
```
Pick retention deliberately (`--data-retention-in-hours`); the Create stream page shows 24 as its example.

## Ingest
The C++ producer SDK builds a GStreamer plugin, `kvssink`, that connects an existing GStreamer pipeline to a stream:
Put `kvssink` as the sink of the pipeline (for example after an RTSP source, depayloader and parser); take the exact
element properties from the kvssink example page linked from the GStreamer page.
- Avoid long-lived access keys on devices; prefer temporary credentials.
- A new fragment starts at each keyframe (a frame carrying the keyframe flag), so keyframe spacing sets fragment length.

## Playback
```bash
EP=$(aws kinesisvideo get-data-endpoint --stream-name door-cam-1 \
     --api-name GET_HLS_STREAMING_SESSION_URL --query DataEndpoint --output text)
aws kinesis-video-archived-media get-hls-streaming-session-url --endpoint-url "$EP" \
  --stream-name door-cam-1 --playback-mode LIVE --expires 3600
```
- HLS live latency is typically 3-5 seconds (1-10 depending on player and network); it cannot be lower than the fragment duration.
- Keep fragment duration at one second or more, or the service may throttle the player.
- For latency under one second the HLS page recommends the GetMedia API instead.
- MPEG-DASH playback is also available; see the HLS page for the related pages.
- Real-time image generation to S3 (for thumbnails and ML) tags fragments through the producer SDK; see that page.
- WebRTC (low-latency two-way sessions) has its own developer guide; it is not covered here.

## Gotchas
- Clock skew on the device breaks timestamps; run NTP.

## Verify
- [ ] Console media viewer shows live video.
- [ ] The HLS URL plays in a browser player.

## Checked
2026-10-28. Confirmed in the Kinesis Video Streams Developer Guide pages in `sources`: `create-stream --data-retention-in-hours`, the `kvssink` GStreamer plugin, HLS latency figures, fragment-duration rules, GetMedia for sub-second latency, keyframe fragmenting; command flags with check_commands.
Removed (not confirmed on the fetched pages): the retention-0 and "up to years" claims, one-stream-per-camera, IoT credentials provider and the PutMedia IAM action, GOP 1-2 s, the data-endpoint rule for all calls, cost formula, CloudWatch metric names, Rekognition, and WebRTC details; credentials in the RTSP URL replaced with a placeholder.
Method: documentation only; no commands were run.
