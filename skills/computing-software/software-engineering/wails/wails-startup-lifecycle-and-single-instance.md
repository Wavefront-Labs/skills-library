---
id: computing-software.software-engineering.wails.wails-startup-lifecycle-and-single-instance
name: wails-startup-lifecycle-and-single-instance
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, lifecycle, single-instance, callbacks]
level: practitioner
status: docs-checked
description: "Hook Wails startup, dom-ready, before-close and shutdown callbacks and enforce a single running instance with SingleInstanceLock."
sources: [https://wails.io/docs/reference/options, https://wails.io/docs/reference/runtime/intro]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails lifecycle callbacks and single instance

Goal: run code at the right moment in the app's life and prevent a second copy from running.

## Callbacks (fields on `options.App`)

- `OnStartup func(ctx context.Context)`: called after the frontend is created but before `index.html` loads. The ctx is the application context you pass to runtime calls.
- `OnDomReady func(ctx context.Context)`: called after the frontend loaded `index.html` and its resources.
- `OnShutdown func(ctx context.Context)`: called after the frontend is destroyed, just before the app terminates.
- `OnBeforeClose func(ctx context.Context) bool`: called when the app is about to quit, from the close button or `runtime.Quit`. Returning `true` prevents the quit (the app continues); `false` continues shutdown. Useful to confirm with the user:

```go
func (b *App) beforeClose(ctx context.Context) (prevent bool) {
    dialog, err := runtime.MessageDialog(ctx, runtime.MessageDialogOptions{
        Type:    runtime.QuestionDialog,
        Title:   "Quit?",
        Message: "Are you sure you want to quit?",
    })
    if err != nil {
        return false
    }
    return dialog != "Yes"
}
```

Runtime caveat from the runtime intro: the ctx is provided to `OnStartup`, but the runtime is not guaranteed to work there because the window initialises on another thread. Call runtime methods at startup from `OnDomReady`.

## Single instance

`SingleInstanceLock` (`*options.SingleInstanceLock`) allows only one running instance:

```go
SingleInstanceLock: &options.SingleInstanceLock{
    UniqueId:               "c9c8fd93-6758-4144-87d1-34bdb0a8bd60",
    OnSecondInstanceLaunch: app.onSecondInstanceLaunch,
},
```

- `UniqueId` (string): used to build the mutex name on Windows and macOS and the dbus name on Linux. Use a UUID so it is unique.
- `OnSecondInstanceLaunch func(secondInstanceData SecondInstanceData)`: called when a second instance of the app is launched.

Related: `computing-software.software-engineering.wails.wails-runtime-dialogs`.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx: OnStartup, OnDomReady, OnShutdown, OnBeforeClose with its example, SingleInstanceLock, UniqueId, OnSecondInstanceLaunch) and the whole runtime intro page (website/docs/reference/runtime/intro.mdx, including the note that runtime methods may not work in OnStartup and should be called from OnDomReady). Trimmed: OnSecondInstanceLaunch "in the running instance", which the page does not say (it says only that the callback runs when a second instance is launched). The mutex (Windows/macOS) and dbus (Linux) UniqueId wording matched.

Method: documentation only; no commands were run.
