---
id: computing-software.software-engineering.wails.wails-file-drop
name: wails-file-drop
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, drag-and-drop, file-drop, runtime]
level: practitioner
status: docs-checked
description: "Enable Wails file drag and drop with DragAndDrop options, then receive dropped paths via OnFileDrop, wails:file-drop event and CSS drop targets."
sources: [https://wails.io/docs/reference/options, https://wails.io/docs/reference/runtime/draganddrop]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails file drag and drop

Goal: get absolute paths of files or folders dropped on the window.

## Enable

Set `options.App.DragAndDrop`:

```go
DragAndDrop: &options.DragAndDrop{
    EnableFileDrop:     false,   // set true to use the runtime methods
    DisableWebViewDrop: false,
    CSSDropProperty:    "--wails-drop-target",
    CSSDropValue:       "drop",
},
```

- `EnableFileDrop` (default false): must be `true` to use the drop runtime methods. Alternatively listen for the `wails:file-drop` event with `EventsOn` in Go or JS; it carries the drop coordinates and a slice of file paths.
- `DisableWebViewDrop` (default false): disables the webview's own drag and drop, e.g. to stop dragged-in files being opened in the webview when you do not need drops.
- `CSSDropProperty` (default `--wails-drop-target`) and `CSSDropValue` (default `drop`): an element is a valid drop target when it has that property with that value.

## Runtime methods

- Go: `OnFileDrop(ctx context.Context, callback func(x, y int, paths []string))`. The callback gets the in-window coordinates of the release and absolute paths.
- JS: `OnFileDrop(callback: (x, y, paths) => void, useDropTarget: boolean)`. With `useDropTarget` true, it also tracks the mouse and, when it is over an element with the `CSSDropProperty` style, adds the class `wails-drop-target-active` to that element and removes it when the mouse leaves.
- `OnFileDropOff(ctx)` (Go) / `OnFileDropOff()` (JS): removes all registered drag and drop listeners and handlers.

Related: `computing-software.software-engineering.wails.wails-runtime-events`.

## Checked

2026-11-07. Read the whole Drag And Drop runtime page (website/docs/reference/runtime/draganddrop.mdx: OnFileDrop Go and JS signatures, useDropTarget behaviour and the wails-drop-target-active class, OnFileDropOff) and the DragAndDrop section of the Options reference page (website/docs/reference/options.mdx: EnableFileDrop, DisableWebViewDrop, CSSDropProperty, CSSDropValue, the wails:file-drop event). Defaults (false, false, --wails-drop-target, drop) matched. No claims were trimmed.

Method: documentation only; no commands were run.
