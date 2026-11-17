---
id: computing-software.computer-graphics-engineering.opengl.vulkan-pipeline-creation-feedback-and-binaries
name: vulkan-pipeline-creation-feedback-and-binaries
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, pipeline-creation-feedback, pipeline-binaries, fail-on-compile-required]
level: advanced
status: docs-checked
description: "Measure Vulkan pipeline compile cost and cache hits with creation feedback, use FAIL_ON_PIPELINE_COMPILE_REQUIRED, and VK_KHR_pipeline_binary for explicit caching."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/pipelines.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_pipeline_binary.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline creation feedback, cache control and binaries

## Creation feedback (core 1.3)
```c
VkPipelineCreationFeedback whole, stages[2];
VkPipelineCreationFeedbackCreateInfo fb = { VK_STRUCTURE_TYPE_PIPELINE_CREATION_FEEDBACK_CREATE_INFO };
fb.pPipelineCreationFeedback = &whole;
fb.pipelineStageCreationFeedbackCount = 2; fb.pPipelineStageCreationFeedbacks = stages;
gpci.pNext = &fb;
vkCreateGraphicsPipelines(dev, cache, 1, &gpci, NULL, &pipe);
bool hit = whole.flags & VK_PIPELINE_CREATION_FEEDBACK_APPLICATION_PIPELINE_CACHE_HIT_BIT;
double ms = whole.duration / 1e6;   // nanoseconds
```
Log name, duration and cache-hit per pipeline at load time and in a telemetry build. Pipelines
created mid-gameplay with long durations are your stutter list.

## Don't compile on the render thread (core 1.3 cache control)
```c
gpci.flags |= VK_PIPELINE_CREATE_FAIL_ON_PIPELINE_COMPILE_REQUIRED_BIT;
VkResult r = vkCreateGraphicsPipelines(dev, cache, 1, &gpci, NULL, &pipe);
if (r == VK_PIPELINE_COMPILE_REQUIRED) { queueBackgroundCompile(gpci); useFallbackPipeline(); }
```
Creation fails with `VK_PIPELINE_COMPILE_REQUIRED` (and the pipeline handle is `VK_NULL_HANDLE`) if a compile would be required. Pair with
`VK_PIPELINE_CREATE_EARLY_RETURN_ON_FAILURE_BIT` for batches. Fallbacks: a simpler shader, or skip
the draw for a frame (with pipeline libraries, link a fast unoptimised variant).

`VK_PIPELINE_CACHE_CREATE_EXTERNALLY_SYNCHRONIZED_BIT` declares that all commands modifying the cache are externally synchronised, so the
implementation may skip internal locking (for example one cache per thread, merged with `vkMergePipelineCaches`).

## Explicit binaries (VK_KHR_pipeline_binary)
Instead of an opaque `VkPipelineCache` blob, retrieve per-pipeline binaries with keys:
```c
VkPipelineBinaryCreateInfoKHR bci = { VK_STRUCTURE_TYPE_PIPELINE_BINARY_CREATE_INFO_KHR };
bci.pipeline = pipe;                                   // capture from a created pipeline
vkCreatePipelineBinariesKHR(dev, &bci, NULL, &handles);
vkGetPipelineBinaryDataKHR(dev, &info, &key, &size, data);   // store data under key in your own DB
// next run: vkCreatePipelineBinariesKHR from data, then chain VkPipelineBinaryInfoKHR at creation
```
Lets you manage binaries in your own store keyed by the returned `VkPipelineBinaryKeyKHR`. If the `pipelineBinaryInternalCacheControl`
property is true, `VkDevicePipelineBinaryInternalCacheControlKHR::disableInternalCache` turns off the driver's internal cache; if
`pipelineBinaryPrefersInternalCache` is true, the implementation prefers its internal cache and applications should not keep their own
on-disk copies of binaries.

## Gotchas
- Cache blobs are driver/device specific; validate the header (`vendorID`, `deviceID`,
  `pipelineCacheUUID`) before loading, and expect misses after driver updates.
- Pipeline derivatives (`VK_PIPELINE_CREATE_DERIVATIVE_BIT`) need a parent created with the allow-derivatives flag; don't rely on them for speed.

## Verify
- [ ] Load log shows >95% cache hits on second run; no pipeline creation during gameplay over a budget (e.g. 1 ms).

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and vk.xml. Confirmed: `VkPipelineCreationFeedback::duration` is in nanoseconds; `VK_PIPELINE_CREATE_FAIL_ON_PIPELINE_COMPILE_REQUIRED_BIT` makes creation fail with `VK_PIPELINE_COMPILE_REQUIRED` and a null pipeline; `EARLY_RETURN_ON_FAILURE` semantics; `VK_PIPELINE_CACHE_CREATE_EXTERNALLY_SYNCHRONIZED_BIT` semantics; pipeline creation feedback and cache control are promoted to Vulkan 1.3 (vk.xml); `vkCreatePipelineBinariesKHR` and `vkGetPipelineBinaryDataKHR` signatures and `VkPipelineBinaryCreateInfoKHR::pipeline`; the real meaning of `pipelineBinaryPrefersInternalCache` (implementation prefers its internal cache, applications should not store binaries in their own on-disk caches) and `pipelineBinaryInternalCacheControl`. Corrected the 'returns immediately unless in cache' wording and removed the derivative, caching-by-driver and zero-duration claims.

Method: documentation only; no commands were run.
