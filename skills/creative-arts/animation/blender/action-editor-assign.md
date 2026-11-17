---
id: creative-arts.animation.blender.action-editor-assign
name: action-editor-assign
category: creative-arts
field: animation
product: blender
tags: [blender, action-editor, action-editor-assign, fake-user-actions, action-management, stash-action, unlink-action, actions, game-animation]
level: practitioner
status: docs-checked
description: "Manage actions in Blender's Action Editor: assign, stash vs push down, replace an action on all users, frame range and cyclic flags, and keep a game rig's action list clean."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/dope_sheet/modes/action.html
  - https://docs.blender.org/manual/en/5.2/animation/actions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# action-editor-assign

Goal: several clips (idle, walk, run) on one rig without losing any.

## Basics (Dope Sheet > Action Editor mode, object/armature selected)

- **Action** data-block menu in the header: assign an existing action, or clear the object's active action. Name new actions immediately (`Hero_Walk`).
- Clicking **New Action** on an object that already has an active action stashes the previous action automatically.
- **Fake user** (shield icon on the data-block): keeps an action saved even with zero users (standard data-block behaviour). Turn on for every clip.
- **Stash Action** (Action menu): creates a new muted NLA track at the bottom of the NLA tracks and moves the active action into it, so it no longer affects the animation.
- **Push Down Action** (Action menu): creates a new NLA track below the Action Track and moves the action there (same as Push Down in the NLA editor; see `nla-push-down-tweak`).
- Both leave the object with no active action; select the strip in the NLA editor and press Tab for Tweak Mode to edit it again.
- **Replace Action**: pops up a chooser and swaps the action on every data-block that uses the active object's action. It ignores NLA strips and action constraints; use Outliner **Remap Users** to also change those.
- **Replace with New Action**: creates a duplicate of the current action and replaces all its users with it (also ignores NLA strips and action constraints).

## Switching clips

Assign a different action from the Action menu. Channels that the new action does not animate keep the value they last had, so key a rest/neutral pose on every control in every clip.

## Game-character hygiene

- Naming: `<Rig>_<Clip>` keeps exported take or clip names readable.
- Action properties (Dope Sheet or NLA sidebar when a channel or NLA track is selected): **Manual Frame Range** (toggled by its checkbox) sets the intended playback range. It is used instead of the key range when an NLA track is added from the action, and exporters can use it; it does not change evaluation.
- **Cyclic Animation** only records intent: the first and last frame of the range should be the same pose one loop apart. It does not make the action loop by itself.
- Before exporting several actions, delete test actions or clear their fake users so only real clips remain.

## Gotchas

- Actions are shared data-blocks: two objects using the same action move together.
- Actions contain slots (one per animated data-block); the Action Editor header has a slot selector next to the action. See `action-slots`.
- Merge Animation and Separate Slots (Action menu) work only on directly assigned actions, not those referenced by NLA strips.

## Verify

Outliner > Blender File > Actions lists every clip; switching actions on the rig shows each clip correctly from its first frame.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Action Editor header and Action menu (Stash, Push Down, Replace, Replace with New Action, Merge Animation, Separate Slots), automatic stash on New Action, Manual Frame Range and Cyclic Animation behaviour. Removed as unconfirmed: warning on unlink, Shift-click unlink, the stash track's label, and exporter mode names.
Method: documentation only; no commands were run.
