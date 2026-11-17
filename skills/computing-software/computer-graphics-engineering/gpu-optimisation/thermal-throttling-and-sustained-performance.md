---
id: computing-software.computer-graphics-engineering.gpu-optimisation.thermal-throttling-and-sustained-performance
name: thermal-throttling-and-sustained-performance
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, thermal-throttling, sustained-performance, adpf, thermal-headroom, mobile-power]
level: sme
status: draft
description: "Hold frame rate on mobile under heat: measuring sustained performance, Android ADPF thermal headroom APIs, iOS thermal state, adaptive quality, and power budgets."
sources: ["https://developer.android.com/games/optimize/adpf", "https://developer.android.com/reference/android/os/PowerManager#getThermalHeadroom(int)", "https://developer.apple.com/documentation/foundation/processinfo/thermalstate", "https://developer.arm.com/documentation/102643/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thermal throttling and sustained performance

## 1. The problem
Phones and standalone headsets can sustain only ~3-5 W total. A game that hits 60 fps in the first two minutes
heats up, the SoC lowers clocks, and frame rate collapses after 10-20 minutes. Benchmarks from a cold device
lie.

## 2. Measure sustained, not peak
- Run a 30-minute soak on a fixed scene at room temperature, with screen brightness fixed; log fps, frame time,
  CPU/GPU frequency and skin temperature (`adb shell dumpsys thermalservice`).
- Measure energy per frame (Perfetto power rails on Pixel, Snapdragon Profiler, Xcode Energy gauge).
- Target: the frame time budget with headroom (e.g. 60 fps game using <= 70% of GPU time) so clocks can stay low.

## 3. Android ADPF
```kotlin
val pm = getSystemService(PowerManager::class.java)
val headroom = pm.getThermalHeadroom(10)   // forecast seconds; 1.0 = severe throttling threshold
pm.addThermalStatusListener { status -> /* THERMAL_STATUS_MODERATE / SEVERE ... */ }
```
- Poll headroom no more often than about once per second (it returns NaN if called too frequently).
- Performance Hint API (`PerformanceHintManager.createHintSession(tids, targetNs)`, then
  `reportActualWorkDuration`) lets the CPU governor pick the lowest clocks that meet your target.
- Game Mode API: respect the user's battery vs performance mode.

## 4. iOS
`ProcessInfo.processInfo.thermalState` (`.nominal`, `.fair`, `.serious`, `.critical`) plus
`thermalStateDidChangeNotification`; at `.serious` reduce load proactively. Low Power Mode
(`isLowPowerModeEnabled`) also caps frame rate expectations.

## 5. Adaptive response (in order of visual cost)
1. Cap frame rate (60 -> 30, or 90 -> 72 on headsets) with good frame pacing; a stable lower rate beats a
   fluctuating high one.
2. Dynamic resolution scaling.
3. Drop expensive passes (SSAO, bloom resolution, shadow cascade count), LOD bias.
Apply with hysteresis so quality does not oscillate.

## Gotchas
- Rendering faster than display refresh wastes power; always cap to refresh or the target rate.
- Busy-wait loops and spinning threads keep CPU clocks high.
- Charging while testing raises temperature; test both on battery and charging.

## Verify
- [ ] 30-minute soak: fps stays at target (or the chosen cap) with no step drops; thermal status never
  reaches SEVERE on the reference device.
