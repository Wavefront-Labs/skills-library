---
id: computing-software.computer-graphics-engineering.directx.d3d12-info-queue-filtering-and-callbacks
name: d3d12-info-queue-filtering-and-callbacks
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-debugging, id3d12infoqueue, break-on-error, id3d12infoqueue1, debug-message-callback]
level: practitioner
status: docs-checked
description: "Configure the D3D12 info queue: break on corruption/error, filter known-noisy message IDs, and route messages to your logger with ID3D12InfoQueue1 callbacks."
sources: ["https://microsoft.github.io/DirectX-Specs/d3d/MessageCallback.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/nf-d3d12sdklayers-id3d12debug-enabledebuglayer", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12sdklayers/ne-d3d12sdklayers-d3d12_message_id", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/using-d3d12-debug-layer-gpu-based-validation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 info queue

With the debug layer enabled, the device exposes `ID3D12InfoQueue` holding validation messages. Break on
severity, filter, or route them to your logger so they are not lost.

## Break on errors
```cpp
ComPtr<ID3D12InfoQueue> iq;
if (SUCCEEDED(device.As(&iq))) {
    iq->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_CORRUPTION, TRUE);
    iq->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_ERROR, TRUE);
    iq->SetBreakOnSeverity(D3D12_MESSAGE_SEVERITY_WARNING, FALSE);   // TRUE once warnings are clean
}
```
Guard with `IsDebuggerPresent()` to avoid crashing test runs without a debugger.

## Filter known noise
```cpp
D3D12_MESSAGE_ID deny[] = {
    D3D12_MESSAGE_ID_CLEARRENDERTARGETVIEW_MISMATCHINGCLEARVALUE,  // clear colour != optimized clear value
    D3D12_MESSAGE_ID_MAP_INVALID_NULLRANGE,
    D3D12_MESSAGE_ID_UNMAP_INVALID_NULLRANGE,
};
D3D12_INFO_QUEUE_FILTER f = {};
f.DenyList.NumIDs = _countof(deny); f.DenyList.pIDList = deny;
D3D12_MESSAGE_SEVERITY sev[] = { D3D12_MESSAGE_SEVERITY_INFO };
f.DenyList.NumSeverities = 1; f.DenyList.pSeverityList = sev;
iq->PushStorageFilter(&f);
```
Deny only IDs you have understood and decided to accept, with a comment why.

## Route to your logger (ID3D12InfoQueue1)
```cpp
ComPtr<ID3D12InfoQueue1> iq1;
if (SUCCEEDED(device.As(&iq1))) {
    DWORD cookie;
    iq1->RegisterMessageCallback(
        [](D3D12_MESSAGE_CATEGORY cat, D3D12_MESSAGE_SEVERITY sev, D3D12_MESSAGE_ID id,
           LPCSTR desc, void* ctx) { Log(sev, "[D3D12 %d] %s", id, desc); },
        D3D12_MESSAGE_CALLBACK_FLAG_NONE, nullptr, &cookie);
}
```
`ID3D12InfoQueue1` inherits `ID3D12InfoQueue`; the callback runs when a message is produced. With
`D3D12_MESSAGE_CALLBACK_FLAG_NONE` the callback is filtered like the messages logged to the debug output;
`D3D12_MESSAGE_CALLBACK_IGNORE_FILTERS` makes it unfiltered. Do not assume the callback runs on the calling thread
(it can run on internal debug layer threads used for queue virtualization and GPU-based validation), and the
callback must not make any D3D API calls. Unregister with `UnregisterMessageCallback(cookie)`. Without the
callback interface, poll the stored messages with `GetNumStoredMessages` and `GetMessage`.

## Gotchas
- Enable the debug layer before device creation (`D3D12GetDebugInterface` then `EnableDebugLayer`); calling it after
  the device exists makes the runtime remove the device.
- GPU-based validation output is produced after `ExecuteCommandLists` completes on the GPU, so those messages do
  not break at the recording call.
- Keep the debug layer off in shipping builds unless you opt in with a developer switch; Microsoft advises running with
  it enabled most of the time during development.

## Verify
- [ ] A deliberate error (for example a wrong resource state) breaks into the debugger at the API call; logs
  contain D3D12 messages with IDs.

## Checked
Date: 2026-10-26. Documentation: DirectX-Specs "Message callback" spec (2026-10-22), `D3D12_MESSAGE_ID`,
`ID3D12Debug::EnableDebugLayer` (MicrosoftDocs/sdk-api, last commit 2026-10-08) and the GPU-based validation page
(MicrosoftDocs/win32). Confirmed (method names against `d3d12sdklayers.h` in DirectX-Headers): `SetBreakOnSeverity`, `PushStorageFilter`, `GetNumStoredMessages`, `GetMessage`; the three message IDs used; callback registration signature, flags, cookie and
unregister; threading and no-API-calls note; EnableDebugLayer-before-device rule; GBV asynchronous output. Removed
unconfirmed claims: "Windows 11 / Agility SDK" requirement for InfoQueue1, the claim that messages go only to the
debugger by default, DXGI info queue details (`DXGIGetDebugInterface1`, `DXGI_DEBUG_ALL`) and the shipping-build CPU
cost statement.
Method: documentation only; no commands were run.
