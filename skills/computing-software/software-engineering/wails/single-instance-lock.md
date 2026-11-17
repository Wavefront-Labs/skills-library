---
id: computing-software.software-engineering.wails.single-instance-lock
name: single-instance-lock
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, single-instance, runtime, second-instance, options]
level: practitioner
status: docs-checked
description: "Prevent multiple Wails app instances with SingleInstanceLock, handle OnSecondInstanceLaunch, bring the window forward, and treat passed arguments as untrusted."
sources: [https://wails.io/docs/guides/single-instance-lock]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single instance lock

Goal: allow only one running instance and forward the second launch's args (e.g. a file to open) to the first.

## Mechanism per OS

Windows: named mutex derived from your unique id; data goes to the first instance through SendMessage. macOS: named mutex from the id; data via NSDistributedNotificationCenter. Linux: a dbus name from the id; data via dbus.

## Setup

Pass `SingleInstanceLock` in the app options with a `UniqueId` (use a UUID) and an `OnSecondInstanceLaunch` callback receiving `options.SecondInstanceData` (`Args`, `WorkingDirectory`).

```go
SingleInstanceLock: &options.SingleInstanceLock{
    UniqueId:               "e3984e08-28dc-4e3d-b70a-45e961589cdc",
    OnSecondInstanceLaunch: app.onSecondInstanceLaunch,
},
```
```go
func (a *App) onSecondInstanceLaunch(d options.SecondInstanceData) {
    runtime.WindowUnminimise(*wailsContext)
    runtime.Show(*wailsContext)
    go runtime.EventsEmit(*wailsContext, "launchArgs", d.Args)
}
```
Keep the context from `OnStartup` (the example stores a pointer to it in a package variable) so the callback can call runtime methods.

## Gotchas

- The callback does not focus the window; call `runtime.WindowUnminimise` and `runtime.Show` yourself. On Linux, window managers may refuse to raise the window to avoid stealing focus.
- There is no secure protocol between instances. Treat the args and working directory from the callback as untrusted and validate them.

## Checked

2026-11-07. Read the whole Single Instance Lock guide (website/docs/guides/single-instance-lock.mdx): the untrusted-data warning, the per-OS mechanism (named mutex plus SendMessage on Windows, named mutex plus NSDistributedNotificationCenter on macOS, dbus on Linux), the UniqueId/OnSecondInstanceLaunch usage text (SecondInstanceData with command line arguments and working directory), the no-focus note with runtime.WindowUnminimise and runtime.Show, the Linux window-manager caveat and the full main.go example (saved context pointer, launchArgs event). No claims were trimmed; the linked Microsoft, Apple and freedesktop pages were not opened.

Method: documentation only; no commands were run.
