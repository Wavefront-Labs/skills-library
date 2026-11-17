---
id: creative-arts.theatre.theatre-sound-design.main-and-backup-playback-redundancy
name: main-and-backup-playback-redundancy
category: creative-arts
field: theatre
product: theatre-sound-design
tags: [theatre, theatre-sound-design, qlab, cue-stack, playback-redundancy, main-backup, backup-machine, redundancy, dante, failover, osc, show-control, mac]
level: practitioner
status: draft
description: "Set up main and backup QLab playback: mirrored machines, synced GO via OSC or MIDI, audio failover switching, workspace sync, and testing a live switch-over."
sources:
  - "https://qlab.app/docs/v5/"
  - "https://www.audinate.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Main and backup playback redundancy

A playback machine failure mid-show is a show stop unless a backup takes over
seamlessly. Standard in professional theatre.

## Architecture
1. **Two identical Macs** (same macOS and QLab versions, same audio interfaces
   or Dante Virtual Soundcard config), each with the full workspace and media.
2. **Synced GO**: the operator's GO on main also fires backup — via a QLab
   Network/MIDI cue in each cue, an external GO button feeding both, or
   "QLab sync" approaches using OSC (`/go` sent to backup). Both machines run
   in lockstep.
3. **Audio failover**: outputs from both go to the console; the console or a
   switcher selects main or backup. With Dante, both machines on the network;
   switching via console input routing or a redundancy switcher.
4. Backup outputs muted at the console until needed.

## Workspace management
- Main is the master copy; **copy workspace and media to backup after every
  session** (Bundle workspace or sync folder with a tool like rsync/Carbon Copy).
- Same cue numbers and IDs; verify by comparing cue lists.
- Version filenames with date.

## Testing
- Daily pre-show: fire a test cue on both, check both meters at the console.
- In tech: simulate a failure (disconnect main) and switch to backup mid-cue;
  confirm continuity.

## During a failure
1. Op switches console input to backup (or failover triggers).
2. If backup is in sync, continue; if not, manually go to the correct cue
   (QLab "load to time" or start the next cue).
3. Report in show report; investigate main.

## Other redundancy
- UPS power for computers and interfaces.
- Spare interface and cables.
- Disable automatic updates, notifications, sleep, Wi-Fi/Bluetooth on show Macs.

## Gotchas
- Backup not updated after a change — fires old cues.
- Backup machine triggered twice (double GO).
- Both machines on one power circuit.

## Verify
- [ ] Workspaces identical (cue count and numbers checked).
- [ ] Failover tested during tech.
- [ ] Pre-show checks include backup meters.
