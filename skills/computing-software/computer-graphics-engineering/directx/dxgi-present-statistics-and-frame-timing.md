---
id: computing-software.computer-graphics-engineering.directx.dxgi-present-statistics-and-frame-timing
name: dxgi-present-statistics-and-frame-timing
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, frame-statistics, getframestatistics, missed-vblank]
level: advanced
status: docs-checked
description: "Measure real display timing in DXGI apps with GetFrameStatistics/GetLastPresentCount, detect missed vblanks and dropped frames, and cross-check with PresentMon."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-getframestatistics", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/ns-dxgi-dxgi_frame_statistics", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-getlastpresentcount", "https://github.com/GameTechDev/PresentMon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Present statistics and frame timing

CPU timestamps around `Present` tell you when you *submitted*, not when the frame *appeared*.
DXGI exposes display-side counters.

## Read statistics
```cpp
DXGI_FRAME_STATISTICS st;
if (SUCCEEDED(swapChain->GetFrameStatistics(&st))) {
    UINT lastPresent; swapChain->GetLastPresentCount(&lastPresent);
    // st.PresentCount: present index that was last displayed
    // st.PresentRefreshCount: vblank count when that present was displayed
    // st.SyncRefreshCount / st.SyncQPCTime: vblank count and QPC time of that vblank
}
```
`GetFrameStatistics` cannot be used for swap chains that use the blt (bitblt) model and draw in windowed mode; it works for
flip-model swap chains or full-screen mode. Treat failures as a reason to reset your tracking.

## Detect missed frames
Keep a ring of (PresentCount you issued -> expected vblank). For consecutive statistics:
- `deltaRefresh = PresentRefreshCount - prevPresentRefreshCount`
- `deltaPresent = PresentCount - prevPresentCount`
If `deltaRefresh > deltaPresent * syncInterval`, frames were displayed late (missed vblank /
judder). `lastPresent - st.PresentCount` = frames queued but not yet shown (latency in frames).

## Pacing loop
Combine with a frame latency waitable object: wait on the waitable before starting CPU work, then
measure display intervals from `SyncQPCTime` deltas. At a fixed 60 Hz refresh a steady interval equal to the
refresh period means good pacing; alternating one and two refresh periods indicates missed deadlines.

## PresentMon for ground truth
```sh
PresentMon.exe --process_name game.exe --output_file pm.csv --v2_metrics   # name your own exe; these flags are in the console README
```
Columns: `MsBetweenPresents` (CPU cadence), `MsBetweenDisplayChange` (what the user sees),
`MsUntilDisplayed` / `DisplayLatency`, `PresentMode` (Independent Flip vs Composed), `AllowsTearing`. Column sets differ between 1.x and 2.x metrics.
Use PresentMon in QA to validate the in-app numbers and to catch composition fallbacks.

## Gotchas
- Statistics are unavailable for windowed blt-model swap chains; check the HRESULT.
- `SyncRefreshCount` and `SyncQPCTime` are based on boot time in full-screen mode and on swap-chain creation time in windowed mode; do not compare them across modes.
- With variable refresh rate, refresh counts are not fixed-interval; use QPC deltas.

## Verify
- [ ] Debug overlay shows display interval histogram and missed-frame counter matching PresentMon within 1 frame.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: DXGI_FRAME_STATISTICS fields (PresentCount, PresentRefreshCount, SyncRefreshCount, SyncQPCTime, SyncGPUTime) and their time bases, GetFrameStatistics availability rule, GetLastPresentCount exists, PresentMon flags (--process_name, --output_file, --v2_metrics) and columns (MsBetweenPresents, MsBetweenDisplayChange, MsUntilDisplayed, DisplayLatency, PresentMode, AllowsTearing, MsPCLatency). The missed-frame arithmetic is the skill author's heuristic, not a documented formula. Removed: the DXGI_ERROR_FRAME_STATISTICS_DISJOINT trigger list and frame-generation product names.
Method: documentation only; no commands were run.
