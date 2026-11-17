---
id: computing-software.game-programming.unity.gizmos-and-handles
name: gizmos-and-handles
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-editor-scripting, ondrawgizmos, unity-handles, scene-view-tools, debug-visualisation, game-programming]
level: intro
status: docs-checked
description: "Visualise gameplay data in the Scene view with OnDrawGizmos/OnDrawGizmosSelected and the Gizmos class, and build custom Scene view controls with Handles in OnSceneGUI."
sources: ["https://docs.unity3d.com/ScriptReference/Gizmos.html", "https://docs.unity3d.com/ScriptReference/Handles.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gizmos and handles

**Goal:** see trigger radii, patrol paths and spawn points in the Scene view, and edit them with handles.

## Gizmos (any MonoBehaviour)
All gizmo drawing must happen in `MonoBehaviour.OnDrawGizmos()` or `MonoBehaviour.OnDrawGizmosSelected()`.
- `OnDrawGizmos` is called when the Scene view or Game view is repainted; everything drawn there is pickable.
- `OnDrawGizmosSelected` is called only if the object the script is attached to is selected.

```csharp
public class GizmosExample : MonoBehaviour
{
    void OnDrawGizmosSelected()
    {
        Gizmos.color = new Color(0.75f, 0.0f, 0.0f, 0.75f);
        // Convert the local coordinate values into world coordinates for the matrix transformation.
        Gizmos.matrix = transform.localToWorldMatrix;
        Gizmos.DrawCube(Vector3.zero, Vector3.one);
    }
}
```
- `Gizmos.color` sets the colour of the gizmos drawn next; `Gizmos.matrix` sets the matrix the Editor uses to draw
  them. Most draw methods accept extra position/rotation parameters, applied on top of the current `Gizmos.matrix`.
- Draw methods listed on the page: `DrawCube`, `DrawWireCube`, `DrawSphere`, `DrawWireSphere`, `DrawLine`,
  `DrawLineList` (pairs of points), `DrawLineStrip`, `DrawRay`, `DrawFrustum`, `DrawIcon`, `DrawMesh`, `DrawWireMesh`,
  `DrawGUITexture`. See also `GizmoUtility` (named on the page; not read).

## Handles (Editor code)
`Handles` (namespace `UnityEditor`) are the 3D controls used to manipulate items in the Scene view. You can define your
own for custom component editors, which suits waypoints, location markers and procedurally generated content. Draw them
from `Editor.OnSceneGUI()`:

```csharp
[CustomEditor(typeof(ExampleScript))]
public class ExampleEditor : Editor
{
    public void OnSceneGUI()
    {
        var t = target as ExampleScript;
        var pos = t.transform.position;
        Handles.color = new Color(1, 0.8f, 0.4f, 1);
        Handles.DrawWireDisc(pos, t.transform.up, 1.0f);
        Handles.Label(pos, t.value.ToString("F1"));
    }
}
```
- `Handles.color` is persistent state affecting handles drawn after it; use `Handles.DrawingScope` to set colour (and/or
  `Handles.matrix`) for a block without leaking it.
- Interactive handles named on the page: `PositionHandle`, `RotationHandle`, `ScaleHandle`, `RadiusHandle`,
  `FreeMoveHandle`, `FreeRotateHandle`, `Slider`, `Slider2D`, `Disc`, `Button`, plus drawing calls such as `DrawWireArc`,
  `DrawAAPolyLine`, `DrawWireDisc`, `DrawDottedLine`.
- For 2D GUI over the Scene view, enclose standard GUI calls in `Handles.BeginGUI` and `Handles.EndGUI` inside
  `OnSceneGUI`; `HandleUtility.GUIPointToWorldRay` and `HandleUtility.WorldToGUIPoint` convert between 2D and 3D.
- Snapping helpers: `Handles.SnapValue`, `SnapToGrid`, `SnapAngleValue`, `SnapScaleValue`.

## Checked
Date: 2026-11-07.
Read in full: Gizmos and Handles script reference pages (6000.6 docs): Remarks, both code samples, and the full
property and method tables.
Removed as unconfirmed: the Game view Gizmos toggle, "editor-only so no `#if`", `[DrawGizmo]`, `DrawWireSphere`-based
alert-radius sample and the PositionHandle/RadiusHandle sample (those signatures are not on the page), `Undo.RecordObject`
and `EditorGUI.BeginChangeCheck` advice, `HandleUtility.GetHandleSize`, the Overlays/`EditorTool` remark and the invented
Verify checklist. Referenced pages `GizmoUtility` and the per-method pages were not opened.
Method: documentation only; no commands were run.
