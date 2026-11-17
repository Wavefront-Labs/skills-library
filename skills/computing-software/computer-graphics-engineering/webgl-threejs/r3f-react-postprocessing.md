---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-react-postprocessing
name: r3f-react-postprocessing
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, react-postprocessing, effectcomposer, selective-bloom, n8ao]
level: practitioner
status: draft
description: "Add post effects in React Three Fiber with @react-three/postprocessing: EffectComposer setup, bloom with emissive, SMAA/N8AO, selective outlines, custom effects and cost."
sources: ["https://react-postprocessing.docs.pmnd.rs/", "https://github.com/pmndrs/react-postprocessing", "https://github.com/pmndrs/postprocessing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-processing in R3F (@react-three/postprocessing)

## 1. Setup
```jsx
import { EffectComposer, Bloom, N8AO, SMAA, ToneMapping, Vignette } from '@react-three/postprocessing';
<Canvas gl={{ antialias: false }} dpr={[1, 2]}>
  <Scene />
  <EffectComposer multisampling={0} enableNormalPass={false}>
    <N8AO aoRadius={0.5} intensity={2} halfRes />
    <Bloom mipmapBlur luminanceThreshold={1} intensity={0.8} />
    <ToneMapping />
    <SMAA />
    <Vignette eskil={false} offset={0.1} darkness={0.6} />
  </EffectComposer>
</Canvas>
```
Built on pmndrs `postprocessing`: effects are merged into as few fullscreen passes as possible,
much cheaper than stacking three's EffectComposer passes.

## 2. Bloom only what should glow
With `luminanceThreshold={1}`, only colours above 1.0 bloom. Make glowing materials exceed it:
`<meshStandardMaterial emissive="orange" emissiveIntensity={4} toneMapped={false} />`.
No layers/selection juggling needed. `<SelectiveBloom selection={refs}>` exists but costs an extra pass.

## 3. Outlines and selection
```jsx
<Selection>
  <EffectComposer autoClear={false}><Outline blur edgeStrength={3} visibleEdgeColor={0xffffff} /></EffectComposer>
  <Select enabled={hovered}><mesh /></Select>
</Selection>
```

## 4. Custom effect
Extend `Effect` from postprocessing with a GLSL `mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor)`
and wrap with `wrapEffect` or `forwardRef` + `primitive object={effect}`.

## Cost and quality notes
- Set `gl={{ antialias: false }}` and use `multisampling` (MSAA on composer, default 8; lower to 4 or 0 + SMAA on mobile).
- Tone mapping: the composer disables renderer tone mapping; add `<ToneMapping />` (or `mode`) at the end, or colours look flat.
- Every effect samples the full screen; N8AO and DepthOfField are the expensive ones. Gate with a quality setting / `PerformanceMonitor`.

## Gotchas
- Effects order matters (AO before bloom, tone mapping before SMAA/vignette).
- `frameloop="demand"`: composer renders only on invalidate, which is fine; continuous effects (noise, film grain) need "always".

## Verify
- [ ] Only emissive objects bloom; whites in textures do not.
- [ ] GPU time with all effects within budget on target device.
