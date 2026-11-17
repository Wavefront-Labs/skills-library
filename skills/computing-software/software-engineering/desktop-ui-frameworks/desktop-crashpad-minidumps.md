---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-crashpad-minidumps
name: desktop-crashpad-minidumps
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-crashpad-minidumps, desktop-crash-reporting, crash-reporting, minidump, sentry, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Capture native crashes with Crashpad/Breakpad minidumps and upload symbols."
sources:
  - https://docs.sentry.io/platforms/
  - https://chromium.googlesource.com/crashpad/crashpad/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Crashpad and minidump capture

**Goal:** debuggable crashes.

```text
Electron: crashReporter.start({ submitURL: 'https://crash.example.com/upload', uploadToServer: true })
Qt/C++: Sentry Native or Crashpad; keep PDB/dSYM files per release
Tauri/Rust: sentry crate + panic hook, or minidumper for native crashes
Symbolicate: minidump-stackwalk dump.dmp symbols/   or  upload symbols with sentry-cli debug-files upload
```

**Gotcha:** Without matching symbol files for the exact build, dumps show only addresses; archive symbols at release time.

## Verify
- A forced crash arrives on the server with a readable stack.
