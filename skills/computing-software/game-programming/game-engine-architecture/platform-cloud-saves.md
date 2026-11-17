---
id: computing-software.game-programming.game-engine-architecture.platform-cloud-saves
name: platform-cloud-saves
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, cloud-save, save-system, platform-integration, game-programming]
level: practitioner
status: draft
description: "Integrate platform cloud saves: Steam Auto-Cloud and remote storage, console save data APIs, conflict resolution, atomic writes and quota limits."
sources: ["https://partner.steamgames.com/doc/features/cloud"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform cloud saves

**Goal:** saves follow the player across devices without corruption or lost progress.

## Steam
- **Auto-Cloud:** configure paths and patterns in Steamworks (root e.g. `WinAppDataLocal`, subdir,
  pattern `*.sav`, quota); Steam syncs before launch and after exit. No code needed; files written
  while running sync on exit.
- **ISteamRemoteStorage:** `FileWrite`, `FileRead`, `FileWriteStreamOpen` for explicit control;
  check `IsCloudEnabledForAccount()` and `IsCloudEnabledForApp()`.
- Steam Deck/Proton: Auto-Cloud path roots must include Linux/Proton mapping.

## Xbox (GDK)
`XGameSaveFiles` (file-based, simplest port) or `XGameSave` containers with blobs; saves sync
through Connected Storage. Writes are transactional per update submission.

## PlayStation / Switch
Platform save data APIs with mount/commit semantics; quotas declared at submission. Switch has
no generic cloud for all titles (Nintendo Switch Online save data cloud, opt-out possible).

## Robust writes everywhere
1. Serialise to memory, add header (magic, version, size, CRC/hash).
2. Write to `save.tmp`, flush, then atomic rename over `save.dat` (or platform commit).
3. Keep the previous save as `save.bak`; on load, fall back if the main file fails validation.

## Conflicts
Two devices played offline: platform shows a conflict dialog (Steam) or the game resolves. Store
metadata (playtime, timestamp, progress summary) in a small header so the game or player can pick.
Never auto-merge progress without rules.

## Pitfalls
- Saving every frame or every few seconds hits quotas and write limits; save on checkpoints.
- Absolute paths or machine-specific data in saves.
- Cert requirements: show saving indicator, don't power off during writes.

## Verify
- Play on PC A, quit, load on PC B; play offline on both and resolve conflict; pull power mid-save
  and recover from backup.
