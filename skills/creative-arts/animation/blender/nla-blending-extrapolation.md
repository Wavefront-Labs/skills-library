---
id: creative-arts.animation.blender.nla-blending-extrapolation
name: nla-blending-extrapolation
category: creative-arts
field: animation
product: blender
tags: [blender, nla, nla-blending-modes, nla-combine, nla-replace, nla-extrapolation, hold-forward, nla-hold, animation-layers]
level: practitioner
status: verified
description: "Layer actions in Blender's NLA: strip blend types (Replace, Combine, Add, Subtract, Multiply) and extrapolation (Hold, Hold Forward, Nothing) so layers mix without popping."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/nla/sidebar.html
  - https://docs.blender.org/manual/en/5.2/editors/nla/strips.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# nla-blending-extrapolation

Goal: additive layers (breathing on top of a walk, a head-turn override) that combine predictably.

## Blending (Sidebar > Strip > Active Strip, or Edited Action for the active action)

- API: `NlaStrip.blend_type` is `REPLACE`, `COMBINE`, `ADD`, `SUBTRACT` or `MULTIPLY`; `extrapolation` is `NOTHING`, `HOLD` or `HOLD_FORWARD` (strips made with `track.strips.new()` start as Replace and Hold). `influence` has an effect only while `use_animated_influence` is on.
- **Replace**: overwrites the values from the lower tracks; with Influence below 1 it linearly interpolates between previous and new values.
- **Add / Subtract / Multiply**: result = mix(previous, previous (+, -, x) value, influence). Add on a scale of 1 with a value of 1 gives 2, so avoid it for scale.
- **Combine**: the method depends on the property type. Axis/angle rotation: previous + value x influence. Quaternion rotation: previous x value^influence (quaternion maths on all four channels). Proportional (scale): previous x (value / default)^influence. Others: previous + (value - default) x influence. Use it for animation layers, and key layers relative to the default/rest values.
- Combine always drives all four quaternion channels, and Insert Single Keyframe is forced to insert all four keys.

## Extrapolation

- **Hold**: the first keyframe's values also apply to earlier frames (only if the strip is the first in its track) and the last keyframe's values apply to later frames, up to the next strip.
- **Hold Forward**: the last keyframe's values apply to later frames (up to the next strip); earlier frames are unaffected.
- **Nothing**: animated properties return to their default values outside the strip boundaries.
- While an action is still the active action, Hold is used regardless of the setting.

## Recipe: additive breathing

1. Base walk in track 1 (Replace, Hold).
2. Breathing action keyed as offsets from rest, pushed down to track 2 with Blending **Combine**, Extrapolation **Nothing** or **Hold Forward**, and Repeat to cover the shot.
3. Adjust Influence for intensity.

## Gotchas

- A Hold strip that is not first in its track will not extend backwards; popping at the start of a layer is usually its extrapolation or blend setting.
- Nothing resets the layer's properties to their defaults outside the strip, so lower tracks must supply the values there.
- Strips and tracks can be muted; Solo (star) mutes all other tracks including the Action Track.

## Verify

Solo each track to see its contribution; scrub across strip boundaries and look for pops.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), NLA Sidebar and Tracks pages: all five blending modes and the Combine formulas, the three extrapolation modes, Hold limitation, Solo behaviour. Removed as unconfirmed: "Hold Forward is the default for most strips", fall-through behaviour of unkeyed channels. Corrected: Hold extends backwards only when the strip is first in its track (not "lowest track"); Nothing returns values to defaults.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): two tracks, base strip loc x 4 scale x 2, upper strip loc x 10 scale x 3, read at frame 10 with influence 1 then 0.5: Replace 10 and 3 then 7 and 2.5; Add 14 and 5 then 9 and 3.5; Subtract -6 then -1; Multiply 40 then 22 and scale 6 then 4; Combine 14 and 6 then 9 and 3.4641 (= 2 x 3^0.5, matching previous x (value / default)^influence). Extrapolation: a first-in-track strip with Hold held its first key before it and its last after it; Hold Forward changed nothing before it; Nothing returned location 0 and scale 1 outside (4.5.14 default values) and a strip in a second track with Hold also held backwards to frame 5. Not run (confirmed from the manual only): the quaternion Combine maths, Insert Single Keyframe on Combine, the active-action Hold rule and Solo behaviour.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
