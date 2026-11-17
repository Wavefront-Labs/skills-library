---
id: computing-software.game-programming.unity.ugui-canvas-scaler-and-layout
name: ugui-canvas-scaler-and-layout
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-ui, ugui, canvas-scaler, rect-transform, anchors, layout-groups, safe-area, render-mode, content-size-fitter, game-programming]
level: practitioner
status: docs-checked
description: "Lay out Unity uGUI that works on every resolution: Canvas render modes, Canvas Scaler settings, RectTransform anchors/pivots, layout groups and safe areas."
sources: ["https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/script-CanvasScaler.html", "https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/UIBasicLayout.html", "https://docs.unity3d.com/ScriptReference/Screen-safeArea.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uGUI Canvas Scaler and layout

**Goal:** one UI layout that looks right on 16:9 monitors, ultrawide, 4:3 tablets and notched phones.

## Canvas render modes
| Mode | Use |
|---|---|
| Screen Space - Overlay | HUD/menus drawn on top of everything; simplest. |
| Screen Space - Camera | UI at a plane in front of a camera; allows post effects/particles in front of UI. |
| World Space | Diegetic UI (health bars over heads, in-world screens, VR). |

## Canvas Scaler
- UI Scale Mode has three options: Constant Pixel Size, **Scale With Screen Size** and Constant Physical Size.
  Scale With Screen Size scales the canvas to fit a Reference Resolution, e.g. 1920x1080.
- Screen Match Mode (when the aspect ratio differs from the reference): **Match Width Or Height** (the Match
  slider scales with the width, the height, or a mix), **Expand** (canvas never smaller than the reference) or
  **Shrink** (canvas never larger than the reference). Choose the Match value that protects the axis your layout
  depends on.
- Reference Pixels Per Unit: a sprite with this Pixels Per Unit setting maps one sprite pixel to one UI unit.

## RectTransform anchors
- Anchors define what the element is attached to; pivots define its own origin.
- Corner HUD elements: anchor to that corner with the Anchor Presets dropdown in the Rect Transform.
- Stretch anchors (Anchor Min 0, Anchor Max 1; anchors are fractions of the parent rectangle) for panels that
  resize with the screen; Left/Right/Top/Bottom then define the padding inside the anchor rectangle.
- Avoid centre-anchored elements far from centre: on ultrawide they float away from edges.

## Layout groups
- Horizontal/Vertical/Grid Layout Group for lists and inventories; Layout Element for
  preferred/min/flexible sizes; Content Size Fitter to grow a container to its content.

## Safe area (notches, rounded corners, TV overscan)
```csharp
[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour
{
    Rect last;
    void Update() { if (Screen.safeArea != last) Apply(); }
    void Apply()
    {
        last = Screen.safeArea;
        var rt = (RectTransform)transform;
        Vector2 min = last.position, max = last.position + last.size;
        min.x /= Screen.width; min.y /= Screen.height; max.x /= Screen.width; max.y /= Screen.height;
        rt.anchorMin = min; rt.anchorMax = max;
    }
}
```
Put interactive and critical HUD under a SafeArea panel; backgrounds stay full-screen. `Screen.safeArea` is in
pixels, relative to the application window, and may equal the full window on some Android versions (see its
Scripting API page).

## Testing
Game view resolution dropdown: add 1920x1080, 2560x1080, 1024x768 and a phone resolution with a notch.

## Checked
2026-11-01. Confirmed against the Unity uGUI 2.0 manual (Canvas Scaler, Basic Layout) and Screen.safeArea
Scripting API: scale modes, match modes, Reference Pixels Per Unit, anchors as fractions, anchor presets,
Left/Right/Top/Bottom padding, safe-area semantics. Removed: Content Size Fitter and layout-group rebuild claims,
Alt+Shift preset shortcut, 100 PPU default, Match 0/0.5/1 mapping, Device Simulator mention.
Method: documentation only; no commands were run.

## Verify
- [ ] Every screen checked at 16:9, 21:9, 4:3 and a notched phone.
- [ ] Nothing interactive outside the safe area.
