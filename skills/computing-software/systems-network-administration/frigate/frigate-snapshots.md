---
id: computing-software.systems-network-administration.frigate.frigate-snapshots
name: frigate-snapshots
category: computing-software
field: systems-network-administration
product: frigate
tags: [snapshots, clean-snapshot, snapshot-retention, mqtt-snapshots, zone-snapshots]
level: practitioner
status: docs-checked
description: "Enable per-object snapshots in Frigate, know where they are stored and how they differ from recordings and MQTT snapshots."
sources: ["https://docs.frigate.video/configuration/snapshots/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate snapshots

A snapshot is one still image of a tracked object at its best moment. With snapshots on, Frigate writes `<camera>-<id>-clean.webp` to `/media/frigate/clips` for each tracked object; the clean image has no annotations (no timestamp, boxes or cropping). Enable globally with `snapshots: enabled: True` or per camera under `cameras.<name>.snapshots`.

Things to know:
- Snapshots are per tracked object, so a camera without detections saves none even if recording is on.
- Snapshots and recordings are configured and retained independently.
- They appear in the Explore pane, where they can be submitted to Frigate+.
- To save only for objects that enter a given zone, see the zone docs on restricting snapshots.
- Snapshots published over MQTT are configured separately under the camera MQTT settings.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/snapshots (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
