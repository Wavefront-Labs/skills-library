---
id: computing-software.computer-graphics-engineering.directx.d3d12-query-heaps-and-timestamps
name: d3d12-query-heaps-and-timestamps
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, command-queue, query-heap, resolvequerydata, gettimestampfrequency, gpu-timing-d3d12]
level: practitioner
status: docs-checked
description: "Time GPU passes in D3D12 with timestamp query heaps: EndQuery, ResolveQueryData into a readback buffer, timestamp frequency, copy-queue caveats and stable power state."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/timing", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-resolvequerydata", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-setstablepowerstate", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_query_heap_type"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query heaps and GPU timestamps

## Setup
```cpp
D3D12_QUERY_HEAP_DESC qh = { D3D12_QUERY_HEAP_TYPE_TIMESTAMP, MAX_QUERIES * FRAMES, 0 };
device->CreateQueryHeap(&qh, IID_PPV_ARGS(&queryHeap));
// readback buffer: MAX_QUERIES * FRAMES * sizeof(UINT64), heap type READBACK
UINT64 freq; queue->GetTimestampFrequency(&freq);      // ticks per second (Hz), per queue
```
`GetTimestampFrequency` is per command queue and fails (`E_FAIL`) if the queue does not support timestamps.

## Record
```cpp
UINT base = frameSlot * MAX_QUERIES;
cmd->EndQuery(queryHeap.Get(), D3D12_QUERY_TYPE_TIMESTAMP, base + 0);   // timestamps use EndQuery only
DrawShadows(cmd);
cmd->EndQuery(queryHeap.Get(), D3D12_QUERY_TYPE_TIMESTAMP, base + 1);
DrawGBuffer(cmd);
cmd->EndQuery(queryHeap.Get(), D3D12_QUERY_TYPE_TIMESTAMP, base + 2);
cmd->ResolveQueryData(queryHeap.Get(), D3D12_QUERY_TYPE_TIMESTAMP, base, 3,
                      readback.Get(), base * sizeof(UINT64));
```
`ResolveQueryData` works with all heap types; the destination buffer must be in `COPY_DEST`, and the destination
offset must be a multiple of 8 bytes.

## Read (frames later, after the slot's fence)
```cpp
UINT64* t; D3D12_RANGE r = { base * 8, (base + 3) * 8 };
readback->Map(0, &r, (void**)&t);
double shadowsMs = double(t[base+1] - t[base]) / double(freq) * 1000.0;
D3D12_RANGE none = {0, 0}; readback->Unmap(0, &none);
```
Use floating-point arithmetic for the tick difference, as the timing documentation advises.

## Other query types
| Type | Notes |
|---|---|
| `OCCLUSION` / `BINARY_OCCLUSION` | Begin/EndQuery; binary is the pass/fail form; feeds predication |
| `PIPELINE_STATISTICS` (and `PIPELINE_STATISTICS1` for mesh shader pipelines) | shader invocation and primitive counts |
| `SO_STATISTICS_STREAM0..3` | stream output |
| `VIDEO_DECODE_STATISTICS` | video decode command lists only |

## Calibration and caveats
- Correlate GPU and CPU clocks with `ID3D12CommandQueue::GetClockCalibration`, which samples the GPU timestamp
  counter and `QueryPerformanceCounter` at nearly the same time.
- `device->SetStablePowerState(TRUE)` is a development-time aid that avoids dynamic frequency scaling artifacts. It
  works only in developer mode (otherwise device removal occurs), lowers clocks for the entire system, and must not
  be called in normal execution of a shipped application.
- Copy queue timestamps need `D3D12_FEATURE_DATA_D3D12_OPTIONS3::CopyQueueTimestampQueriesSupported` and query heap
  type `D3D12_QUERY_HEAP_TYPE_COPY_QUEUE_TIMESTAMP`.

## Verify
- [ ] Per-pass timings in an overlay match a profiler capture's trends; no CPU stall when reading.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Timing", `ID3D12Device::SetStablePowerState`,
`ResolveQueryData`, `D3D12_QUERY_TYPE`, `D3D12_QUERY_HEAP_TYPE`, `D3D12_FEATURE_DATA_D3D12_OPTIONS3`
(MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08); the mesh shader spec for `PIPELINE_STATISTICS1`.
Confirmed: per-queue frequency, E_FAIL for unsupported queues, calibration API, floating-point advice, ResolveQueryData
rules, stable power state restrictions, copy queue timestamp cap and heap type, query type names. Corrected:
`SetStablePowerState` outside developer mode causes device removal. Removed the unconfirmed "within ~10%" accuracy
target and the overlapping-work accuracy remark.
Method: documentation only; no commands were run.
