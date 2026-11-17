---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-async-ui-patterns
name: wpf-async-ui-patterns
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-async-ui-patterns, wpf-threading, wpf, dispatcher, async, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Keep the WPF UI thread free with async/await and Task.Run for blocking work."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/threading-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF async UI patterns

**Goal:** responsive UI during blocking work.

```csharp
async void OnFetchClick(object s, RoutedEventArgs e) {
    Fetch.IsEnabled = false;
    var data = await Task.Run(() => Compute());   // blocking work off the UI thread
    Result.Text = data.ToString();                // resumes on the UI thread
    Fetch.IsEnabled = true;
}
```

**Gotcha:** Do not call blocking methods from event handlers: the application appears to freeze. Await the work so the handler resumes on the UI thread when it completes.

## Verify
- The window stays responsive (animations, resizing) while the work runs.

## Checked

2026-11-03. Confirmed in the WPF threading model page: the "Handle a blocking operation with Task.Run" section (an `async` event handler awaits a `Task.Run`, resumes on the UI thread, and blocking calls from event handlers freeze the app). Removed: CancellationTokenSource and Progress<T> code, and the async void advice, which that page does not cover.

Method: documentation only; no commands were run.
