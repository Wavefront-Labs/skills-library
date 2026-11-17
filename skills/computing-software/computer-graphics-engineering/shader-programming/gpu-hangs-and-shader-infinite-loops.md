---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-hangs-and-shader-infinite-loops
name: gpu-hangs-and-shader-infinite-loops
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, gpu-hang, tdr, device-lost, dred, nsight-aftermath, infinite-loop]
level: advanced
status: docs-checked
description: "Debug GPU hangs and TDRs caused by shaders: infinite loops, out-of-bounds access, D3D12 DRED breadcrumbs, Vulkan device-lost diagnostics, Aftermath and loop guards."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/use-dred", "https://developer.nvidia.com/nsight-aftermath", "https://docs.vulkan.org/spec/latest/chapters/devsandqueues.html#devsandqueues-lost-device"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU hangs and infinite loops in shaders

## 1. Symptoms
- Windows: screen freezes, then TDR (Timeout Detection and Recovery) resets the driver;
  D3D12 reports device removal (`DXGI_ERROR_DEVICE_REMOVED`); Vulkan returns
  `VK_ERROR_DEVICE_LOST`.
- Other platforms: read the driver's own log for the hang or reset message.

## 2. Common shader causes
- Loops whose exit depends on data that never converges (ray marching without a step cap, while
  loops on floats, linked-list traversal of a corrupted list).
- Spin locks between lanes of the same wave.
- Out-of-bounds reads/writes with robustness disabled (can hang or page fault).
- Reading uninitialised indices that produce huge loop counts.

## 3. Find which draw/dispatch
**D3D12 DRED** (Device Removed Extended Data):
```cpp
ComPtr<ID3D12DeviceRemovedExtendedDataSettings> s;
D3D12GetDebugInterface(IID_PPV_ARGS(&s));
s->SetAutoBreadcrumbsEnablement(D3D12_DRED_ENABLEMENT_FORCED_ON);
s->SetPageFaultEnablement(D3D12_DRED_ENABLEMENT_FORCED_ON);
// after removal: ID3D12DeviceRemovedExtendedData::GetAutoBreadcrumbsOutput / GetPageFaultAllocationOutput
```
Auto-breadcrumbs record which render ops (draws, dispatches, copies) completed before the removal; the counter may be imprecise because the GPU is pipelined, and the feature is off by default because it costs some performance.

**Vulkan**: `VK_EXT_device_fault` (fault info), `VK_NV_device_diagnostic_checkpoints`
(`vkCmdSetCheckpointNV`), `VK_AMD_buffer_marker` (write markers to a buffer after each pass).

**Vendor**: NVIDIA Nsight Aftermath produces GPU crash dumps; see the vendor's page for supported APIs.

## 4. Loop guards
```glsl
for (int i = 0; i < MAX_STEPS; i++) {   // MAX_STEPS: your own constant ... if (done) break; }   // never unbounded while()
```
Debug builds: add a counter that writes a sentinel colour/flag when the cap is hit.

## 5. Debugging workflow
1. Reproduce with markers enabled; identify the pass.
2. Bisect by disabling draws in that pass or simplifying the shader.
3. Enable the API's robust buffer access feature to see if it is out-of-bounds.
4. Raising the TDR timeout (see Microsoft's TDR registry keys page) is only for diagnosing long-running legitimate work, never a fix.

## Gotchas
- After device loss every API call fails; log markers immediately, don't try to continue rendering.
- Hangs caused by a previous frame's corrupt data appear in an innocent pass; check resource
  producers too.

## Verify
- [ ] Crash pipeline (DRED/Aftermath) produces reports in test builds.
- [ ] All shader loops have explicit caps.

## Checked
2026-11-01. Confirmed from Microsoft Learn DRED page (auto-breadcrumbs, page-fault reporting, FORCED_ON setting, imprecision, off by default, `GetAutoBreadcrumbsOutput`), TDR page, Vulkan spec lost-device section, and Khronos refpages for `VK_EXT_device_fault`, `VK_NV_device_diagnostic_checkpoints`, `VK_AMD_buffer_marker`; NVIDIA Aftermath page. Removed: TDR delay figure and registry path, Linux and WebGL log strings, `DEVICE_HUNG`, `robustBufferAccess2`, Radeon GPU Detective, shader-line claim (not confirmed in fetched pages).
Method: documentation only; no commands were run.
