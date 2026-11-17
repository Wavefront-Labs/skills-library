---
id: computing-software.software-engineering.objective-c.crash-symbolication
name: crash-symbolication
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-debugging, crash-symbolication]
level: advanced
status: draft
description: "Symbolicate crash reports with dSYMs, verify UUIDs, and use atos and Xcode Organizer to map addresses to Objective-C methods."
sources:
  - https://developer.apple.com/documentation/xcode
  - https://lldb.llvm.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crash symbolication
**Goal:** turn addresses into method names.

```bash
dwarfdump --uuid App.app.dSYM                    # UUIDs per arch; must match the crash report's binary image
atos -arch arm64 -o App.app.dSYM/Contents/Resources/DWARF/App -l 0x104a00000 0x104a3c1f4
mdfind "com_apple_xcode_dsym_uuids == <UUID>"    # find a dSYM by UUID
xcrun symbolicatecrash crash.crash App.app.dSYM  # older helper; location varies by Xcode (unconfirmed)
```
- Build with `DEBUG_INFORMATION_FORMAT = dwarf-with-dsym` in Release and archive the dSYMs for every shipped build.
- In `atos`, `-l` is the load address of the image from the crash report's "Binary Images" section; the address is the frame address.
- Xcode Organizer shows crashes with symbolication automatically if dSYMs are in the archive.
- Third-party crash reporters need dSYM uploads in the build phase.
- Objective-C frame names look like `-[ABCCart addItem:]`, `+[ABCCart shared]`.
- Exceptions' backtraces appear in "Last Exception Backtrace".

## Gotchas
- Bitcode-era recompiled dSYMs from App Store Connect differ from local ones (relevant only to older builds).
- Stripped symbols without matching dSYM give `???`.

## Self-check
Symbolicate a crash from a test build and confirm file:line output.
