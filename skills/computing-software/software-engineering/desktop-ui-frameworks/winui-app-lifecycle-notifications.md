---
id: computing-software.software-engineering.desktop-ui-frameworks.winui-app-lifecycle-notifications
name: winui-app-lifecycle-notifications
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [winui-app-lifecycle-notifications, winui-windows-app-sdk, winui3, windows-app-sdk, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use AppInstance single-instancing and AppNotificationManager app notifications in a WinUI 3 app."
sources:
  - https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/applifecycle/applifecycle-single-instance
  - https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/migrate-to-windows-app-sdk/guides/toast-notifications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows App SDK lifecycle and notifications

**Goal:** single instance app with app notifications.

```csharp
var args = AppInstance.GetCurrent().GetActivatedEventArgs();
var main = AppInstance.FindOrRegisterForKey("MySingleInstanceApp");
if (!main.IsCurrent) { await main.RedirectActivationToAsync(args); return; }

AppNotificationManager.Default.NotificationInvoked += (s, a) => { /* dispatch to the UI thread, then handle */ };
AppNotificationManager.Default.Register();
var n = new AppNotificationBuilder().AddText("Export finished").BuildNotification();
AppNotificationManager.Default.Show(n);
```

**Gotcha:** Register the `NotificationInvoked` handler before calling `Register()`, otherwise a click can start a new process. Dispatch to the App or Window dispatcher before touching UI from the handler.

## Verify
- A second launch redirects to the first and a notification click activates the app.

## Checked

2026-11-03. Confirmed in the single-instance WinUI how-to (`AppInstance.GetCurrent().GetActivatedEventArgs`, `FindOrRegisterForKey`, `IsCurrent`, `RedirectActivationToAsync`) and the Windows App SDK toast notifications guide (`AppNotificationManager.NotificationInvoked`, `Register` after the handler, `AppNotificationBuilder().AddText`, `Show(BuildNotification())`, dispatching to the UI). Removed: the unpackaged AUMID claim marked "confirm", which those pages do not settle.

Method: documentation only; no commands were run.
