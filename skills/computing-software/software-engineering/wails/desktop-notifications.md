---
id: computing-software.software-engineering.wails.desktop-notifications
name: desktop-notifications
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, notifications, runtime, macos, windows, linux]
level: practitioner
status: docs-checked
description: "Send native Wails v2 notifications from Go, including macOS authorization, interactive categories with actions and reply fields, response handling and platform differences."
sources: [https://wails.io/docs/guides/notifications]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native notifications in Wails (Go runtime)

Goal: show system notifications, optionally with buttons or a reply field, and handle the user's response. The page states notifications are not supported in the JS runtime; use Go.

## Setup (call in OnStartup)

```go
err := runtime.InitializeNotifications(a.ctx) // on macOS may fail if bundle identifier is not set
if runtime.IsNotificationAvailable(a.ctx) { /* macOS: checks 10.14+; Windows/Linux: always true */ }
```
macOS only: check and request permission.
```go
ok, err := runtime.CheckNotificationAuthorization(a.ctx)
if !ok { ok, err = runtime.RequestNotificationAuthorization(a.ctx) }
```
Windows and Linux need no authorization.

## Basic notification

```go
err := runtime.SendNotification(a.ctx, runtime.NotificationOptions{
    ID: "calendar-invite-001", Title: "New Calendar Invite",
    Subtitle: "From: Jane Doe", // macOS and Linux only
    Body: "Tap to view the event",
})
```

## Interactive notifications

Register a category first, then send with `CategoryID`. If the category is unknown or `CategoryID` is empty, a basic notification is sent.
```go
category := runtime.NotificationCategory{
    ID: "message-category",
    Actions: []runtime.NotificationAction{
        {ID: "OPEN", Title: "Open"},
        {ID: "ARCHIVE", Title: "Archive", Destructive: true}, // macOS: red button
    },
    HasReplyField: true, ReplyPlaceholder: "Type your reply...", ReplyButtonTitle: "Reply",
}
err := runtime.RegisterNotificationCategory(a.ctx, category)
err = runtime.SendNotificationWithActions(a.ctx, runtime.NotificationOptions{
    ID: "message-001", Title: "New Message", Body: "Free for lunch?", CategoryID: "message-category",
})
```

## Responses and custom data

```go
runtime.OnNotificationResponse(a.ctx, func(result runtime.NotificationResult) {
    if result.Error != nil { return }
    r := result.Response   // r.ID, r.ActionIdentifier, r.UserText (for "TEXT_REPLY"), r.UserInfo
    runtime.EventsEmit(a.ctx, "notification", r)
})
```
`NotificationOptions.Data` (a `map[string]interface{}`) is returned in `response.UserInfo`.

## Cleanup

`RemoveNotificationCategory(ctx, id)`; `RemovePendingNotification`, `RemoveAllPendingNotifications`, `RemoveDeliveredNotification`, `RemoveAllDeliveredNotifications` (macOS and Linux only); `RemoveNotification` (Linux-specific).

## Platform notes

- macOS: permission required, notarization required for distribution; subtitles, text input, destructive actions.
- Windows: toast notifications; text input supported; no subtitles.
- Linux: depends on desktop environment; subtitles supported; no text input.

Verify support with `IsNotificationAvailable` before use and test on each target platform.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Notifications" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
