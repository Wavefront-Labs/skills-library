---
id: computing-software.computer-graphics-engineering.opengl.vulkan-profiles-and-roadmap-targets
name: vulkan-profiles-and-roadmap-targets
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-device, vulkan-profiles, vulkan-roadmap, android-baseline]
level: advanced
status: docs-checked
description: "Target Vulkan capability sets with profiles (Roadmap 2022/2024/2026, Android and LunarG baselines): checking support, the profiles library, and the profiles layer."
sources: ["https://docs.vulkan.org/guide/latest/vulkan_profiles.html", "https://github.com/KhronosGroup/Vulkan-Profiles", "https://docs.vulkan.org/spec/latest/appendices/roadmap.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan profiles and roadmap targets

A profile is a named JSON bundle of required version, extensions, features, limits and formats.
Instead of checking 40 individual things, you check one profile.

## Useful profiles
| Profile | Scope |
|---|---|
| `VP_KHR_roadmap_2022` | requires Vulkan 1.3, optional features such as `descriptorIndexing`, and raised limits |
| `VP_KHR_roadmap_2024` | requires Roadmap 2022; adds `VK_KHR_dynamic_rendering_local_read`, `VK_KHR_maintenance5`, `VK_KHR_push_descriptor`, `multiDrawIndirect`, 8/16-bit shader types, line rasterization and more |
| `VP_KHR_roadmap_2026` | requires Roadmap 2024 and Vulkan 1.4; adds swapchain/present guarantees (for example `VK_KHR_present_id2`, `VK_KHR_present_wait2`) and extensions such as `VK_KHR_fragment_shading_rate` |
| `VP_ANDROID_baseline_2022` | Android baseline; requires Vulkan 1.1 core (Vulkan Guide) |
| `VP_LUNARG_desktop_baseline_2022` (also 2023, 2024, 2026 in the repository) | desktop baseline built from GPUinfo.org reports; intended as an example for your own profiles |

## Check and create with the profiles library
```cpp
#include <vulkan/vulkan_profiles.hpp>
VpProfileProperties profile{ VP_KHR_ROADMAP_2022_NAME, VP_KHR_ROADMAP_2022_SPEC_VERSION };
VkBool32 ok = VK_FALSE;
vpGetPhysicalDeviceProfileSupport(instance, gpu, &profile, &ok);   // returns VkResult
if (ok) {
    VkDeviceCreateInfo dci{ VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO };
    dci.queueCreateInfoCount = 1; dci.pQueueCreateInfos = &qci;
    VpDeviceCreateInfo vci{}; vci.pCreateInfo = &dci;
    vci.enabledFullProfileCount = 1; vci.pEnabledFullProfiles = &profile;
    vpCreateDevice(gpu, &vci, nullptr, &device);   // enables all profile extensions/features
}
```
The header is generated from the profile JSON files (`gen_profiles_solution.py` in the Vulkan-Profiles repository) and ships in the Vulkan SDK.

## Test on the minimum with the profiles layer
`VK_LAYER_KHRONOS_profiles` makes a more capable GPU *simulate* a profile by modifying the features, limits and
extensions it reports. Its layer settings include `profile_dirs`, `profile_name` and `simulate_capabilities`
(values such as `SIMULATE_API_VERSION_BIT`, `SIMULATE_FEATURES_BIT`, `SIMULATE_PROPERTIES_BIT`); set them in vkconfig or the layer settings file
(see the LunarG profiles layer documentation for exact variable names). Per the layer's tutorial it simulates rather than emulates: it
does not add missing hardware capability, so still test on real low-end devices. Order the profiles layer last (closest to the driver) so the validation layer sees the simulated capabilities.

## Writing your own profile
Create a JSON in the Vulkan-Profiles schema listing exactly what your engine requires; generate
the header with `gen_profiles_solution.py`; use the same JSON in the profiles layer.

## Gotchas
- A profile passing doesn't mean good performance; it only means features exist.
- Roadmap profiles are forward-looking targets (the Guide describes them as capabilities vendors are encouraged to support); ship a fallback path or require a baseline profile.

## Verify
- [ ] Startup logs which profile is supported; app runs clean under the profiles layer emulating your minimum profile.

## Checked
Checked 2026-10-26 against Vulkan-Docs appendices/roadmap/Roadmap-2022/2024/2026.adoc (v1.4.366), Vulkan-Headers registry/profiles/VP_KHR_roadmap.json, the Vulkan Guide vulkan_profiles chapter, and the Vulkan-Profiles repository (scripts/gen_profiles_solution.py, layer/VkLayer_khronos_profiles.json.in, layer/TUTORIAL.md).
Confirmed: roadmap profile names and requirements; Android Baseline 2022 needs Vulkan 1.1; LunarG desktop baseline directories (2022, 2023, 2024, 2026); vpGetPhysicalDeviceProfileSupport and vpCreateDevice signatures, VpDeviceCreateInfo full-profile fields and generated NAME/SPEC_VERSION macros; layer name and the settings keys profile_dirs, profile_name, simulate_capabilities. Removed the Android 2021 profile, maintenance6 under Roadmap 2024, and unconfirmed environment variable names.
Method: documentation only; no commands were run.
