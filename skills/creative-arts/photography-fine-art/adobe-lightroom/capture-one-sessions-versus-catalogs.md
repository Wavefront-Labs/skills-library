---
id: creative-arts.photography-fine-art.adobe-lightroom.capture-one-sessions-versus-catalogs
name: capture-one-sessions-versus-catalogs
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, capture-one-sessions, capture-one-workflow, capture-one-catalog, session-folders, capture-one]
level: practitioner
status: draft
description: "Choose between Capture One sessions and catalogs, set up session folders (Capture, Selects, Output, Trash), and move work between them."
sources: ["https://support.captureone.com/hc/en-us/articles/360003692438-Switching-from-Lightroom-to-Capture-One-FAQ", "https://support.captureone.com/hc/en-us/categories/360000279017-User-guide (Sessions; Catalogs)", "https://support.captureone.com/hc/en-us/articles/360002547957-Tethered-capture"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture One sessions versus catalogs

## Session
- A folder-based project: a `.cosessiondb` file plus folders **Capture**, **Selects**, **Output**, **Trash**. Adjustments live in `CaptureOne/Settings` sidecars beside images.
- Best for one shoot, tethered studio work, client jobs and portable projects (copy the whole session folder to move it).
- Session Favorites and the Library tool browse any folder without importing.
- Special folders: set Capture (tethered destination), Selects (Ctrl/Cmd+J moves selects), Output (default export destination).

## Catalog
- A database (`.cocatalog`) like Lightroom's: images referenced (or stored inside), with Albums, Smart Albums, Groups, Projects, keywords.
- Best for a long-term archive, search across years and large libraries.
- Import dialog: Store Files "Current location" (referenced) or copy to a folder.

## Choosing
| Need | Use |
|---|---|
| Tethered shoot, deliver in days | Session |
| Archive of decades, search and keywords | Catalog |
| Hybrid | Shoot in sessions, import finished sessions into the master catalog (File > Import Session) |

## Gotchas
- Moving image files outside Capture One breaks catalog links (use Locate); sessions are robust because sidecars move with images if you move the whole session folder.
- Catalog/session files upgraded by a newer Capture One version cannot be opened in older versions; back up before upgrading.
- Back up the catalog via File > Backup settings (Preferences > General > Backup).

## Verify
- [ ] After copying a session folder to another drive and opening it, all adjustments and selects remain.
