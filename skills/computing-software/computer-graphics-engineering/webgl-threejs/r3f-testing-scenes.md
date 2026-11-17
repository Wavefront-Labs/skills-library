---
id: computing-software.computer-graphics-engineering.webgl-threejs.r3f-testing-scenes
name: r3f-testing-scenes
category: computing-software
field: computer-graphics-engineering
product: webgl-threejs
tags: [computer-graphics-engineering, r3f, react-three-fiber, react-three-test-renderer, visual-regression, playwright, vitest]
level: practitioner
status: draft
description: "Test React Three Fiber scenes: unit tests with @react-three/test-renderer (graph, events, frames), logic split from rendering, and Playwright screenshot regression with WebGL."
sources: ["https://r3f.docs.pmnd.rs/api/testing", "https://github.com/pmndrs/react-three-fiber/tree/master/packages/test-renderer", "https://playwright.dev/docs/test-snapshots"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing R3F scenes

## 1. Scene graph tests (no GPU)
```jsx
import ReactThreeTestRenderer from '@react-three/test-renderer';
test('box rotates and responds to clicks', async () => {
  const onClick = vi.fn();
  const r = await ReactThreeTestRenderer.create(<Box onClick={onClick} />);
  const mesh = r.scene.children[0];
  expect(mesh.instance.rotation.x).toBe(0);
  await ReactThreeTestRenderer.act(async () => { await r.advanceFrames(2, 1 / 60); }); // run useFrame
  expect(mesh.instance.rotation.x).toBeGreaterThan(0);
  await r.fireEvent(mesh, 'click');
  expect(onClick).toHaveBeenCalled();
  expect(r.scene.findAll(n => n.type === 'Mesh')).toHaveLength(1);
});
```
Runs in Node/jsdom with a mocked WebGL context: tests structure, props, useFrame logic and
events. It does not render pixels or compile shaders.

## 2. Keep logic testable
Move game/configurator logic (state machines, zustand stores, math) out of components and test it
plainly. Components then become thin bindings worth only a smoke test.

## 3. Visual regression (real GPU)
```ts
test('product viewer renders', async ({ page }) => {
  await page.goto('/viewer?seed=1&animate=0');       // deterministic: fixed camera, no time-based motion
  await page.waitForFunction(() => window.__sceneReady === true);
  await expect(page.locator('canvas')).toHaveScreenshot({ maxDiffPixelRatio: 0.01 });
});
```
- Expose a ready flag after assets load and a frame renders (`useEffect` + `invalidate`).
- CI headless Chromium uses SwiftShader (software GL): slow but deterministic; pin browser
  version and generate baselines on CI, not dev machines (GPU differences).
- `gl={{ preserveDrawingBuffer: true }}` in test builds if you capture via `toDataURL`.

## Gotchas
- drei components that load assets (useGLTF) need Suspense and network mocks or local fixtures in unit tests.
- Snapshot tests of the whole three graph are brittle; assert specific properties.
- Antialiasing and floating-point differences need a small diff tolerance.

## Verify
- [ ] Unit tests run in under a few seconds without a browser.
- [ ] Screenshot test fails when a material colour changes, passes on rerun otherwise.
