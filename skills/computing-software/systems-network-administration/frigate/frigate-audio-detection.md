---
id: computing-software.systems-network-administration.frigate.frigate-audio-detection
name: frigate-audio-detection
category: computing-software
field: systems-network-administration
product: frigate
tags: [audio-detection, audio-role, audio-listen-types, audio-labelmap, min-volume, audio-events]
level: practitioner
status: docs-checked
description: "Enable Frigate's CPU audio detector, give a stream the audio role, choose listen labels and group related audio classes."
sources: ["https://docs.frigate.video/configuration/audio_detectors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Audio event detection

Frigate has a built-in audio detector that always runs on the CPU, which suits audio because it is far lighter than image inference. An audio event starts when a configured type of sound is heard and ends once it has not been heard for a configured time; a snapshot is saved at the start.

Enable it globally with `audio.enabled: True` or per camera under `cameras.<name>.audio`. With multiple streams, give the `audio` role to the stream that carries sound (any stream, so long as it includes audio). That adds another connection to the camera, so using the go2rtc restream for it is recommended; the example puts `audio` and `detect` on the sub stream and `record` on the main stream.

Minimum volume: audio detection only runs when volume exceeds the configured minimum, similar to how motion gates object detection. Camera audio levels vary widely, so test with the debug view. Volume also counts as motion for recordings: with `record` retention mode `motion`, any segment where volume exceeds the minimum is kept.

Listen types: the model knows over 500 sound types, many impractical. The defaults are `bark`, `fire_alarm`, `speech` and `yell`; set `audio.listen` to the labels you want (for example `siren`, `glass`, `shatter`, `doorbell`, `knock`, `car_alarm`, `gunshot`, `meow`, `footsteps`). Frequent labels such as `speech` can create many events and snapshots, so start narrow.

Grouping: map several class IDs to one name with `audio.labelmap` (for example `69`, `70`, `75` all to `dogs`), add `dogs` to `listen`, and give it a filter such as `threshold: 0.8`. IDs are zero-based indices into `audio-labelmap.txt`, so each is one less than the line number in the file. Audio label maps are separate from the object detector's `model.labelmap`.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/audio_detectors (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
