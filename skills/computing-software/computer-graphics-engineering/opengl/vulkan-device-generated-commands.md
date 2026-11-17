---
id: computing-software.computer-graphics-engineering.opengl.vulkan-device-generated-commands
name: vulkan-device-generated-commands
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, command-buffers, device-generated-commands, indirect-commands-layout, gpu-driven-rendering]
level: sme
status: docs-checked
description: "Generate Vulkan command sequences on the GPU with VK_EXT_device_generated_commands: layouts, execution sets for shader switching, preprocess buffers."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_device_generated_commands.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/device_generated_commands/generatedcommands.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device generated commands (VK_EXT_device_generated_commands)

Indirect draws let the GPU choose *counts and parameters*. DGC lets the GPU also change
**state between draws**: push constants, vertex/index buffers, and even the shader/pipeline
(via indirect execution sets). Equivalent of D3D12 ExecuteIndirect with state changes.

## Pieces
1. **Indirect commands layout** (`VkIndirectCommandsLayoutEXT`): the token sequence of one
   GPU-written record, e.g. `[EXECUTION_SET, PUSH_CONSTANT, INDEX_BUFFER, VERTEX_BUFFER, DRAW_INDEXED]` (at most one execution-set token, which must be first, and the action token must be last).
2. **Indirect execution set** (`VkIndirectExecutionSetEXT`): a table of pipelines or shader
   objects the GPU can pick by index per sequence.
3. **Preprocess buffer**: driver scratch memory, size from
   `vkGetGeneratedCommandsMemoryRequirementsEXT`.
4. **Sequence buffer**: your compute shader writes records matching the layout.

## Execution
```c
VkGeneratedCommandsInfoEXT gi = { VK_STRUCTURE_TYPE_GENERATED_COMMANDS_INFO_EXT };
gi.shaderStages = VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT;
gi.indirectExecutionSet = execSet;
gi.indirectCommandsLayout = layout;
gi.indirectAddress = seqBufAddr; gi.indirectAddressSize = seqBytes;   // buffer device addresses
gi.preprocessAddress = prepAddr; gi.preprocessSize = prepBytes;
gi.maxSequenceCount = maxSeq;
gi.sequenceCountAddress = countAddr;                                   // optional GPU count
vkCmdExecuteGeneratedCommandsEXT(cmd, VK_FALSE /*isPreprocessed*/, &gi);
```
Optionally call `vkCmdPreprocessGeneratedCommandsEXT(cmd, &gi, stateCmd)` earlier and pass
`isPreprocessed = VK_TRUE` to the execute call. The state command buffer must already hold the descriptor sets and
push constants that execution will use, and be from the same queue family. The spec notes that on some
implementations preprocessing has no effect on performance.

When preprocessing explicitly, barrier the compute shader that writes the sequence buffer to dst stage
`VK_PIPELINE_STAGE_2_COMMAND_PREPROCESS_BIT_EXT`, access `VK_ACCESS_2_COMMAND_PREPROCESS_READ_BIT_EXT` (the access the
spec defines for buffer inputs of the preprocess command). The execute command may itself write the preprocess
buffer whatever `isPreprocessed` says; the spec states the implementation inserts that synchronisation
(`DRAW_INDIRECT` to `COMMAND_PREPROCESS` and back with `INDIRECT_COMMAND_READ`). Read the synchronisation notes in
the generated-commands chapter for your exact case.

## When it pays
- GPU-driven renderers with many materials: per-object shader selection without CPU readback
  or bin-by-material passes.
- Scenes where CPU state-change recording dominates. If all objects share one pipeline,
  plain `vkCmdDrawIndexedIndirectCount` + bindless is simpler and as fast.

## Gotchas
- Check the `deviceGeneratedCommands` feature and the limits in
  `VkPhysicalDeviceDeviceGeneratedCommandsPropertiesEXT` (for example `maxIndirectCommandsTokenCount`,
  `maxIndirectSequenceCount`, `supportedIndirectCommandsShaderStages`).
- Pipelines used in execution sets must be created with `VK_PIPELINE_CREATE_2_INDIRECT_BINDABLE_BIT_EXT`
  (shader objects with `VK_SHADER_CREATE_INDIRECT_BINDABLE_BIT_EXT`) and compatible layouts.
- The older `VK_NV_device_generated_commands` has a different API; don't mix docs.

## Verify
- [ ] GPU capture shows generated draws with the expected pipeline switches; CPU recording time for the pass drops to near zero.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and vk.xml. Confirmed: all type, function, stage, access and flag names exist; `VkGeneratedCommandsInfoEXT` members (`shaderStages`, `indirectExecutionSet`, `indirectCommandsLayout`, `indirectAddress`, `indirectAddressSize`, `preprocessAddress`, `preprocessSize`, `maxSequenceCount`, `sequenceCountAddress`); `vkCmdPreprocessGeneratedCommandsEXT` takes a `stateCommandBuffer`; pipelines and shader objects in an execution set need the indirect-bindable create flags; the execution-set token must be first and the action token last; limit names `maxIndirectCommandsTokenCount`, `maxIndirectSequenceCount`, `supportedIndirectCommandsShaderStages`; `COMMAND_PREPROCESS_READ` is the access for preprocess buffer inputs. Replaced the vendor and driver support list (not documented in the specification) and the single-stage barrier advice with the spec's own wording.

Method: documentation only; no commands were run.
