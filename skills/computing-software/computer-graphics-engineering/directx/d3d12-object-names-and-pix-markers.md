---
id: computing-software.computer-graphics-engineering.directx.d3d12-object-names-and-pix-markers
name: d3d12-object-names-and-pix-markers
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-debugging, setname, pix-events, winpixeventruntime]
level: practitioner
status: docs-checked
description: "Name every D3D12 object and annotate command lists with PIX events/markers (WinPixEventRuntime) so debug layer, PIX, DRED and crash dumps are readable."
sources: ["https://github.com/microsoft/PixEvents", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12object-setname", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/use-dred"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object names and PIX event markers

## Names
```cpp
texture->SetName(L"GBuffer.Albedo");
cmdQueue->SetName(L"Queue.Direct");
pso->SetName(L"PSO.Opaque.Skinned");
```
Debug names appear in the debug layer's messages (for example the GPU-based validation output prints
`Resource: ... 'Main Color Buffer'`) and in DRED reports (command list and queue debug names, and the names
of existing and recently freed objects matching a faulting address). Name at creation, including heaps, descriptor
heaps, fences and command allocators. Wrap creation helpers so a name is mandatory.

## PIX events (WinPixEventRuntime)
Get the headers and runtime from the `WinPixEventRuntime` NuGet package or build the open-source
`microsoft/PixEvents` repository yourself. `pix3.h` defines `USE_PIX` automatically on x64 and ARM64 when `_DEBUG`,
`DBG`, `PROFILE` or `PROFILE_BUILD` is defined; define `USE_PIX` yourself for other builds that should emit markers.
```cpp
#define USE_PIX
#include <pix3.h>
PIXBeginEvent(cmdList, PIX_COLOR_INDEX(3), L"Shadow cascade %d", i);
// ... draws ...
PIXEndEvent(cmdList);
PIXSetMarker(cmdQueue, PIX_COLOR(255,0,0), L"Present");
{ PIXScopedEvent(cmdList, PIX_COLOR_INDEX(1), "GBuffer"); /* RAII */ }
```
- Events and markers take a context (a command list or queue) plus a colour and a format string. `PIX_COLOR(r,g,b)`
  gives an explicit colour and `PIX_COLOR_INDEX(i)` lets PIX choose one per category index.
- `PIXBeginEvent(color, format, ...)` without a context records a CPU event for timing captures.
- PIX markers are supported on AMD64 and ARM64; elsewhere `USE_PIX` produces a compile warning.

## Markers for crash analysis
With DRED breadcrumb context enabled (`SetBreadcrumbContextEnablement`), PIX marker and event strings appear
in the auto-breadcrumb output (DRED 1.2), so a breadcrumb can say which named region was executing.

## Gotchas
- If `USE_PIX` is not defined, the PIX macros compile to nothing: define it in profile and QA builds.
- Use the scoped macro so every `PIXBeginEvent` has a matching end.

## Verify
- [ ] A PIX GPU capture shows a named pass hierarchy and named resources; debug layer messages print names.

## Checked
Date: 2026-10-26. Documentation: `microsoft/PixEvents` repository (README, `pix3.h`, `PIXEvents.h`, last commit
2026-07-16), Microsoft Learn "Use DRED" and the DirectX-Specs DRED spec, and the GPU-based validation page.
Confirmed: `USE_PIX` auto-definition rules and supported architectures; `PIX_COLOR` and `PIX_COLOR_INDEX`; context
and no-context `PIXBeginEvent`; `PIXScopedEventObject`; names in DRED and GBV output; breadcrumb context. Removed
unconfirmed claims: Nsight and RGD using the same markers, "no runtime formatting with newer runtime",
Vulkan equivalents, and the claim that unbalanced events corrupt the tree.
Method: documentation only; no commands were run.
