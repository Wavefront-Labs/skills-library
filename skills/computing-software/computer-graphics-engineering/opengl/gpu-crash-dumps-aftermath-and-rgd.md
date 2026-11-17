---
id: computing-software.computer-graphics-engineering.opengl.gpu-crash-dumps-aftermath-and-rgd
name: gpu-crash-dumps-aftermath-and-rgd
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-debugging, nsight-aftermath, radeon-gpu-detective, gpu-crash-dump]
level: sme
status: docs-checked
description: "Capture and read GPU crash dumps for Vulkan/D3D12 with NVIDIA Nsight Aftermath and AMD Radeon GPU Detective: setup, markers, shader debug info, triage."
sources: ["https://developer.nvidia.com/nsight-aftermath", "https://docs.nvidia.com/nsight-aftermath/", "https://gpuopen.com/radeon-gpu-detective/", "https://gpuopen.com/manuals/rgd_manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU crash dumps: Nsight Aftermath and Radeon GPU Detective

When the device is lost (TDR, page fault), these tools capture GPU state at the moment of the
crash: which draw/dispatch was executing, the faulting address and resource, and the shader.

## NVIDIA Nsight Aftermath
1. Integrate the Nsight Aftermath SDK into the game's crash reporter (D3D12 or Vulkan). The Aftermath Monitor (in the SDK and Nsight Graphics) collects crash information, and the API can add user markers and application metadata. Take the exact setup calls and Vulkan extension flags from the SDK documentation.
2. On device loss, let the SDK finish generating the dump before terminating the process (see the SDK docs for the status API).
3. Insert markers per pass so the dump shows the execution state of each marker.
4. Compile shaders with debug info and keep it so the viewer can map the crash to shader source; see the SDK docs for the callbacks.
5. Open the dump in Nsight Graphics. Aftermath reports which warps were running, the state of GPU subunits, details of the faulting unit and the marker execution state.

## AMD Radeon GPU Detective (RGD)
No SDK integration needed for basic use:
1. Enable crash analysis in Radeon Developer Panel (RDP) and start the app (Vulkan or D3D12).
2. After system recovery RDP lists a new `.rgd` file under recently collected dumps; convert it to a text or JSON summary from RDP (right-click) or with the `rgd` command line tool (`rgd -h`).
3. The report contains an execution marker tree (you can insert user markers with custom strings) and a page fault summary section.

## Gotchas
- Dumps can contain shader code and application data; treat them as confidential.

## Verify
- [ ] Forced crash in a test build produces a dump that names the correct pass and shader line on both vendors.

## Checked

2026-10-28. Confirmed: Nsight Aftermath integrates into D3D12 or Vulkan crash reporters, generates GPU mini-dumps on exception or TDR, reports warps, subunits, faulting unit and marker state, and the Aftermath Monitor ships in the SDK and Nsight Graphics (NVIDIA page); Radeon GPU Detective supports DirectX 12 and Vulkan, writes `.rgd` files, converts to text or JSON via RDP or the `rgd` CLI (`rgd -h`), and reports an execution marker tree, user markers and a page fault summary (AMD pages).
Removed (not in the fetched pages): `GFSDK_Aftermath_*` call names, `VK_NV_device_diagnostics_config` flags, `.nv-gpudmp`, `vkCmdSetCheckpointNV`, DXC/glslang debug flags, the `rgd --parse` invocation, `vkCmdBeginDebugUtilsLabelEXT`, shader-disassembly claim, resource-tracking cost claim, the triage recipe.

Method: documentation only; no commands were run.
