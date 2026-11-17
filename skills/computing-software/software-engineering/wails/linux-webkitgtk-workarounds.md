---
id: computing-software.software-engineering.wails.linux-webkitgtk-workarounds
name: linux-webkitgtk-workarounds
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, linux, webkitgtk, gstreamer, panic-recovery, signal-handling, video]
level: practitioner
status: docs-checked
description: "Fix Linux-only WebKitGTK issues in Wails apps: video ended event, GStreamer autoaudiosink error, and SA_ONSTACK panic crashes."
sources: [https://wails.io/docs/guides/linux]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: work around three known WebKitGTK problems on Linux.

## Video "ended" event never fires
A WebKitGTK bug. Workaround:

```js
videoTag.addEventListener("timeupdate", (event) => {
  if (event.target.duration - event.target.currentTime < 0.2) {
    let ended = new Event("ended");
    event.target.dispatchEvent(ended);
  }
});
```

## GStreamer error with Audio/Video elements
Symptom message: `GStreamer element autoaudiosink not found. Please install it`. Install gst-plugins-good:

- Arch: `pacman -S gst-plugins-good`
- Debian/Ubuntu: `apt-get install gstreamer1.0-plugins-good`
- Fedora: `dnf install gstreamer1-plugins-good`

If that is not enough more GStreamer packages may be needed (see GStreamer's Linux install docs). The page attributes this to an upstream WebKitGTK issue, says Arch-based systems hit it more often, and says Tauri apps are affected too.

## Crash: non-Go code set up signal handler without SA_ONSTACK flag
Errors: `signal 11 received but handler not on signal stack` / `fatal error: non-Go code set up signal handler without SA_ONSTACK flag`. WebKit installs signal handlers that stop Go converting SIGSEGV (e.g. nil dereference) into a recoverable panic.

Fix: call `runtime.ResetSignalHandlers()` (from `github.com/wailsapp/wails/v2/pkg/runtime`) right before the risky code, in each goroutine that needs recovery:

```go
go func() {
    defer func() {
        if err := recover(); err != nil {
            log.Printf("Recovered from panic: %v", err)
        }
    }()
    runtime.ResetSignalHandlers()
    // code that might panic
}()
```

Rules: call it per goroutine, immediately before the code (WebKit may reset handlers at any time); it is a no-op on other platforms. It adds SA_ONSTACK to the handlers for SIGSEGV, SIGBUS, SIGFPE and SIGABRT.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Linux" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
