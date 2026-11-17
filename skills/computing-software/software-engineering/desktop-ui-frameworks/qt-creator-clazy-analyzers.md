---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-creator-clazy-analyzers
name: qt-creator-clazy-analyzers
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-creator-clazy-analyzers, qt-creator, qt, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Run Clang-Tidy and Clazy from Qt Creator to analyse a file or project and apply fixits."
sources:
  - https://doc.qt.io/qtcreator/creator-clang-tools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt Creator code analysis with Clazy

**Goal:** catch Qt anti-patterns early.

```text
Analyze > Clang-Tidy or Clazy -> select the files -> Analyze      (whole project)
Tools > C++ > Analyze Current File with Clang-Tidy / Clazy        (current file)
Preferences > Analyzer > Clang Tools                              (global settings; clear Analyze open files to stop auto-analysis)
Projects > Project Settings > Clang Tools                         (per-project checks and suppression list)
```

**Gotcha:** Where a diagnostic has a fixit, tick its checkbox to schedule it; use Disable This Check or Suppress This Diagnostic in the context menu to silence noise.

## Checked
2026-11-03. Confirmed in the Qt Creator page Analyze code with Clang-Tidy and Clazy: menu paths, per-file and per-project analysis, Preferences > Analyzer > Clang Tools, fixits, disable and suppress options. Removed: the named Clazy checks, the qmlls step, the clazy-standalone and compile_commands.json commands and the kit mismatch claim (not in the page).

Method: documentation only; no commands were run.

## Verify
- The Clazy view lists diagnostics for the selected files.
