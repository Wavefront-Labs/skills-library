---
id: creative-arts.animation.blender.timeline-playback
name: timeline-playback
category: creative-arts
field: animation
product: blender
tags: [blender, timeline, timeline-playback, sync-mode, audio-scrubbing, play-every-frame, frame-dropping, playback-performance]
level: practitioner
status: docs-checked
description: "Get trustworthy playback in Blender: Sync mode (Play Every Frame, Frame Dropping, Sync to Audio), audio scrubbing, Play In editors, preview range, loop modes and Render Playblast."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/animation_editors.html
  - https://docs.blender.org/manual/en/5.2/editors/timeline.html
  - https://docs.blender.org/manual/en/5.2/editors/3dview/viewport_render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# timeline-playback

Goal: know whether what you see in playback is real timing.

## Playback popover (footer of the Timeline and other animation editors)

- **Sync** (used when playback cannot keep up with the scene frame rate; the actual FPS in the top-left of the 3D Viewport turns red):
  - *Play Every Frame*: plays every frame even if slower than intended.
  - *Frame Dropping*: drops frames if playback is slower than the scene frame rate.
  - *Sync to Audio*: drops frames if playback is too slow to stay synced with the audio.
- **Audio > Scrubbing**: plays bits of the sound while you drag the Playhead. **Audio > Play Audio**: untick to mute all sound.
- **Limit to Frame Range**: the mouse cannot move the Playhead outside the frame range. **Allow Preroll**: lets playback continue before the Start Frame (disabled while Limit to Frame Range is on).
- **Follow Current Frame**: the view pans to catch up when the Playhead goes off screen.
- **Loop**: Infinite, Stop at End Frame, Stop at Start Frame, Restore Frame, Bounce.
- **Play In**: which editors update on every frame; unticked editors update only when playback stops. Starting playback in the Graph Editor, Dope Sheet or NLA Editor plays all editors regardless.
- **Show > Subframes**: display and set fractional current frames.
- **Use Preview Range**: an alternative frame range for repeating a short segment in the 3D Viewport; it does not affect rendering. Set it with P and drag a box, clear it with Alt-P; its bounds are dark orange.

## Transport shortcuts

Spacebar play/pause, Shift-Ctrl-Spacebar play in reverse, Shift-Left / Shift-Right jump to start/end of the frame range (or preview range), Up / Down previous/next keyframe, Ctrl-Left / Ctrl-Right jump by a configurable delta, Left/Right one frame.

## Checking real timing

- The red FPS readout means the machine is not keeping up with the scene frame rate.
- The definitive check is a file: 3D Viewport > View > **Render Playblast** renders the viewport animation (Workbench or EEVEE only, not Cycles), using the current viewport settings plus the output resolution, aspect, path and format; **Render Playblast on Keyframes** renders only frames where selected objects have a key. Disable overlays to hide rigs and empties.
- Solid mode uses Workbench settings and Material Preview uses EEVEE settings for these renders.

## Gotchas

- The Frame Range defaults to 1 to 250; change Start/End in the Timeline header or Output Properties.
- Playback in a workspace with a heavy Graph Editor plays all editors, so use a viewport-only workspace to measure speed.

## Verify

The FPS readout matches the scene rate during playback, or the playblast plays correctly in a media player.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), Animation Editors, Timeline and Viewport Render pages: playback popover options and descriptions, loop modes, Play In rule, preview range keys, transport shortcuts, Render Playblast menu names and engine limits, default frame range. Corrected: the menu item is Render Playblast (not Viewport Render Animation); preview range is cleared with Alt-P (not Ctrl-P). Removed as unconfirmed: lip-sync requirement, Simplify and subdivision tips, frame-rate-base remark, "Sync to Audio with no audio" remark.
Method: documentation only; no commands were run.
