---
id: computing-software.game-programming.unity.profiling-development-builds-on-device
name: profiling-development-builds-on-device
category: computing-software
field: game-programming
product: unity
tags: [unity, profiler, development-build, autoconnect-profiler, deep-profiling, adb, android, ios, game-programming]
level: practitioner
status: docs-checked
description: "Profile Unity development builds on a target device: Autoconnect Profiler, Attach to Player, iOS and Android remote profiling, adb tunnels and Deep Profiling."
sources: ["https://docs.unity3d.com/2022.3/Documentation/Manual/profiler-profiling-applications.html", "https://docs.unity3d.com/2022.3/Documentation/ScriptReference/Profiling.Profiler.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling development builds on device

**Goal:** measure the real device, not the Editor. Play mode runs in the same process and main thread as the Editor, so
CPU, GPU and memory use cannot be fully isolated from the Editor's, which skews the data. Use Play mode profiling to iterate
quickly after profiling on a device, not as a replacement for it.

## Build settings
- You can only profile an application built as a **Development Build** (Build Settings). Enabling it exposes **Autoconnect
  Profiler** and **Deep Profiling Support**.
- **Autoconnect Profiler**: the Editor bakes its IP address into the Player at build time; the Player tries to connect to the
  Profiler at that address when it starts.
- **Deep Profiling Support**: the built Player starts with Deep Profiling, which profiles every part of the code, not just
  `ProfilerMarker`s. Useful for start-up times; adds a small overhead to the build.

## Connecting
- Manual connection is through the Profiler's **Attach to Player** dropdown and only when Autoconnect Profiler is disabled.
  The target must be visible on the local network or connected by cable, and running a Development Build.
- Select **<Enter IP>** in the dropdown to connect by IP address and optional port. Pick the Player, then click **Record**.
- Enable **Run In Background** in Player Settings (Resolution and Presentation) to keep collecting while the app is in the
  background.
- Mobile: iOS and Android support remote profiling over a network. If you use a firewall, open ports 54998 to 55511 in its
  outbound rules. You can also plug the device in by cable to avoid network issues.
- **iOS**: connect the device to the WiFi network, attach by cable, tick Development Build and Autoconnect Profiler, Build &
  Run, then open the Profiler window (Window > Analysis > Profiler).
- **Android WiFi**: disable mobile data, join the WiFi network, attach by cable, tick Development Build and Autoconnect
  Profiler, Build & Run. The device and the Editor host must be on the same subnet for detection.
- **Android adb**: device in developer mode with USB debugging on, listed in adb devices, Development Build ticked, Build &
  Run, then choose `AndroidProfiler(ADB@127.0.0.1:34999)` in Attach to Player. Build & Run creates the adb tunnel
  automatically; for another application or after restarting the adb server, create it by hand:
  - Editor to Android over USB: `adb forward tcp:34999 localabstract:Unity-{bundle identifier}`
  - Android to Editor over USB: `adb reverse tcp:34998 tcp:34999`
- **Android Deep Profiling** needs the Mono Scripting Backend and starting the game with
  `adb shell am start -n {bundle identifier}/com.unity3d.player.UnityPlayerActivity -e 'unity' '-deepprofiling'`.
- **WebGL**: you cannot attach to a running WebGL player (WebSockets allow no incoming connections in the browser); enable
  Autoconnect Profiler. Draw calls cannot be profiled for WebGL.

## Profiler API
`Profiling.Profiler` has `enabled` (enables the Profiler), `enableBinaryLog` (logs profiling data to a file), `logFile` (the
file to write profiling data to) and `maxUsedMemory` (the maximum memory, in bytes, the Profiler uses for buffering data).

## Best practices (from the manual)
- Add only the Profiler modules for the area under investigation.
- Avoid Deep Profiling because of its high overhead; to see details for markers such as `GC.Alloc` or `JobFence.Complete`
  enable **Call Stacks** in the Profiler toolbar instead.
- Disable **Live** if you do not need the Hierarchy or Timeline view updating during capture.
- F9 enables or disables the Profiler without the window open.
- When profiling in the Editor, maximise the Play mode view and close extra Editor windows; consider the Standalone Profiler.

## Verify
- [ ] The build is a Development Build and the profiler connects to the device, not the Editor.
- [ ] Deep Profiling is used only when Call Stacks cannot answer the question.

## Checked
Date: 2026-11-09. Read: Unity 2022.3 manual "Collecting performance data" (full text) and the Script Reference
Profiling.Profiler class page (property summaries). Removed as not on those pages: the Script Debugging and IL2CPP claims,
UDP multicast discovery, the `Profiler.logFile` usage code and `capture.raw` loading, frame-count and warm-up method, the
`Gfx.WaitForPresentOnGfxThread` interpretation, Profile Analyzer advice, thermal throttling and `Debug.Log` gotchas.
Method: docs-checked 2026-11-09 against the two Unity pages named above.
