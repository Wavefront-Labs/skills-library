---
id: computing-software.computer-graphics-engineering.directx.d3d12-device-removed-recovery-and-tdr
name: d3d12-device-removed-recovery-and-tdr
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-debugging, device-removed-recovery, tdr, getdeviceremovedreason]
level: advanced
status: docs-checked
description: "Detect D3D12 device removal (DXGI_ERROR_DEVICE_REMOVED/RESET/HUNG), interpret GetDeviceRemovedReason, recover by recreating the device, and respect TDR limits."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-getdeviceremovedreason", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12fence-getcompletedvalue", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-error", "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery", "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/tdr-registry-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device removed recovery and TDR

## Detect
Removal surfaces as a failing HRESULT from calls such as `Present`, and as fence values reading `UINT64_MAX`.
```cpp
HRESULT hr = swapChain->Present(syncInterval, flags);
if (hr == DXGI_ERROR_DEVICE_REMOVED || hr == DXGI_ERROR_DEVICE_RESET) {
    HRESULT reason = device->GetDeviceRemovedReason();
    LogRemoval(reason);         // + DRED data, last markers, driver version
    RecreateDevice();
}
```
For asynchronous notification, the `GetDeviceRemovedReason` documentation suggests
`fence->SetEventOnCompletion(UINT64_MAX, hEvent)`: device removal signals all fences to that value, which also
completes every wait on smaller values.

| Reason | Documented meaning |
|---|---|
| `DXGI_ERROR_DEVICE_HUNG` | the device failed due to badly formed commands sent by the application; a design-time issue to investigate and fix |
| `DXGI_ERROR_DEVICE_REMOVED` | the video card was physically removed, or a driver upgrade occurred; destroy and recreate the device |
| `DXGI_ERROR_DEVICE_RESET` | the device failed due to a badly formed command; a run-time issue; destroy and recreate the device |
| `DXGI_ERROR_DRIVER_INTERNAL_ERROR` | the driver hit a problem and put the device into the removed state |
| `DXGI_ERROR_INVALID_CALL` | the application passed invalid parameter data; must be debugged and fixed |

## Recovery
1. Destroy the old device and every object created from it (resources, heaps, PSOs, swap chain, queues,
   fences), then create a new device.
2. Create the queues and swap chain again and reload GPU resources from CPU copies or disk.
3. If removal repeats within minutes, tell the user and offer reduced settings.

## TDR
Windows detects a GPU task that exceeds the TDR timeout. The default `TdrDelay` is 2 seconds, and the
documentation says graphics operations should take no more than two seconds in end-user scenarios. After the
reset the OS purges all video memory allocations. By default the OS bug-checks on the sixth GPU hang when five
or more hangs and recoveries happen within one minute.
- Split long compute work (offline bakes, path tracing) into chunks that finish well under the timeout.
- Do not ask users to change `TdrDelay`; changing it is a developer-machine choice.

## Gotchas
- After removal `GetCompletedValue` returns `UINT64_MAX`; loops that wait for "completed >= x" end immediately,
  so check for removal separately.
- Read DRED data (see `d3d12-dred-device-removed-diagnosis`) before tearing the device down.

## Verify
- [ ] A forced hang (an intentionally over-long dispatch on a test machine) triggers recovery: the app continues
  with a recreated device and no leaked references (check with live-object reporting).

## Checked
Date: 2026-10-26. Documentation: `ID3D12Device::GetDeviceRemovedReason`, `ID3D12Fence::GetCompletedValue`
(MicrosoftDocs/sdk-api), DXGI return codes page (MicrosoftDocs/win32), and Windows driver docs "Timeout Detection
and Recovery" and "TDR registry keys" (MicrosoftDocs/windows-driver-docs). Repositories current as of October
2026. Confirmed: UINT64_MAX fence behaviour and the SetEventOnCompletion notification trick; meanings of the
five DXGI error codes; 2 second default; five hangs in one minute bug-check rule; video memory purge.
Removed unconfirmed claims: `E_OUTOFMEMORY` as a removal reason, "debug layer triggers removals with GBV",
"a hang in one queue resets all apps' contexts", `Map` behaviour after removal, `dxcap -forcetdr`, and use-after-free
attributions for driver errors.
Method: documentation only; no commands were run.
