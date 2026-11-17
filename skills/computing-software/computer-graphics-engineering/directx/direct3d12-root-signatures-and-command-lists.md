---
id: computing-software.computer-graphics-engineering.directx.direct3d12-root-signatures-and-command-lists
name: direct3d12-root-signatures-and-command-lists
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [directx, direct3d, d3d12, directx-12, dx12, hlsl, dxc, shader-model-6, root-signature, descriptor-heap, descriptor-table, root-constants, bindless, resource-barriers, enhanced-barriers, command-list, command-allocator, command-queue, fence, pso, pipeline-state-object, dxgi, swap-chain, pix, debug-layer, gpu-based-validation]
level: advanced
status: docs-checked
description: "Direct3D 12 essentials: command allocators/lists/queues and fences per frame, root signatures and descriptor heaps, resource barriers, PSOs, HLSL with DXC, debugging with PIX."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-limits", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/shader-visible-descriptor-heaps", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-resource-barriers-to-synchronize-resource-states-in-direct3d-12", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_DynamicResources.md", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/ne-dxgi-dxgi_swap_effect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct3D 12: root signatures and command lists

**Goal:** structure a D3D12 renderer so command recording, resource binding and GPU/CPU
synchronisation are correct and fast — the parts D3D11 used to do for you.

## Objects and their lifetimes
| Object | What it is | Rule |
|---|---|---|
| `ID3D12CommandQueue` | GPU queue (direct/compute/copy) | Usually one direct queue; extra async compute/copy queues are an optimisation. |
| `ID3D12CommandAllocator` | Backing memory for recorded commands | **One per frame in flight per recording thread.** Can only be `Reset()` once the GPU has finished with it (fence). |
| `ID3D12GraphicsCommandList` | The recorder | Can be reset and reused immediately after `ExecuteCommandLists`, with an idle allocator. |
| `ID3D12Fence` | 64-bit GPU-signalled counter | CPU waits on a value; the frame pacing primitive. |
| `ID3D12PipelineState` (PSO) | Shaders + blend/raster/depth state + formats, baked | Create at load time, not on the hot path. Cache with a pipeline library (`ID3D12PipelineLibrary`). |

## Frame loop with a fence
```cpp
// per frame index i: allocator[i], fenceValue[i]; swap chain with FrameCount = 2 or 3 buffers
void Render() {
    UINT i = swapChain->GetCurrentBackBufferIndex();
    if (fence->GetCompletedValue() < fenceValue[i]) {           // GPU still using frame i's resources?
        fence->SetEventOnCompletion(fenceValue[i], fenceEvent);
        WaitForSingleObject(fenceEvent, INFINITE);
    }
    allocator[i]->Reset();
    cmd->Reset(allocator[i].Get(), pso.Get());
    // barrier backbuffer PRESENT -> RENDER_TARGET, set root sig/heaps, draw, barrier -> PRESENT
    cmd->Close();
    ID3D12CommandList* lists[] = { cmd.Get() };
    queue->ExecuteCommandLists(1, lists);
    swapChain->Present(1, 0);                                    // 1 = vsync; tearing needs flags + 0
    fenceValue[i] = ++currentFence;
    queue->Signal(fence.Get(), fenceValue[i]);
}
```
Use a flip-model swap effect such as `DXGI_SWAP_EFFECT_FLIP_DISCARD` (not usable with multisampling).
Upload/constant buffers written by the CPU each frame also need one copy per frame in flight.

## Root signatures and descriptors
The root signature is the function signature of your shaders: what's bound and how.
- Root parameter costs (64 DWORD max): root **constants** = 1 DWORD each, root **descriptors**
  (CBV/SRV/UAV GPU virtual addresses) = 2 DWORDs, descriptor **tables** = 1 DWORD (pointer
  into a heap range).
- Shader-visible **descriptor heaps**: one CBV/SRV/UAV heap and one sampler heap set
  at a time (`SetDescriptorHeaps`); on some hardware switching heaps needs a GPU wait for idle —
  allocate one big heap and sub-allocate ranges (ring buffer per frame for transient
  descriptors).
- Static samplers do not count towards the root signature size; use them for common samplers.
- **Bindless (SM 6.6):** `ResourceDescriptorHeap[index]` in HLSL with the
  `CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED` root signature flag; pass indices as root constants.
  Simplifies binding enormously on supported hardware/drivers (check feature support).

```hlsl
// HLSL, compiled with DXC: dxc -T ps_6_6 -E main -Zi -Qembed_debug shader.hlsl -Fo shader.cso
struct DrawData { uint albedoIndex; uint samplerIndex; };
ConstantBuffer<DrawData> draw : register(b0);       // root constants
float4 main(float2 uv : TEXCOORD0) : SV_Target {
    Texture2D tex    = ResourceDescriptorHeap[draw.albedoIndex];
    SamplerState smp = SamplerDescriptorHeap[draw.samplerIndex];
    return tex.Sample(smp, uv);
}
```
FXC (`fxc.exe`, SM ≤ 5.1) is legacy; use **DXC** for Shader Model 6.x.

## Resource barriers
- Transition states explicitly: render target → shader resource, copy dest → pixel
  shader resource, etc. Batch multiple barriers into one `ResourceBarrier` call.
- Split barriers (`BEGIN_ONLY`/`END_ONLY`) let the GPU overlap the transition with work.
- **Enhanced Barriers** (newer Agility SDK / drivers) separate sync, access and layout
  like Vulkan — prefer them for new code where supported (`EnhancedBarriersSupported` in
  `D3D12_FEATURE_DATA_D3D12_OPTIONS12`).
- Buffers and simultaneous-access textures are implicitly promoted from `COMMON` on first
  use; non-simultaneous-access textures cannot be promoted to render target or depth states.

## Debugging
- Enable the debug layer (`D3D12GetDebugInterface` → `EnableDebugLayer`) in dev builds and
  GPU-based validation for binding/state bugs (slow, use selectively). Break on errors via
  `ID3D12InfoQueue`.
- Device removed (`DXGI_ERROR_DEVICE_REMOVED`)? Call `GetDeviceRemovedReason`, enable
  DRED (auto-breadcrumbs + page fault data) to find the faulting command.
- **PIX on Windows**: GPU captures for per-draw state and timing; timing captures for
  CPU/GPU overlap. Name objects with `SetName` and use PIX markers.
- Ship the **Agility SDK** to get newer D3D12 features independent of the Windows version.

## Verify
- [ ] Debug layer silent over a session including resize and fullscreen toggle.
- [ ] Allocators and CPU-written buffers are per frame in flight and fence-guarded.
- [ ] No PSO creation during gameplay (hitches) — check PIX timing capture.
- [ ] Barriers batched; no redundant transitions in a GPU capture.
- [ ] DRED enabled in test builds so device-removed reports are actionable.

## Checked

2026-10-26. Checked against the Microsoft Learn root signature limits, descriptor heaps, shader-visible heaps and barrier pages,
the d3d12.h header (D3D12_ROOT_SIGNATURE_FLAG_CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED, EnhancedBarriersSupported), the
DXGI_SWAP_EFFECT page and the DXC option definitions (win32, sdk-api, DirectX-Headers and DirectXShaderCompiler
repositories, commits to 2026-10). Confirmed: 64 DWORD limit and per-entry costs (1/2/1), static samplers cost no
root space, heap-switch GPU wait on some hardware, promotion table, flip discard restriction, dxc -Zi/-Qembed_debug.
Removed the unconfirmed PSO-millisecond and parameter-order guidance.
Method: documentation only; no commands were run.
