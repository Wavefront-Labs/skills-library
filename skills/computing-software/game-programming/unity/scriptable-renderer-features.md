---
id: computing-software.game-programming.unity.scriptable-renderer-features
name: scriptable-renderer-features
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-graphics, urp, scriptable-renderer-feature, scriptable-render-pass, render-graph, custom-post-processing, game-programming]
level: advanced
status: draft
description: "Extend URP with a ScriptableRendererFeature and ScriptableRenderPass using the Render Graph API (Unity 6): injection points, blits, render-layer filters, frame data."
sources: ["https://docs.unity3d.com/6000.0/Documentation/Manual/urp/render-graph.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scriptable renderer features and render graph

**Goal:** add custom passes to URP (outlines, see-through-walls silhouettes, custom post effects)
without forking the pipeline.

## Shape
- `ScriptableRendererFeature`: asset added to the **Universal Renderer Data** (Add Renderer Feature);
  holds settings, creates passes in `Create()`, enqueues them in `AddRenderPasses`.
- `ScriptableRenderPass`: does the work. Unity 6 URP uses **Render Graph**: implement
  `RecordRenderGraph(RenderGraph rg, ContextContainer frameData)`; the old `Execute` path is compatibility mode only.

```csharp
public class TintFeature : ScriptableRendererFeature {
    public Material material;
    TintPass pass;
    public override void Create() => pass = new TintPass { renderPassEvent = RenderPassEvent.BeforeRenderingPostProcessing };
    public override void AddRenderPasses(ScriptableRenderer r, ref RenderingData d) {
        if (material == null || d.cameraData.cameraType == CameraType.Preview) return;
        pass.material = material; r.EnqueuePass(pass);
    }
}

class TintPass : ScriptableRenderPass {
    public Material material;
    public override void RecordRenderGraph(RenderGraph rg, ContextContainer frameData) {
        var res = frameData.Get<UniversalResourceData>();
        if (res.isActiveTargetBackBuffer) return;                  // can't read the back buffer
        TextureHandle src = res.activeColorTexture;
        var desc = rg.GetTextureDesc(src); desc.name = "_TintTemp"; desc.clearBuffer = false;
        TextureHandle dst = rg.CreateTexture(desc);
        rg.AddBlitPass(new RenderGraphUtils.BlitMaterialParameters(src, dst, material, 0), "Tint");
        res.cameraColor = dst;                                     // swap: later passes read our output
    }
}
```
- Render graph culls passes whose outputs aren't used; declare reads/writes correctly
  (`builder.UseTexture`, `builder.SetRenderAttachment`) in custom `AddRasterRenderPass` passes.
- Need depth or normals? Call `ConfigureInput(ScriptableRenderPassInput.Depth | .Normal)` on the pass.

## Drawing filtered objects (outline/silhouette)
In an `AddRasterRenderPass`, build a `RendererListHandle` via `rg.CreateRendererList(new RendererListParams(cullResults, drawSettings, new FilteringSettings(RenderQueueRange.opaque, layerMask)))`
using `RenderingUtils.CreateDrawingSettings(shaderTagIds, renderingData, cameraData, lightData, SortingCriteria.CommonOpaque)` with an override material. URP's built-in **Render Objects**
feature does this without code for simple cases.

## Gotchas
- Features run for every camera, including Scene view and reflection probes; filter by `cameraType`.
- `renderPassEvent` ordering: AfterRenderingOpaques for depth-aware effects, BeforeRenderingPostProcessing
  for effects that should be tonemapped.
- Use **Render Graph Viewer** (Window > Analysis) to see passes, resources and culled passes.
- Mobile: each full-screen blit costs bandwidth; merge effects into one pass where possible.

## Verify
- [ ] Render Graph Viewer shows the pass not culled and reading the expected textures.
- [ ] Effect absent from preview cameras; no errors in Scene view.
