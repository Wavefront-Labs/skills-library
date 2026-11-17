---
id: computing-software.software-engineering.wails.wails-window-startup-options
name: wails-window-startup-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, window, options, frameless]
level: practitioner
status: docs-checked
description: "Configure the initial Wails window in options.App: size, min/max, start state, frameless, hidden start, background colour and always-on-top."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails window startup options

Goal: set how the main window first appears by filling `options.App` passed to `wails.Run()`.

## Method

Fields (all on `options.App`):

- `Title` (string): title bar text.
- `Width` (int, default 1024) and `Height` (int, default 768): initial size.
- `DisableResize` (bool): `true` keeps a fixed size; windows are resizable by default.
- `MinWidth`, `MinHeight`, `MaxWidth`, `MaxHeight` (int): if `Width`/`Height` fall outside these limits, the window is set to the limit.
- `WindowStartState` (`options.WindowStartState`): `options.Fullscreen`, `options.Maximised`, `options.Minimised`. Minimised is not supported on Mac; the other two work on Windows, Mac and Linux. `Fullscreen` (the bool field) is deprecated in favour of this.
- `Frameless` (bool): no borders or title bar. See the frameless guide.
- `StartHidden` (bool): window stays hidden until `WindowShow` is called.
- `HideWindowOnClose` (bool): closing the window hides it instead of quitting the app.
- `BackgroundColour` (`*options.RGBA`, default white), e.g. `options.NewRGBA(255,0,0,128)` is red at 50% transparency.
- `AlwaysOnTop` (bool): keep the window above others when it loses focus.

```go
err := wails.Run(&options.App{
    Title:            "Menus Demo",
    Width:            800,
    Height:           600,
    WindowStartState: options.Maximised,
    Frameless:        true,
    MinWidth:         400,
    MinHeight:        400,
    MaxWidth:         1280,
    MaxHeight:        1024,
    StartHidden:      false,
    BackgroundColour: &options.RGBA{R: 0, G: 0, B: 0, A: 255},
    AlwaysOnTop:      false,
})
```

## Dragging a frameless window

`CSSDragProperty` (default `--wails-draggable`) and `CSSDragValue` (default `drag`) tell Wails which elements drag the window: an element whose CSS has that property set to that value acts as the drag handle.

## Related

- Change these at runtime: `computing-software.software-engineering.wails.wails-runtime-window-control`.
- Platform specifics: the windows, mac and linux options skills in this folder.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), including the example block and the Title, Width, Height, DisableResize, WindowStartState (platform table), Frameless, Min/Max, StartHidden, HideWindowOnClose, BackgroundColour, AlwaysOnTop, CSSDragProperty and CSSDragValue sections; no includes. Confirmed Width 1024 / Height 768 defaults, white background default, Minimised unsupported on Mac, Fullscreen deprecated in favour of WindowStartState, the drag property defaults. No claims were trimmed; the `options.Fullscreen` and `options.Minimised` constant spellings are inferred from the table and the `options.Maximised` example, not spelled out on the page.

Method: documentation only; no commands were run.
