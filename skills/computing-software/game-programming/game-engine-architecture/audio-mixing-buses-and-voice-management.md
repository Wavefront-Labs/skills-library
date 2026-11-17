---
id: computing-software.game-programming.game-engine-architecture.audio-mixing-buses-and-voice-management
name: audio-mixing-buses-and-voice-management
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, audio-mixing, voice-management, sound-concurrency, voice-stealing, ducking, unreal-engine, game-programming]
level: advanced
status: docs-checked
description: "Limit simultaneous sounds with concurrency groups, resolution rules, voice stealing fades and volume-scale ducking, using Unreal's Sound Concurrency as the reference."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audio mixing buses and voice management

**Goal:** important sounds stay audible and the engine never plays more sounds than it can afford.
Unreal's Sound Concurrency Reference Guide states the problem: playing too many sounds at once
causes high resource consumption and poor performance, and Sound Concurrency assets limit how
many play at the same time and what happens when the limit is reached. Rules can apply to
individual sounds, groups of sounds, or all sounds in a project.

## Concurrency group settings (Unreal)
- **Max Count:** maximum concurrently active sounds in the group before the Resolution Rule
  applies. All active components count, not only audibly playing sounds; a Source Bus takes two
  slots (the source and the bus), even when set to Output to Bus Only.
- **Limit to Owner:** apply the rules per actor that plays the sound.
- **Resolution Rule** when Max Count is reached: Prevent New; Stop Oldest; Stop Farthest Then
  Prevent New; Stop Farthest Then Oldest; Stop Lowest Priority (ties stop the oldest); Stop
  Quietest; Stop Lowest Priority Then Prevent New.
- **Retrigger Time:** minimum wait in seconds between playing sounds; sounds rejected by it
  ignore virtualization settings.

## Ducking by volume scale
- Volume Scale is the scaling factor (ducking) applied to older sounds, compounding according to
  the Volume Scale Mode: Default (older sounds scaled more), Distance (distant sounds more), or
  Priority (lower priority sounds more).
- Duck Time and Recover Time (seconds) control the fade down and back; Can Recover lets scaling
  return to default after all sounds in the group stop.
- To avoid thrashing, Volume Scale is applied after Stop Quietest rules are evaluated.

## Voice stealing
Voice Steal Release Time is the fade-out time in seconds when a sound is stopped because another
sound in the group started. Use a short fade so stolen voices do not click (the fade length is a
tuning choice).

## Assigning groups
- A project-wide default is set in Project Settings > Audio (Default Sound Concurrency).
- Per source (MetaSounds, Sound Cues, Sound Waves): Voice Management > Concurrency > Concurrency
  Set. A shared asset shares properties and state between sources.
- A set can hold several assets; the source must satisfy all the rules before it plays. If more
  than one stops active sounds, one sound per group is stopped.
- Override Concurrency sets rules on one sound without creating an asset.

## Design guidance (own advice, not from the page)
- Group sounds by category so a mix can be controlled per category, and give dialogue the highest
  priority so it is never stolen.
- Cap per-frame sound starts so one event (a grenade hitting many objects) does not start dozens
  of sounds.

## Verify
- [ ] In the heaviest combat, dialogue stays audible and is not stolen.
- [ ] The active voice count never exceeds the budget in the audio profiler.
- [ ] Stolen voices fade rather than click.

## Checked
Method: docs-checked 2026-11-09 against Epic's Sound Concurrency Reference Guide (downloaded HTML, read in full). Removed the bus hierarchy, voice counts, dB and LUFS figures, virtual voice, snapshot and HDR claims and the Wwise, FMOD and Unity details: the FMOD page returned a stub and the Unity page was not read.
