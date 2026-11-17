---
id: computing-software.software-engineering.wails.wails-mac-options
name: wails-mac-options
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, macos, titlebar, options]
level: practitioner
status: docs-checked
description: "Configure options.App.Mac in Wails: title bar presets, NSAppearance, transparency, webview Preferences, About dialog and file or URL open callbacks."
sources: [https://wails.io/docs/reference/options]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails macOS options

Goal: tune `options.App.Mac` (`*mac.Options`, package `github.com/wailsapp/wails/v2/pkg/options/mac`).

## Title bar

`TitleBar` (`*mac.TitleBar`) has bool fields `TitlebarAppearsTransparent`, `HideTitle`, `HideTitleBar` (removes NSWindowStyleMaskTitled), `FullSizeContent`, `UseToolbar`, `HideToolbarSeparator`. Presets: `mac.TitleBarDefault()`, `mac.TitleBarHidden()`, `mac.TitleBarHiddenInset()`:

```go
Mac: &mac.Options{
    TitleBar: mac.TitleBarHiddenInset(),
}
```

## Appearance and transparency

`Appearance` (`mac.AppearanceType`): `DefaultAppearance`, `NSAppearanceNameAqua`, `NSAppearanceNameDarkAqua`, `NSAppearanceNameVibrantLight`, and the four `NSAppearanceNameAccessibilityHighContrast...` variants (Aqua, DarkAqua, VibrantLight, VibrantDark).

`WebviewIsTransparent` (transparent where CSS alpha is 0) and `WindowIsTranslucent` are usually combined for frosted looks. `ContentProtection` sets the NSWindow sharingType to NSWindowSharingNone so the window is excluded from capture.

## Webview preferences

`Preferences` (`*mac.Preferences`) fields use `mac.Enabled` / `mac.Disabled`: `TabFocusesLinks`, `TextInteractionEnabled`, `FullscreenEnabled`, `EnableAutoplayWithoutUserAction`.

```go
Preferences: &mac.Preferences{
    TabFocusesLinks:                 mac.Enabled,
    TextInteractionEnabled:          mac.Disabled,
    FullscreenEnabled:               mac.Enabled,
    EnableAutoplayWithoutUserAction: mac.Enabled,
},
```

## About box and open callbacks

`About` (`*mac.AboutInfo{Title, Message, Icon []byte}`) adds an About item to the app menu created by the `AppMenu` role (see `computing-software.software-engineering.wails.wails-application-menus`); clicking opens a message box. Embed the icon with `//go:embed build/appicon.png`.

`OnFileOpen func(filePath string)` and `OnUrlOpen func(filePath string)` are called when a file or URL is opened with the app. In the docs overview example they are set inside the `TitleBar` literal; the detail section lists them as `Mac` options.

## Checked

2026-11-07. Read the whole Options reference page (website/docs/reference/options.mdx), including the "Mac" subsection: TitleBar struct table and presets, Appearance table, WebviewIsTransparent, WindowIsTranslucent, ContentProtection, OnFileOpen, OnUrlOpen, Preferences struct and example, About struct and example. No includes. Every field name, preset, appearance value and the NSWindowSharingNone / NSWindowStyleMaskTitled statements matched. No claims were trimmed; the page's overview example places OnFileOpen/OnUrlOpen inside TitleBar while the detail section lists them under Mac, which the skill already notes.

Method: documentation only; no commands were run.
