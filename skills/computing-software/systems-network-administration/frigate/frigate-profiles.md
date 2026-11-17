---
id: computing-software.systems-network-administration.frigate.frigate-profiles
name: frigate-profiles
category: computing-software
field: systems-network-administration
product: frigate
tags: [profiles, profile-overrides, home-away-mode, runtime-config, profile-activation]
level: practitioner
status: docs-checked
description: "Define named Frigate profiles that override camera settings at runtime, such as home and away, and activate them from the UI, MQTT or API."
sources: ["https://docs.frigate.video/configuration/profiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frigate profiles

Profiles are named sets of per-camera overrides that you can switch on and off without restarting. There are two levels: definitions at the top level under `profiles` (a machine name plus a `friendly_name`), and overrides under each camera's `cameras.<name>.profiles.<profile>` containing only the fields to change. Every profile named by a camera must be defined at the top level.

On activation Frigate merges the overrides over the camera's base config, applied in memory with no restart; deactivating reverts all cameras. Only one profile can be active at a time, and the active profile survives restarts (stored in `/config/.profiles`).

Overridable sections: `enabled`, `audio`, `birdseye`, `detect`, `face_recognition`, `lpr`, `motion`, `notifications`, `objects`, `record`, `review`, `snapshots` and `zones`. Only explicitly set fields change. Profile zones and masks override the base entries, and each must reference an entry that already exists on the base camera config; profile-only zones or masks are rejected at startup.

Example from the docs: a front door camera where the `away` profile turns on notifications and tracks `person`, `car` and `package` with matching review alert labels, while `home` turns notifications off and tracks only `person`.

Create and manage them in Settings, Global configuration, Profiles (Add Profile, then pick a camera and profile in the section editor). Activate from the main menu Profiles item, over MQTT by publishing a profile name (or `none`) to `frigate/profile/set`, via the HTTP API or through the Home Assistant integration. Switching profiles clears runtime toggle overrides so stale toggles do not undo the profile.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/profiles (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Replaced the unsupported "do not duplicate them casually" advice on masks and zones with the documented rule that profile zones and masks must reference existing base entries.
