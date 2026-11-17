---
id: computing-software.software-engineering.wails.file-association-setup
name: file-association-setup
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, file-association, wails-json, nsis, nfpm, packaging]
level: practitioner
status: docs-checked
description: "Associate file types with a Wails app via wails.json fileAssociations and handle the open event on macOS, Windows and Linux."
sources: [https://wails.io/docs/guides/file-association]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have the OS launch your Wails app when a user opens a given file type.

## wails.json
Under `info`, add `fileAssociations`:

```json
{
  "info": {
    "fileAssociations": [
      { "ext": "wails", "name": "Wails", "description": "Wails Application File",
        "iconName": "wailsFileIcon", "role": "Editor" }
    ]
  }
}
```

- `ext`: extension without the leading period
- `name`: display name
- `iconName`: icon name without extension; icons live in the build folder and proper icons are generated from the .png for macOS and Windows
- `description`: Windows only; shown in Explorer's Type column
- `role`: macOS only; corresponds to CFBundleTypeRole

## macOS
The system launches the app and calls `Mac.OnFileOpen`:

```go
Mac: &mac.Options{
	OnFileOpen: func(filePaths []string) { /* handle paths */ },
},
```

## Windows
Only supported with the NSIS installer, which writes registry entries. Opening a file starts a new instance with the path as a command-line argument: read `os.Args[1:]`. To reuse the running instance, enable the single instance lock:

```go
SingleInstanceLock: &options.SingleInstanceLock{
	UniqueId:               "e3984e08-28dc-4e3d-b70a-45e961589cdc",
	OnSecondInstanceLaunch: app.onSecondInstanceLaunch,
},
```

## Linux
Wails does not bundle for Linux, so associate manually in your package (example uses a .deb built with nfpm):
1. `.desktop` file with `Exec=/usr/bin/wails-open-file %u` and `MimeType=application/x-wails;...`
2. A shared-mime-info XML (`<mime-type type="application/x-wails">` with `<glob pattern="*.wails"/>`)
3. SVG icons for the file types
4. postinstall script: `update-mime-database /usr/share/mime`, `update-desktop-database /usr/share/applications`, `update-icon-caches /usr/share/icons/*`
5. nfpm config mapping the binary, desktop file, mime XML (to `/usr/share/mime/packages/`) and icons (to `hicolor/scalable/...`; the page also copies to the Yaru theme because Ubuntu did not pick up hicolor file icons) and scripts
6. `nfpm pkg --packager deb --target .`

Opening a file starts a new instance with the path as an argument; use the same args or single-instance handling as on Windows.

Related: `computing-software.software-engineering.wails.custom-protocol-schemes`.

## Gaps
The macOS sample on the page has a typo (`println(filestring)`); use your own variable.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "File Association" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
