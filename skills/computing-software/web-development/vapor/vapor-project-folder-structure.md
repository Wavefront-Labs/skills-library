---
id: computing-software.web-development.vapor.vapor-project-folder-structure
name: vapor-project-folder-structure
category: computing-software
field: web-development
product: vapor
tags: [vapor, folder-structure, project-layout, filemiddleware, public, configure, routes, entrypoint]
level: intro
status: docs-checked
description: "Know what each folder and file in a Vapor template does: Public, Sources/App, configure.swift, entrypoint.swift, routes.swift, Tests."
sources:
  - https://docs.vapor.codes/getting-started/folder-structure/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: find where things belong in a Vapor project (based on SPM layout).

```
.
├── Public
├── Sources/App/{Controllers,Migrations,Models,configure.swift,entrypoint.swift,routes.swift}
├── Tests/AppTests
└── Package.swift
```

- Public: files served by the app only if FileMiddleware is enabled (images, CSS, browser scripts). With it, `localhost:8080/favicon.ico` serves `Public/favicon.ico` if present. Enable in configure.swift:
```swift
let fileMiddleware = FileMiddleware(
    publicDirectory: app.directory.publicDirectory
)
app.middleware.use(fileMiddleware)
```
- Sources/App: the module declared in the SwiftPM manifest; all application logic.
  - Controllers: groups of functions that take a request and return a response.
  - Migrations: Fluent database migrations.
  - Models: your `Content` structs or Fluent `Model`s.
  - configure.swift: holds `configure(_:)`, called by entrypoint.swift to configure the new `Application`; register services like routes, databases and providers here.
  - entrypoint.swift: the `@main` entry point that sets up, configures and runs the app.
  - routes.swift: `routes(_:)`, called near the end of `configure(_:)` to register routes.
- Tests: each non-executable module in Sources can have a matching folder in Tests (XCTest-based). Run with `swift test` or Cmd+U in Xcode. AppTests holds unit tests for the App module.
- Package.swift: the SPM manifest.

## Checked

2026-11-08: read in full the Folder Structure page at docs.vapor.codes/getting-started/folder-structure/ (each folder and file, FileMiddleware snippet, Tests). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
