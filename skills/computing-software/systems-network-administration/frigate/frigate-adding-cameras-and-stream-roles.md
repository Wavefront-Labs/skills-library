---
id: computing-software.systems-network-administration.frigate.frigate-adding-cameras-and-stream-roles
name: frigate-adding-cameras-and-stream-roles
category: computing-software
field: systems-network-administration
product: frigate
tags: [add-camera-wizard, camera-inputs, stream-roles, detect-role, onvif-probe, rtsp-url, camera-validation]
level: practitioner
status: docs-checked
description: "Add a camera with Frigate's wizard or YAML, assign detect and record roles to streams and read the wizard's validation checks."
sources: ["https://docs.frigate.video/configuration/cameras/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding cameras and assigning stream roles

Use Settings, Global configuration, Camera management, Add Camera. Step 1: enter a name, host and credentials and choose Probe camera (ONVIF, port usually 80 or 8080; some cameras need a separate ONVIF account or digest auth) or Manual selection (URL templates for Dahua/Amcrest, Hikvision/Uniview/Annke, Ubiquiti, Reolink, Axis, TP-Link, Foscam, or Other for a custom RTSP URL). Names are lowercased with underscores, and a `friendly_name` is stored if needed. Step 3 assigns roles; step 4 validates and previews each stream. Save New Camera starts it immediately with no restart.

YAML equivalent: under `cameras.<name>.ffmpeg.inputs` list each `path` with `roles`. A typical pairing is a low-resolution sub stream with `detect` and the main stream with `record`, plus optional `detect: width/height`. If you define a single input without `detect`, Frigate assigns it. Even for recording-only use, a low-resolution `detect` stream reduces decoding load.

The wizard warns about: detect resolution too high or too low, a `record` stream without AAC audio, an `audio` stream with no audio, a restreamed input used for `record`, a Reolink RTSP stream that should use http-flv, and Dahua or Hikvision substreams chosen for detect. "Reduce connections to camera" routes the input through the go2rtc restream; "stream compatibility mode" sends it through go2rtc's ffmpeg module but prevents two-way talk detection.

Deleting a camera requires the admin role and permanently removes its recordings, tracked objects and configuration; set the camera Off or Disabled to just stop processing.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/cameras (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
