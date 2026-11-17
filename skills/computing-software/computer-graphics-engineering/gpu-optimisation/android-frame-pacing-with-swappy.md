---
id: computing-software.computer-graphics-engineering.gpu-optimisation.android-frame-pacing-with-swappy
name: android-frame-pacing-with-swappy
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, swappy, android-frame-pacing, agdk, vulkan-android, choreographer]
level: sme
status: draft
description: "Pace frames on Android with Swappy (AGDK Frame Pacing): GL and Vulkan integration, swap intervals for 30/60/90/120 Hz, and verifying stutter with systrace."
sources: ["https://developer.android.com/games/sdk/frame-pacing", "https://developer.android.com/games/sdk/frame-pacing/vulkan/vulkan-integrate", "https://developer.android.com/games/sdk/frame-pacing/opengl/add-functions", "https://developer.android.com/games/optimize/frame-pacing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Frame pacing on Android (Swappy)

## 1. Problem
Rendering at 30 fps on a 60 Hz display without pacing presents frames at uneven intervals (16.7/50 ms
alternating), which looks worse than steady 30. Also, without a timestamp hint, a frame can be shown too early
and the next one late, plus deep buffer queues add latency.

## 2. Vulkan integration
```cpp
#include "swappy/swappyVk.h"
// after creating the device: tell Swappy which queue family is used
SwappyVk_setQueueFamilyIndex(device, queue, queueFamilyIndex);
uint64_t refreshNs;
SwappyVk_initAndGetRefreshCycleDuration(env, activity, physDev, device, swapchain, &refreshNs);
SwappyVk_setWindow(device, swapchain, nativeWindow);
SwappyVk_setSwapIntervalNS(device, swapchain, SWAPPY_SWAP_30FPS);   // or refreshNs for native rate
// replace vkQueuePresentKHR with:
SwappyVk_queuePresent(queue, &presentInfo);
// on swapchain destroy:
SwappyVk_destroySwapchain(device, swapchain);
```
Requires the AGDK games-frame-pacing library (Maven `androidx.games:games-frame-pacing`, prefab).

## 3. OpenGL ES integration
```cpp
SwappyGL_init(env, activity);
SwappyGL_setWindow(window);
SwappyGL_setSwapIntervalNS(SWAPPY_SWAP_60FPS);
// replace eglSwapBuffers(display, surface) with:
SwappyGL_swap(display, surface);
// on shutdown: SwappyGL_destroy();
```
Swappy uses Choreographer vsync timing and `EGL_ANDROID_presentation_time` to pin each frame's present time.

## 4. Settings
- Choose an interval that the device sustains: 60 on 120 Hz panels uses swap interval 2 refreshes; 30 on 90 Hz
  is not an integer divisor - Swappy can switch display mode, or pick 45.
- `SwappyGL_setAutoSwapInterval(true)` / `SwappyVk_setAutoSwapInterval` lets Swappy drop to a lower rate when
  frames keep missing; `setAutoPipelineMode` trades latency for smoothness.
- Request the matching display refresh rate via `ANativeWindow_setFrameRate` (Android 11+); Swappy does this
  when allowed.

## Gotchas
- Calling `vkQueuePresentKHR` directly anywhere bypasses pacing.
- `VK_PRESENT_MODE_FIFO_KHR` only; Swappy expects FIFO.
- Frame pacing hides nothing if frames exceed the budget: fix GPU/CPU time first.

## Verify
- [ ] Perfetto/systrace: SurfaceFlinger shows frames latched at a constant interval; Android vitals "slow
  frames" and frame time histogram show a single peak at the target.
