---
id: computing-software.computer-graphics-engineering.opengl.vulkan-validation-layers-and-debug-utils
name: vulkan-validation-layers-and-debug-utils
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-instance, validation-layers, debug-utils-messenger, vk-layer-khronos-validation, vkconfig, gpu-assisted-validation, best-practices-validation, vk-ext-debug-utils]
level: practitioner
status: docs-checked
description: "Enable VK_LAYER_KHRONOS_validation with a debug-utils messenger, turn on GPU-assisted, sync and best-practices checks via vkconfig or layer settings, and triage messages."
sources: ["https://docs.vulkan.org/spec/latest/chapters/debugging.html", "https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/khronos_validation_layer.md", "https://github.com/KhronosGroup/Vulkan-ValidationLayers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan validation layers and debug utils

**Goal:** every API misuse reported with the object names and a stack trace, during
development, at zero cost in release.

## 1. Instance creation with the layer and messenger
```cpp
const char* layers[] = {"VK_LAYER_KHRONOS_validation"};
const char* exts[]   = {VK_EXT_DEBUG_UTILS_EXTENSION_NAME, /* + surface exts */};
VkDebugUtilsMessengerCreateInfoEXT dbg{VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT};
dbg.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT | VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
dbg.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT | VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
                  VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;
dbg.pfnUserCallback = onVkMessage;          // return VK_FALSE always
VkInstanceCreateInfo ci{VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO};
ci.pNext = &dbg;                            // also catches messages from vkCreateInstance itself
ci.enabledLayerCount = 1; ci.ppEnabledLayerNames = layers;
```
Then create a persistent messenger with `vkCreateDebugUtilsMessengerEXT` (loaded via
`vkGetInstanceProcAddr` or volk). Check the layer exists with
`vkEnumerateInstanceLayerProperties` — on machines without the SDK, creation fails with
`VK_ERROR_LAYER_NOT_PRESENT`.

## 2. Callback
```cpp
VKAPI_ATTR VkBool32 VKAPI_CALL onVkMessage(VkDebugUtilsMessageSeverityFlagBitsEXT sev,
    VkDebugUtilsMessageTypeFlagsEXT, const VkDebugUtilsMessengerCallbackDataEXT* d, void*) {
    fprintf(stderr, "[%s] %s\n", d->pMessageIdName, d->pMessage);
    for (uint32_t i = 0; i < d->objectCount; ++i)
        fprintf(stderr, "   obj %s\n", d->pObjects[i].pObjectName ? d->pObjects[i].pObjectName : "?");
    if (sev & VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT) DEBUG_BREAK();
    return VK_FALSE;
}
```
Each message carries a **VUID** (for example `VUID-vkCmdDraw-None-08600`): search it in the spec for
the exact rule broken.

## 3. Extra validation modes
Off by default because they are slow; turn on per investigation:
- **Synchronization validation** — hazards between commands/queues.
- **GPU-assisted validation** — checks that need run-time data (buffer contents, how shaders index descriptor arrays); off by default because of its overhead.
- **Best practices** — potential performance issues, questionable usage patterns and common mistakes.
- **Debug printf** — `debugPrintfEXT` from shaders.
The layer documentation lists four ways to configure settings: the **vkconfig** GUI (SDK), application-defined `VK_EXT_layer_settings`
(`VkLayerSettingsCreateInfoEXT`, for example a bool setting named `validate_sync`), a `vk_layer_settings.txt` file found via `VK_LAYER_SETTINGS_PATH`, and environment variables (for example `VK_VALIDATION_VALIDATE_SYNC=1`).
Env override without code: `VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation`.

## Gotchas
- Messages that mention handles as hex only: name your objects
  (`vkSetDebugUtilsObjectNameEXT`) — the payoff is immediate.
- Validation lags new extensions; a false positive on a brand-new extension is possible
  — update the SDK before suppressing.
- Don't ship with the layer enabled: it adds CPU overhead (more with the optional modes above). Gate on a debug flag.
- Suppress specific VUIDs only with a comment explaining why (the layer's `message_id_filter` setting).

## Verify
- [ ] A clean run (including resize and shutdown) produces zero validation messages.
- [ ] Destroying a buffer still in use triggers an error that names the buffer.
- [ ] CI runs a headless frame with validation + sync validation and fails on any error.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/debugging.adoc, appendices/VK_EXT_debug_utils.adoc, xml/vk.xml) and the Vulkan-ValidationLayers docs (khronos_validation_layer.md, syncval_usage.md, gpu_validation.md, best_practices.md, error_messages.md).
Confirmed: debug-utils messenger chained into VkInstanceCreateInfo pNext covers vkCreateInstance; callback should always return VK_FALSE; VK_ERROR_LAYER_NOT_PRESENT exists; four settings routes and the VK_LAYER_SETTINGS_PATH file; validate_sync; message_id_filter; GPU-AV off by default; best-practices scope; debugPrintfEXT from the debug printf document. Replaced a non-existent example VUID and removed the 2-10x overhead figure and vendor suffix claims.
Method: documentation only; no commands were run.
