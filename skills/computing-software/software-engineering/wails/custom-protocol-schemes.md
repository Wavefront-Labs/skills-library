---
id: computing-software.software-engineering.wails.custom-protocol-schemes
name: custom-protocol-schemes
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, protocol, url-scheme, deep-link, wails-json, nsis]
level: practitioner
status: docs-checked
description: "Register a custom URL scheme such as myapp:// for a Wails app and handle opened links on macOS, Windows and Linux."
sources: [https://wails.io/docs/guides/custom-protocol-schemes]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: launch your Wails app from links using a custom protocol, e.g. to connect it to a web app.

## wails.json
```json
{
  "info": {
    "protocols": [
      { "scheme": "myapp", "description": "My App Protocol", "role": "Editor" }
    ]
  }
}
```

`scheme` is the protocol name; `description` is Windows only; `role` is macOS only (CFBundleTypeRole).

## macOS
The system launches the app and calls `Mac.OnUrlOpen`:

```go
Mac: &mac.Options{
	OnUrlOpen: func(url string) { println(url) },
},
```

For universal links, follow Apple's guide (entitlements, Info.plist keys, `apple-app-site-association` on your site). Info.plist gets `NSUserActivityTypes` containing `NSUserActivityTypeBrowsingWeb`; entitlements.plist gets `com.apple.developer.associated-domains` with `applinks:myawesomeapp.com`.

## Windows
Only supported with the NSIS installer, which creates the registry entry. Opening a URL starts a new instance with the URL as an argument; read `os.Args[1:]`. To pass it to a running instance instead, use `SingleInstanceLock` with `UniqueId` and `OnSecondInstanceLaunch`.

## Linux
No Wails bundling for Linux. In a .deb (built with nfpm) ship a `.desktop` file whose `Exec` ends in `%u` (important) and has `MimeType=x-scheme-handler/myapp;`. Add a postinstall script running `update-desktop-database /usr/share/applications`, point nfpm `contents` and `scripts` at the files, build with `nfpm pkg --packager deb --target .`. The URL arrives as an argument (`os.Args[1:]`), or via single instance lock.

Related: `computing-software.software-engineering.wails.file-association-setup`.

## Gaps
Step 7 on the page says "file path" for the Linux argument; it is the URL.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Custom Protocol Scheme association" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
