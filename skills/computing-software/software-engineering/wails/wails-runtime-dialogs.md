---
id: computing-software.software-engineering.wails.wails-runtime-dialogs
name: wails-runtime-dialogs
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, runtime, dialogs, file-dialog]
level: practitioner
status: docs-checked
description: "Show native Wails dialogs from Go: open file, directory and multiple files, save file, and message dialogs with per-platform button and filter behaviour."
sources: [https://wails.io/docs/reference/runtime/dialog]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails runtime dialogs

Goal: prompt the user with native file selectors and message boxes. Go runtime only; the JS runtime does not support dialogs.

## Calls (all take `ctx` first)

- `OpenFileDialog(ctx, OpenDialogOptions) (string, error)`: blank string if cancelled.
- `OpenMultipleFilesDialog(ctx, OpenDialogOptions) ([]string, error)`: nil if cancelled.
- `OpenDirectoryDialog(ctx, OpenDialogOptions) (string, error)`.
- `SaveFileDialog(ctx, SaveDialogOptions) (string, error)`.
- `MessageDialog(ctx, MessageDialogOptions) (string, error)`: returns the text of the selected button.

## Options

`OpenDialogOptions`: `DefaultDirectory`, `DefaultFilename`, `Title`, `Filters []FileFilter`, `ShowHiddenFiles` (Mac, Linux), `CanCreateDirectories` (Mac), `ResolvesAliases` (Mac), `TreatPackagesAsDirectories` (Mac). `SaveDialogOptions` is the same minus `ResolvesAliases`.

`FileFilter{DisplayName, Pattern}`: pattern is a semicolon-separated list, e.g. `"*.jpg;*.png"`. Windows and Linux show each filter as a separate entry. Mac has one pattern set, so with several filters Wails merges all patterns (the docs example becomes `*.png,*.jpg,*.mov,*.mp4`).

`MessageDialogOptions{Type, Title, Message, Buttons, DefaultButton, CancelButton}`; `Type` is `InfoDialog`, `WarningDialog`, `ErrorDialog` or `QuestionDialog`.

## Platform behaviour for message dialogs

- Windows: standard buttons only; returns one of "Ok", "Cancel", "Abort", "Retry", "Ignore", "Yes", "No", "Try Again", "Continue". For Question dialogs the default is "Yes" and cancel is "No"; set `DefaultButton: "No"` to change it.
- Linux: standard buttons only; returns "Ok", "Cancel", "Yes" or "No".
- Mac: up to 4 custom `Buttons`. With no `DefaultButton`/`CancelButton`, the first button is default and bound to return. `DefaultButton` binds return; `CancelButton` binds escape and is shown at the bottom.

```go
selection, err := runtime.MessageDialog(b.ctx, runtime.MessageDialogOptions{
    Title:         "It's your turn!",
    Message:       "Select a number",
    Buttons:       []string{"one", "two", "three", "four"},
    DefaultButton: "two",
    CancelButton:  "three",
})
```

Related: confirm-on-quit in `computing-software.software-engineering.wails.wails-startup-lifecycle-and-single-instance`.

## Checked

2026-11-07. Read the whole Dialog runtime page (website/docs/reference/runtime/dialog.mdx: the five dialog functions and their cancel return values, OpenDialogOptions and SaveDialogOptions field tables with platform columns, MessageDialogOptions table, the Windows, Linux and Mac message-dialog sections, DialogType constants, FileFilter and the per-platform filter sections including the merged Mac pattern example). Screenshots on the page were not viewed. Every claim in the skill matched; no claims were trimmed.

Method: documentation only; no commands were run.
