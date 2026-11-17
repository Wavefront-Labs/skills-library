---
id: creative-arts.animation.blender.nla-push-down-tweak
name: nla-push-down-tweak
category: creative-arts
field: animation
product: blender
tags: [blender, nla, nla-push-down, push-down, nla-tracks, nla-tweak-mode, tweak-mode, nla-solo, stashed-actions]
level: practitioner
status: docs-checked
description: "Work the Blender NLA track stack: push down actions, add/move/solo/mute tracks, enter tweak mode (Tab, or Shift-Tab to solo) to edit a strip's action, and edit stashed actions."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/nla/tracks.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/editing/strip.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/editing/track.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# nla-push-down-tweak

Goal: sequence and layer clips while still being able to edit any of them.

## Push down

- The topmost track with the orange header (Action Track) holds the object's active action. **Push Down Action** creates a new track below it, moves the action there as a strip and leaves the Action Track empty. It is not available in Tweak Mode. Keying afterwards creates a new active action.
- Add > Action (Shift-A) adds a strip referencing an existing action to the active track.
- Track menu: **Add** (new track below the Action Track), **Add Above Selected**, **Delete**, **Move** (To Top Shift-PageUp, Up PageUp, Down PageDown, To Bottom Shift-PageDown; hover the track region or the shortcuts move strips instead).
- Track headers: **Mute** checkbox, **Lock** padlock, **Solo** star (mutes all other tracks including the Action Track). Strips can be muted individually (Strip > Toggle Muting, H). The "Disable NLA stack" checkbox in the object header mutes all tracks except the Action Track.

## Tweak mode

- **Start Tweaking Strips Actions (Full Stack)** (Strip menu, **Tab**): edit the selected strip's action while all other tracks stay enabled. Tab again (or Stop Tweaking Strips Actions) exits.
- **Start Tweaking Strips Actions (Lower Stack)**: mutes tracks above the current one.
- **Start Editing Stashed Action** (**Shift-Tab**): Tweak Mode plus Solo on the strip's track; works on unmuted actions too. Shift-Tab again to exit.
- The strip's action appears in the Action Track; the **Pin** toggle (Tweak Mode only) shows keys at their original action time instead of their strip-mapped time.
- Note: transitions above a tweaked strip can make key remapping fail; tweak without evaluating the upper stack in that case.

## Stashed actions

A stashed action is an action moved by Stash Action into a muted NLA track. To edit it, use Shift-Tab (or Tab) on its strip; unmute the track to have it contribute again.

## Gotchas

- Forgetting to leave Tweak Mode means new keys go into the strip's action.
- Keys in the active action (Action Track) evaluate on top of the tracks, so leftover keys there can override layers.
- Multiple strips can reference one action; Make Single User (U) or Duplicate (Alt-D, duplicates actions) avoids editing a shared action, while Linked Duplicate (Shift-D) shares it and highlights the other strip in red.

## Verify

Each clip sits on its own track; solo each to confirm; leave no active action unless intended.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), NLA Tracks, Editing Tracks, Editing Strips and Introduction pages: Push Down behaviour, track menu and shortcuts, Solo/Mute/Lock, Full Stack vs Lower Stack, Shift-Tab. Corrected: Tab is Full Stack (the skill said Lower Stack); Add Tracks wording and Add > Action shortcut. Removed as unconfirmed: the green action line colour, "[Action Stash]" label.
Method: documentation only; no commands were run.
