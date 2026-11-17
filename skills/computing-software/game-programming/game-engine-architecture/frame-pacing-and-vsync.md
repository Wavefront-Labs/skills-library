---
id: computing-software.game-programming.game-engine-architecture.frame-pacing-and-vsync
name: frame-pacing-and-vsync
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, frame-pacing, vsync, input-latency, swappy, present-timing, dxgi-flip-model, reflex, game-programming]
level: advanced
status: docs-checked
description: "Deliver even frame times: why pacing breaks, Android Swappy modes and refresh rates, the DXGI flip model with present statistics for glitch recovery, and NVIDIA Reflex."
sources: ["https://developer.android.com/games/sdk/frame-pacing", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-flip-model", "https://developer.nvidia.com/performance-rendering-tools/reflex"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Frame pacing and vsync

**Goal:** each frame is shown for the same duration. Average fps hides uneven frame times.

## Why pacing breaks (Android frame pacing guide)
- A game rendering at a different rate than the display hardware gets inconsistent frame times. The
  guide's example: a 30 FPS loop on a 60 Hz device does not notice a repeated frame stays on screen
  an extra 16 ms, giving intervals such as 49, 16 and 33 ms. Overly complex scenes add missed frames.
- Submitting frames as fast as the API allows fills the display pipeline's queue (typically size 2);
  the render thread then blocks in the GL or Vulkan call. This buffer-stuffing adds a frame of
  latency and worsens inconsistency.
- Using Choreographer alone helps but tick delivery offsets vary by device, and buffer-stuffing
  can still occur on long frames. Short frames followed by long ones read as stutter.

## Android: Frame Pacing library (Swappy)
Part of the Android Game Development Kit, for OpenGL and Vulkan games.
- Uses Choreographer (NDK, falling back to Java), presentation timestamps
  (`EGL_ANDROID_presentation_time`, `VK_GOOGLE_display_timing`) so frames are not presented early,
  and sync fences (`EGL_KHR_fence_sync`, `VkFence`) to avoid buffer-stuffing.
- Handles multiple refresh rates. Examples from the guide: on 60 Hz devices 60/30/20 FPS; on
  60 + 90 Hz 90/60/45/30; on 60 + 90 + 120 Hz 120/90/60/45/40/30. It can also save battery by
  setting the refresh rate closest to the target frame rate.
- Modes: auto mode off + pipeline; auto mode on + pipeline; auto mode on + auto pipeline. The
  recommended start is everything off, after Swappy initialisation:
  `swappyAutoSwapInterval(false); swappyAutoPipelineMode(false); swappyEnableStats(false);`
  `swappySwapIntervalNS(1000000000L / yourPreferredFrameRateInHz);`
- Pipeline mode separates CPU and GPU work across VSYNC boundaries; non-pipeline mode gives lower,
  more predictable input-screen latency, and is better when both fit in one swap interval.
- Frame stats are histograms of refreshes waited in the compositor queue, between requested and
  actual present time, between consecutive frames, and between CPU start and present.
- Unity 2019.2 or higher: tick Optimized Frame Pacing under Project Settings > Player > Settings
  for Android > Resolution and Presentation.

## Windows: DXGI flip model
- In the flip model all back buffers are shared with DWM, which composes without a copy, so it is
  generally more efficient than bitblt, mainly in windowed mode. Use bitblt for legacy GDI that
  writes to an HWND directly.
- Create the swap chain with `DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL` (Direct3D 11.1, Windows 8+), with
  `BufferCount` 2 to 16, Format `DXGI_FORMAT_R16G16B16A16_FLOAT`, `B8G8R8A8_UNORM` or
  `R8G8B8A8_UNORM`, and SampleDesc Count 1 / Quality 0 (no MSAA).
- One flip model swap chain per HWND; do not mix with GDI or other APIs on the same HWND; avoid
  GDI `ScrollWindow`/`ScrollWindowEx`.
- Present statistics: `IDXGISwapChain::GetFrameStatistics` fills `DXGI_FRAME_STATISTICS`, valid in
  windowed and full-screen mode for flip model (zeroes for windowed bitblt).
  `GetLastPresentCount` returns the last present ID.
- Glitch recovery per the page: queue `Present1` calls, store each present ID with its expected
  `PresentRefreshCount`, compare with the actual value from `GetFrameStatistics`; if actual is
  later, skip that many frames by passing 0 as `SyncInterval` to the same number of `Present1`
  calls. For large glitches use `DXGI_PRESENT_RESTART` to discard all queued presents.

## Latency: NVIDIA Reflex
Two technologies: Low Latency mode, which synchronises CPU and GPU pipelines for just-in-time
rendering (removes the GPU render queue and reduces CPU back pressure when GPU-bound), and Frame Warp,
which warps the rendered frame to the latest mouse position before scan-out (announced as awaiting
general availability). Latency metrics are broken down by input, simulation, render submission,
driver, render queue and GPU render. Integrate via Streamline, or the Reflex SDK (Windows 10, NVAPI,
C++).

## Verify
- [ ] Frame-time graph (not fps) at the target shows no alternating long and short frames.
- [ ] Input-to-photon latency measured before and after changes.

## Checked

Date 2026-11-08. Pages read in full: Android Frame Pacing library, Microsoft DXGI flip model, NVIDIA Reflex. Confirmed: all claims above. Removed as not on those pages: the "cap at 30 on a 60 Hz display" rule, frame limiter spin and `CREATE_WAITABLE_TIMER_HIGH_RESOLUTION` advice, `DXGI_SWAP_EFFECT_FLIP_DISCARD` and `SetMaximumFrameLatency(1)`, VRR/G-Sync/FreeSync capping, AMD Anti-Lag, Unreal and Unity CVars and API names, PresentMon/CapFrameX and Perfetto tools, and the numeric tolerances (1 ms, 0.2 ms).

Method: docs-only read of cited pages, 2026-11-08
