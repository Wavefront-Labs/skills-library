---
id: computing-software.game-programming.unity.frame-debugger
name: frame-debugger
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-profiler, profiler, frame-debugger, draw-calls, batching, srp-batcher-compatibility, render-passes, renderdoc, game-programming]
level: practitioner
status: docs-checked
description: "Use Unity's Frame Debugger to step through rendering events and read draw-call details: batch cause, shader pass, keywords, textures and constant buffers, plus RenderDoc capture."
sources: ["https://docs.unity3d.com/Manual/FrameDebugger.html", "https://docs.unity3d.com/Manual/frame-debugger-window-event-information.html", "https://docs.unity3d.com/Manual/RenderDocIntegration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Frame Debugger

**Goal:** see how a frame is rendered, event by event, to find unnecessary passes and broken batching.

## What it does
The Frame Debugger pauses the application on a particular frame and lists the rendering events that make up the frame.
You can step through each event and see the graphical state of the scene at that point. It is supported in URP, HDRP,
custom SRPs and the Built-in Render Pipeline (the Built-in pipeline is flagged deprecated in the current docs).
The window updates every frame and cannot be paused; if the number of passes or draw calls changes rapidly, the list can
change too fast to read.

## Event information panel
Top bar: render target selector (pick which target shows in the Game view when rendering to several, for example a
G-buffer), colour channel selector, and Levels (black/white intensity). The centre has an Output tab and a Mesh Preview
tab (preview modes: Shaded, UV Checker, UV Layout, Vertex Color, Normals, Tangents, Blendshapes; plus a wireframe
toggle). Below are the event properties.

Details section includes, among others: RenderTarget, Size, Format, Color/Depth Actions, Blend Color/Alpha, Draw Calls,
Vertices, Indices, Clear Color/Depth/Stencil, **Batch cause**, Meshes, Pass, LightMode, Used Shader, Original Shader,
ZClip, ZTest, ZWrite, Cull, Offset, Stencil fields.
- **Batch cause** displays why the SRP Batcher could not batch the selected event with the previous one; it matters
  only if your application uses the SRP Batcher.
- **Used Shader** can differ from **Original Shader**, for example when the original uses a fallback shader or
  `USEPASS`.

Other sections list the values bound for the event: Keywords (Name, Stage, Scope global/local, Dynamic), Textures,
Ints, Floats, Vectors, Matrices, Buffers and Constant Buffers. A grayed-out section means the shader had no properties of
that type. Stage values: vs (vertex), fs (fragment), gs (geometry), hs (hull), ds (domain). With OpenGL and GLSL shaders
all properties show under the vertex stage.

## RenderDoc for GPU-level capture
The Editor natively launches and captures frames with RenderDoc (version 0.26 or later is required), only on a platform
and graphics API RenderDoc supports.
- If a RenderDoc installation is detected, right-click the Game view or Scene view tab and choose **Load RenderDoc**;
  this reloads the graphics device, so save first. You can also launch the Editor through RenderDoc or pass the
  `-load-renderdoc` command-line option.
- Once loaded, a capture button appears on the right of the Game and Scene view toolbars and captures the next frame of
  that view.
- On DirectX 11, shaders are stripped of debug information by default; add `#pragma enable_debug_symbols` in the
  `HLSLPROGRAM` block to keep it. The page warns it can hurt performance and cause non-deterministic compilation, so
  remove it before a final build.
- For Android, set RenderDoc's Tools > Settings > Android > Android SDK root path to the SDK path Unity uses (Edit >
  Preferences > Android SDK Tools Installed with Unity) so both use the same ADB.
- A standalone D3D11 player can also be captured with the Visual Studio graphics debugger.

## Checked
Date: 2026-11-07.
Read in full: "Introduction to the Frame Debugger", "Frame Debugger Event Information reference" (all tables) and
"RenderDoc integration" (6000.6 docs).
Removed as unconfirmed: the Window > Analysis menu path and Enable button (the intro page gives no menu path), the
URP pass names, remote-device debugging, the invented batch-cause message strings, the "Typical findings" table
(including `CBUFFER_START(UnityPerMaterial)`, MaterialPropertyBlock and Depth/Opaque Texture advice), and the invented
Verify checklist.
Method: documentation only; no commands were run.
