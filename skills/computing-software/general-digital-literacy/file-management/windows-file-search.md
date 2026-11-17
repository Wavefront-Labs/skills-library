---
id: computing-software.general-digital-literacy.file-management.windows-file-search
name: windows-file-search
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-search, windows-search, search-filters, kind-filter, datemodified, file-explorer-search, everything-search, indexing-options, search-index, search-file-contents, advanced-query-syntax]
level: intro
status: docs-checked
description: "Find files in Windows File Explorer and taskbar search, with query operators, Classic versus Enhanced indexing and what to do when results are missing."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.microsoft.com/en-us/windows/experience/performance-optimization/search-indexing-in-windows
  - https://learn.microsoft.com/en-us/windows/win32/search/-search-3x-advancedquerysyntax
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Windows file search

**Goal:** find the file you saved "somewhere" last month.

## Where to search
- **Taskbar search** shows results for documents across your PC and OneDrive.
- **File Explorer search box:** `Ctrl+E` selects it (`F3` also searches for a file or folder). Start from This PC or your user folder for wide searches.

## Query syntax
Combine terms with `AND`, `OR` and `NOT`; these three words must be uppercase and a space between two terms means AND. Properties use the canonical form `System.Kind:picture`; `NOT` can negate a property, for example `System.Kind:NOT picture`. The full property list is in Microsoft's Advanced Query Syntax reference.

## Indexing
- Settings > Privacy & security > **Searching Windows** has *Find my files*: **Classic** indexes Documents, Pictures, Music and the desktop; **Enhanced** indexes the entire PC. Advanced indexing options lets you add or exclude locations and file types.
- By default file properties and, for text files, contents are indexed; you can choose properties only, which keeps name search but not contents.
- If results are missing, Microsoft's troubleshooting route is Advanced indexing options, then Rebuild.

## Verify
- [ ] A phrase from inside a recent document finds it after switching to Enhanced indexing.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Ctrl+E, F3), "Search indexing in Windows" (Classic and Enhanced, contents indexing) and Microsoft Learn "Advanced Query Syntax" (AND/OR/NOT, System.Kind form). Removed unconfirmed claims: kind:/datemodified:/ext:/size: shorthand table, OneDrive online-only notes, regional date formats, and the third-party Everything tool.
Method: documentation only; no commands were run.
