---
id: computing-software.computer-graphics-engineering.directx.dxgi-present1-dirty-rects-and-scroll
name: dxgi-present1-dirty-rects-and-scroll
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, dirty-rects, present1, power-efficient-presentation]
level: advanced
status: docs-checked
description: "Use IDXGISwapChain1::Present1 dirty rectangles and scroll rects to cut composition and power cost for tools/editor UIs that change small regions."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-1-2-presentation-improvements", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_2/nf-dxgi1_2-idxgiswapchain1-present1", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_2/ns-dxgi1_2-dxgi_present_parameters", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-present"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Present1 dirty rects and scroll

For apps that redraw small regions (editors, terminals, chat, map viewers), telling DWM which
pixels changed lets it compose only those, saving GPU and battery on laptops.

## Usage
```cpp
RECT dirty[2] = { cursorRect, statusBarRect };
DXGI_PRESENT_PARAMETERS pp = {};
pp.DirtyRectsCount = 2; pp.pDirtyRects = dirty;
// optional scroll: content in pScrollRect moved by pScrollOffset
RECT scrollRect = { 0, 40, width, height }; POINT offset = { 0, -20 };
pp.pScrollRect = &scrollRect; pp.pScrollOffset = &offset;
swapChain->Present1(1, 0, &pp);
```

## Correctness contract
In flip model the runtime copies the previous frame's content outside this present's dirty rectangles (and the scroll
rectangle, if any) into the current back buffer. You must handle overlaps between this frame's dirty rectangles and
the dirty rectangles of earlier frames: the intersection must be copied from the previous frame (or re-rendered) into this
frame's dirty rectangle. With more than two back buffers, track the dirty rectangles of all previous frames' buffers.
Scroll works only with flip-model swap chains; dirty rectangles also work with `DXGI_SWAP_EFFECT_SEQUENTIAL` (blt model).

Scroll: the runtime copies the scroll rectangle from the previous frame, translated by the offset, minus the updated dirty
rectangles; you render only the newly exposed strip plus other dirty rects.

## When it's worth it
- Mostly static UIs presenting at low rates on battery-powered devices.
- Not for games or full-screen 3D: everything changes every frame and the bookkeeping is wasted.
- Check with PresentMon which present path you get; the benefit applies to composed windowed presentation.

## Gotchas
- See the `DXGI_PRESENT_PARAMETERS` page for the rules on rectangle coordinates and how dirty and scroll rectangles may overlap.
- `DXGI_PRESENT_TEST` presents nothing and only tests swap-chain status; do not count it in the dirty bookkeeping.
- Wrong bookkeeping shows as stale "ghost" pixels from older frames: debug by colouring dirty rects.

## Verify
- [ ] No ghosting with 2- and 3-buffer chains; GPU usage drops for mostly static content.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: dirty-rectangle and scroll-rectangle behaviour, the multi-frame intersection rule, scroll flip-model-only and dirty-rects blt-or-flip rules, DXGI_PRESENT_TEST semantics, Present1 and DXGI_PRESENT_PARAMETERS exist as described. Corrected: the old text said you must copy the previous frame's dirty regions and described FLIP_DISCARD as making dirty rects mere hints; the documentation says the runtime copies the non-dirty content and only the overlap of dirty rectangles across frames is the app's job, and it does not discuss FLIP_DISCARD for this feature.
Method: documentation only; no commands were run.
