---
id: computing-software.computer-graphics-engineering.opengl.vulkan-pipeline-cache-and-compile-stutter
name: vulkan-pipeline-cache-and-compile-stutter
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-pipelines, graphics-pipeline, pipeline-cache, vkpipelinecache, pipeline-library, graphics-pipeline-library, shader-compile-stutter, pso-precompilation]
level: advanced
status: docs-checked
description: "Kill Vulkan shader-compile hitches: persist VkPipelineCache to disk with header validation, precompile known pipelines on worker threads, and use graphics pipeline libraries."
sources: ["https://docs.vulkan.org/spec/latest/chapters/pipelines.html#pipelines-cache", "https://docs.vulkan.org/guide/latest/pipeline_cache.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan pipeline cache and compile stutter

**Goal:** no frame hitches from creating pipelines at draw time; warm starts in
milliseconds instead of seconds.

## 1. Persist the cache
```cpp
std::vector<char> blob = readFile(cachePath);
if (!validHeader(blob, props)) blob.clear();                 // see below
VkPipelineCacheCreateInfo ci{VK_STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO};
ci.initialDataSize = blob.size(); ci.pInitialData = blob.data();
vkCreatePipelineCache(dev, &ci, nullptr, &cache);
// ... pass `cache` to every vkCreateGraphicsPipelines / vkCreateComputePipelines ...
// on shutdown (and periodically):
size_t sz; vkGetPipelineCacheData(dev, cache, &sz, nullptr);
std::vector<char> out(sz); vkGetPipelineCacheData(dev, cache, &sz, out.data());
writeFileAtomic(cachePath, out);                             // temp file + rename
```
**Validate the header yourself** (`VkPipelineCacheHeaderVersionOne`: vendorID, deviceID,
pipelineCacheUUID) against `VkPhysicalDeviceProperties`. The spec says incompatible initial data leaves the cache empty rather than
failing, but a corrupted file can still be malformed, so also store your own size + hash wrapper and discard on mismatch.

## 2. Know your pipelines ahead of time
- Record every (shader set, vertex layout, render-target formats, blend/depth state) the
  game actually uses during QA runs; ship that list.
- At load (or a startup "compiling shaders" screen), create them on worker threads —
  `vkCreate*Pipelines` may be called concurrently with a shared cache (the cache is internally synchronised unless
  created with `VK_PIPELINE_CACHE_CREATE_EXTERNALLY_SYNCHRONIZED_BIT`).
- Minimise permutations: move cheap state to dynamic state (viewport, scissor, cull mode,
  depth test via extended dynamic state).

## 3. Graphics pipeline library (VK_EXT_graphics_pipeline_library)
Split into vertex-input, pre-rasterisation (VS), fragment shader and fragment-output parts;
compile parts early, **link fast** at draw time (omit `VK_PIPELINE_CREATE_LINK_TIME_OPTIMIZATION_BIT_EXT`
for the fast link; the spec says linking is then quicker but device performance may be lower), then recompile the optimised version in the background and swap.

## 4. Feedback
`VkPipelineCreationFeedbackCreateInfo` tells you per pipeline whether it hit the cache
(`APPLICATION_PIPELINE_CACHE_HIT_BIT`) and how long it took. Log misses in QA builds.

## Gotchas
- Driver-side shader caches can hide the problem on dev machines; test with them cleared
  (see each vendor's documentation for how).
- Merging caches from multiple threads: `vkMergePipelineCaches`; or share one.
- Shader objects (`VK_EXT_shader_object`) are an alternative to pipelines; measure first-use cost there too.

## Verify
- [ ] Cold start with cleared driver cache: frame-time graph shows no hitch in gameplay
      after the precompile phase.
- [ ] Warm start: pipeline creation feedback reports `APPLICATION_PIPELINE_CACHE_HIT` for the pipelines you precompiled.
- [ ] A corrupted cache file is rejected cleanly (no crash) and rebuilt.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/pipelines.adoc, xml/vk.xml) and the Vulkan Guide pipeline_cache chapter.
Confirmed: VkPipelineCacheHeaderVersionOne fields (vendorID, deviceID, pipelineCacheUUID); incompatible initial data gives an empty cache; EXTERNALLY_SYNCHRONIZED_BIT semantics; link-time optimisation bit as a host/device trade-off; creation feedback bit APPLICATION_PIPELINE_CACHE_HIT. Removed the DXVK, driver-crash, environment-variable and 95 percent claims.
Method: documentation only; no commands were run.
