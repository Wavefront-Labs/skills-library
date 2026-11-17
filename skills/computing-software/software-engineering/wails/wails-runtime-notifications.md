---
id: computing-software.software-engineering.wails.wails-runtime-notifications
name: wails-runtime-notifications
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, notifications, javascript]
level: practitioner
status: docs-checked
description: "Send native Wails notifications with actions and reply fields: initialise, authorise on macOS, register categories, handle responses and clean up."
sources: [https://wails.io/docs/reference/runtime/notification]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime notifications

Goal: show system notifications, optionally interactive, from Go or JS (JS names are the same, returning Promises).

## Lifecycle

1. `InitializeNotifications(ctx) error` at app startup.
2. `IsNotificationAvailable(ctx) bool`.
3. macOS only: `CheckNotificationAuthorization` then `RequestNotificationAuthorization` (both return `(bool, error)`; always true on Windows and Linux). Apps must be notarized for distribution on macOS.
4. `CleanupNotifications(ctx)` on shutdown (on Linux it closes the D-Bus connection).

## Sending

```go
err := runtime.SendNotification(ctx, runtime.NotificationOptions{
    ID: "notif-1", Title: "Hello", Body: "This is a notification",
})
```

`NotificationOptions`: `ID`, `Title`, `Subtitle` (macOS and Linux), `Body`, `CategoryID`, `Data`. JS uses lowercase keys (`id`, `categoryId`).

For buttons, register a category then send with `SendNotificationWithActions` (falls back to a basic notification if the category is unknown or `CategoryID` is empty):

```go
runtime.RegisterNotificationCategory(ctx, runtime.NotificationCategory{
    ID: "TASK_CATEGORY",
    Actions: []runtime.NotificationAction{
        {ID: "COMPLETE", Title: "Complete"},
        {ID: "CANCEL", Title: "Cancel", Destructive: true},
    },
})
```

Re-registering an ID overrides it; `RemoveNotificationCategory(ctx, id)` removes one. `NotificationCategory` also has `HasReplyField`, `ReplyPlaceholder`, `ReplyButtonTitle` (Windows and macOS only; Linux has no text input). `Destructive` shows a red button on macOS and is ignored elsewhere.

## Responses

`OnNotificationResponse(ctx, func(result NotificationResult))` is Go only; `result.Error` and `result.Response` (`ID`, `ActionIdentifier`, `CategoryID`, `Title`, `Subtitle`, `Body`, `UserText`, `UserInfo`). Special identifiers: `DEFAULT_ACTION` (clicked the notification body) and `TEXT_REPLY` (submitted reply text). For JS, emit an event from the Go callback (`runtime.EventsEmit(ctx, "notification-response", result.Response)`) and listen with `EventsOn`.

## Removal

`RemoveAllPendingNotifications`, `RemovePendingNotification(ctx, id)`, `RemoveAllDeliveredNotifications`, `RemoveDeliveredNotification(ctx, id)` are macOS and Linux only. `RemoveNotification(ctx, id)` works on Linux only; elsewhere it is a stub returning nil.

Windows has no authorization and no subtitle support; Linux behaviour depends on the desktop environment.

Related: `computing-software.software-engineering.wails.wails-runtime-events`.

## Checked

2026-11-07. Read the whole Notification runtime page (website/docs/reference/runtime/notification.mdx: every function section, NotificationOptions, NotificationCategory, NotificationAction, NotificationResponse and NotificationResult tables, the macOS, Windows and Linux platform sections and the Action Identifiers section). Confirmed the macOS-only authorization calls (always true elsewhere), notarization, the SendNotificationWithActions fallback, category override on re-register, platform limits on subtitle, reply fields and Destructive, the macOS/Linux-only pending and delivered removal calls, the Linux-only RemoveNotification stub, Go-only OnNotificationResponse and DEFAULT_ACTION / TEXT_REPLY. No claims were trimmed.

Method: documentation only; no commands were run.
