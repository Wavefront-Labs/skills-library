---
id: computing-software.computer-graphics-engineering.directx.d3d12-dred-device-removed-diagnosis
name: d3d12-dred-device-removed-diagnosis
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, d3d12-debugging, dred, device-removed, dxgi-error-device-hung, auto-breadcrumbs, page-fault, tdr, aftermath]
level: advanced
status: docs-checked
description: "Diagnose Direct3D 12 DEVICE_REMOVED/TDR crashes with DRED auto-breadcrumbs and page-fault data, capture it in the field, and narrow down the faulting command list."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/use-dred", "https://microsoft.github.io/DirectX-Specs/d3d/DeviceRemovedExtendedData.html", "https://learn.microsoft.com/en-us/windows-hardware/drivers/display/tdr-registry-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 DRED: diagnosing device-removed crashes

**Goal:** when the GPU hangs or faults (`DXGI_ERROR_DEVICE_REMOVED`, `DEVICE_HUNG`,
`DEVICE_RESET`), know which command list and operation was executing and which resource
address faulted, including on customer machines.

## 1. Enable before creating the device
```cpp
ComPtr<ID3D12DeviceRemovedExtendedDataSettings1> dred;
if (SUCCEEDED(D3D12GetDebugInterface(IID_PPV_ARGS(&dred)))) {
    dred->SetAutoBreadcrumbsEnablement(D3D12_DRED_ENABLEMENT_FORCED_ON);
    dred->SetPageFaultEnablement(D3D12_DRED_ENABLEMENT_FORCED_ON);
    dred->SetBreadcrumbContextEnablement(D3D12_DRED_ENABLEMENT_FORCED_ON);   // breadcrumb context strings
}
D3D12CreateDevice(adapter, D3D_FEATURE_LEVEL_12_0, IID_PPV_ARGS(&device));
```
DRED settings are global to the process and must be configured before device creation; changes do not affect
devices already created. Auto-breadcrumbs are off by default because they are not free: Microsoft measured a
2-5% performance loss on a typical AAA D3D12 engine. Page-fault tracking is off by default too, because the
runtime must curate a collection of live and recently deleted objects indexed by virtual address (extra system
memory and a small hit on object creation and destruction).

## 2. Detect removal
Check the HRESULT of `Present`, `Signal` and similar calls. On `DXGI_ERROR_DEVICE_REMOVED`/`HUNG`/`RESET`, call
`device->GetDeviceRemovedReason()` and dump DRED:
```cpp
ComPtr<ID3D12DeviceRemovedExtendedData1> d; device.As(&d);
D3D12_DRED_AUTO_BREADCRUMBS_OUTPUT1 bc; d->GetAutoBreadcrumbsOutput1(&bc);
for (auto* n = bc.pHeadAutoBreadcrumbNode; n; n = n->pNext) {
    UINT done = *n->pLastBreadcrumbValue;                // GPU-completed operations in this list
    log(n->pCommandListDebugNameW, n->pCommandQueueDebugNameW, done, n->BreadcrumbCount);
    // operations before index `done` completed; n->pCommandHistory[done] is the first not known to be complete
}
D3D12_DRED_PAGE_FAULT_OUTPUT1 pf; d->GetPageFaultAllocationOutput1(&pf);
log("fault VA 0x%llx", pf.PageFaultVA);   // + pf.pHeadExistingAllocationNode / pHeadRecentFreedAllocationNode
```
`pHeadRecentFreedAllocationNode` lists recently freed objects whose address range matches the faulting VA. A match there
points to a resource released before the GPU finished with it. The breadcrumb ring buffer keeps up to 64 KiB (65536)
operations per command list, so use `(BreadcrumbCount - 1) % 65536` as the last operation index for long lists.

## 3. Make the output readable
- Call `SetName` on every command list and queue and on resources: DRED reports the debug names.
- With breadcrumb context enabled (DRED 1.2), PIX marker and event strings appear in the auto-breadcrumb
  output.
- Upload the dump with your crash report (it is plain structures you format yourself).

## 4. Vendor tools
GPU vendors publish their own crash-analysis tools; consult each vendor's documentation (the NVIDIA Nsight
Aftermath page is listed in `sources`, not read for this check).

## Gotchas
- DRED settings must be applied **before** device creation.
- After removal, recreate the device and every resource, or exit cleanly.
- To get more time under a debugger, the TDR timeout is controlled by the `TdrDelay` registry value (default 2
  seconds); change it on development machines only.
- Run GPU-based validation next if DRED only points to the area, since it reports state and descriptor errors.

## Verify
- [ ] An intentionally faulting test produces a DRED log naming the right command list and operation.
- [ ] Field crash reports include breadcrumbs and page-fault VA.
- [ ] All queues, lists and resources have debug names in the dump.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Use DRED to diagnose GPU faults" (MicrosoftDocs/win32), the
DirectX-Specs Device Removed Extended Data spec (2026-10-22) and Windows driver docs "TDR registry keys".
Confirmed: settings-before-device rule and process scope; defaults off; the 2-5% overhead figure; the 64 KiB
breadcrumb ring buffer and last-op formula; `SetBreadcrumbContextEnablement` on Settings1; structure and field
names (`pLastBreadcrumbValue`, `pCommandHistory`, debug-name fields, `PageFaultVA`, existing and recently-freed
allocation nodes); TdrDelay default. Removed unconfirmed claims: studios shipping breadcrumbs, the root-cause
table (restated only where documented), AMD Radeon GPU Detective, and "raise TdrDelay to reproduce".
Method: documentation only; no commands were run.
