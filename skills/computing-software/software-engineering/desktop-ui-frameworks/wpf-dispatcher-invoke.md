---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-dispatcher-invoke
name: wpf-dispatcher-invoke
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-dispatcher-invoke, wpf-threading, wpf, dispatcher, async, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Update WPF UI from background threads with Dispatcher.InvokeAsync, Invoke and Task.Run."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF Dispatcher.Invoke and InvokeAsync

**Goal:** no cross-thread exceptions.

```csharp
await Task.Run(() => Compute());     // heavy work off the UI thread
Status = "done";                     // the awaiting handler resumes on the UI thread
// from another thread: queue work on the UI thread's Dispatcher
Application.Current.Dispatcher.InvokeAsync(() => Status = "tick", DispatcherPriority.Background);
```

**Gotcha:** WPF objects derive from `DispatcherObject` and are tied to the thread that created them. `Dispatcher.Invoke` is the synchronous call and `InvokeAsync` the asynchronous one; prefer `InvokeAsync` unless the caller must wait.

## Verify
- No InvalidOperationException about thread ownership while updating the UI from a worker.

## Checked

2026-11-03. Confirmed in the WPF threading model page: DispatcherObject thread association, `Dispatcher.InvokeAsync` (asynchronous) and `Dispatcher.Invoke` (synchronous), DispatcherPriority use, and the Task.Run example. Removed: BeginInvoke and CheckAccess usage and the deadlock claim, which that page does not state.

Method: documentation only; no commands were run.
