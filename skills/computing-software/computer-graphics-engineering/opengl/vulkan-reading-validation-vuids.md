---
id: computing-software.computer-graphics-engineering.opengl.vulkan-reading-validation-vuids
name: vulkan-reading-validation-vuids
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-debugging, vuid, validation-errors, validation-triage]
level: practitioner
status: docs-checked
description: "Read Vulkan validation messages: decode VUIDs, find the spec rule, map handles to names, break on error, and fix the ten most common errors."
sources: ["https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/error_messages.md", "https://docs.vulkan.org/guide/latest/validation_overview.html", "https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/khronos_validation_layer.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading validation errors (VUIDs)

## Anatomy of a message
```text
Validation Error: [ VUID-vkCmdSetScissor-firstScissor-00593 ] | MessageID = 0x603fac6b
vkCmdSetScissor(): firstScissor is 1 but the multiViewport feature was not enabled.
The Vulkan spec states: If the multiViewport feature is not enabled, firstScissor must be 0 (https://docs.vulkan.org/spec/latest/chapters/fragops.html#VUID-vkCmdSetScissor-firstScissor-00593)
Objects: 1
   [0] VkCommandBuffer 0x...
```
(Format from the Validation Layers' error_messages document.) In order: severity, the VUID, a message ID (a hash of the VUID),
the function, the faulty parameter or member, the main message, the spec wording and a link.
- A **VUID** is a unique ID per valid usage; add it to the spec HTML as an anchor (`#VUID-...`) to read the exact rule.
  A number in the ID (`...-01044`) marks an explicit valid usage; `...-parameter` marks an implicit one.
- Object names appear only if you name objects (`vkSetDebugUtilsObjectNameEXT`): name everything.

## Workflow
1. Make the debug messenger callback **break into the debugger** on errors in debug builds
   (`__debugbreak()` / `raise(SIGTRAP)`) so the call stack points at the offending API call.
2. Fix the **first** error of a run; later ones are often consequences.
3. Filter only message IDs you understand with the layer's `message_id_filter` setting; never blanket-disable a category.

## Common errors and fixes
| VUID / message | Usual cause | Fix |
|---|---|---|
| `vkCmdDraw-imageLayout-00344` "expects layout X, actual Y" | missing transition or wrong tracked layout | add barrier; track layouts per subresource |
| `vkCmdDraw-None-08600` / `-08114` descriptor set not bound / descriptors not valid | set not bound after layout-incompatible pipeline bind, or binding never written | bind sets after pipeline; write all statically used bindings or PARTIALLY_BOUND |
| `vkQueueSubmit-pCommandBuffers-00071` simultaneous use | resubmitting a command buffer still pending | per-frame command buffers + fences |
| `vkDestroyBuffer-buffer-00922` in use | destroying while GPU uses it | deferred deletion queue per frame |
| `vkQueueSubmit-pSignalSemaphores-00067` semaphore possibly still in use by present | one present-wait semaphore per frame in flight | per-image render-finished semaphores |
| `vkCmdDraw-colorAttachmentCount-06179` and neighbours | pipeline rendering formats differ from the attachments | match `VkPipelineRenderingCreateInfo` formats |
| `vkCmdPushConstants-offset-01795` / `-01796` | push constant range not covered, or stage flags mismatch | one range covering all stages and sizes |
| `vkCmdBindDescriptorSets-pDynamicOffsets-01971` | dynamic uniform offset not a multiple of `minUniformBufferOffsetAlignment` | align offsets to the limit |
| `VkShaderModuleCreateInfo-pCode-08739` / `-08740` | SPIR-V capability without the matching feature or extension | enable it at device creation |
| `vkBindBufferMemory-memory-01035` | allocation type not in `memoryTypeBits` | select type from requirements |

## Other layers worth enabling periodically
- Synchronization validation (the `validate_sync` layer setting).
- GPU-assisted validation (off by default; it inspects GPU resources and instruments shaders at run time) and debug printf.
- Best practices validation (performance issues, questionable usage patterns and common mistakes).

## Verify
- [ ] Zero validation errors over an automated playthrough; CI runs a headless frame capture with validation and fails on any error.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json for every VUID in the table), the Vulkan Guide validation_overview chapter and the Vulkan-ValidationLayers docs (error_messages.md, gpu_validation.md, best_practices.md, syncval_usage.md, khronos_validation_layer.md).
Confirmed: the VUIDs listed exist with the described meaning; VUID anatomy and explicit/implicit numbering; message layout; message_id_filter setting; validate_sync; GPU-AV off by default; best-practices scope. Corrected the example VUIDs (the earlier pipeline-format and imageLayout names were not real), removed UNASSIGNED id claim, vendor suffix claim and the vkconfig Break action.
Method: documentation only; no commands were run.
