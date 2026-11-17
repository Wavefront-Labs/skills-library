---
id: computing-software.game-programming.game-engine-architecture.crash-reporting-and-minidumps
name: crash-reporting-and-minidumps
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, crash-reporting, minidumps, crashpad, breakpad, symbol-server, sentry, backtrace, game-programming]
level: advanced
status: draft
description: "Capture and triage game crashes: minidumps via Crashpad/Breakpad or engine reporters, symbol upload per build, logs and context, and grouping by signature."
sources: ["https://chromium.googlesource.com/crashpad/crashpad/+/HEAD/README.md", "https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/nf-minidumpapiset-minidumpwritedump", "https://dev.epicgames.com/documentation/en-us/unreal-engine/crash-reporting-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crash reporting and minidumps

**Goal:** every crash in playtests and live builds arrives as a symbolicated call stack with the
build id, logs and game context, grouped so the top crashes are obvious.

## Capture
- **Crashpad** (or Breakpad): an out-of-process handler writes a minidump (threads, stacks, modules,
  selected memory) and uploads it. Out-of-process is crucial: the crashing process may have a
  corrupted heap. Crashpad is used by Chrome, Sentry Native, Backtrace, BugSplat SDKs.
- Windows-native: `MiniDumpWriteDump` from a separate watchdog process with flags like
  `MiniDumpWithIndirectlyReferencedMemory | MiniDumpWithThreadInfo`; full-memory dumps for internal
  QA only (large).
- Engines: Unreal CrashReportClient (`-crashreports`, data router URL in `DefaultEngine.ini`);
  Unity Cloud Diagnostics / Unity Crash and Exception reporting; Godot writes backtraces, integrate
  Sentry for uploads.
- Also capture: hangs (watchdog thread detects no frame for N seconds and dumps the main thread),
  GPU device-removed/TDR (log DRED/Aftermath breadcrumbs), out-of-memory (log the memory tracker).

## Symbols
Upload PDBs/dSYMs/.debug files for **every build that leaves the build machine** to a symbol server
(Microsoft symstore layout, Sentry/Backtrace symbol upload, `dump_syms` for Breakpad). Embed a build
id / git hash in the binary and report it. Unsymbolicated dumps from a lost build are useless; keep
symbols for the support lifetime.

## Context to attach
Last N KB of the log, build id, platform/GPU/driver, memory stats, current map, game mode, player
position, last console commands, session length. Breadcrumbs (recent events) are often more useful
than the stack.

## Triage
Group by **crash signature** (top non-system frames of the faulting thread, normalised). Rank by
affected users, not raw count. Track crash-free sessions/users percentage per build as a release
gate. New signature in a new build = likely regression; bisect between builds.

## Consoles and mobile
Platform crash services (PlayStation/Xbox/Nintendo crash portals, Google Play Console Android
vitals, App Store Connect/Xcode Organizer) receive dumps; upload symbols to each. Crash rates are
certification and store-ranking metrics.

## Privacy
Disclose crash reporting in the privacy policy; strip personal data (usernames in paths, chat text).

## Verify
- [ ] A deliberate null dereference, a stack overflow, an abort and a hang each produce symbolicated
  reports with logs attached.
- [ ] Symbols for the current release are on the symbol server (automated build step check).
- [ ] Dashboard shows crash-free percentage per build.
