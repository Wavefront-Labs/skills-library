---
id: computing-software.game-programming.gameplay-programming.achievements-and-stats-integration
name: achievements-and-stats-integration
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, achievements, platform-stats, steamworks, game-programming]
level: practitioner
status: draft
description: "Integrate achievements and stats across Steam, Xbox and PlayStation: a platform-neutral achievement layer, offline queuing, progress stats and cert rules."
sources: ["https://partner.steamgames.com/doc/features/achievements", "https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/live/features/player-data/achievements/live-achievements-nav"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Achievements and stats platform integration

**Goal:** one gameplay-side API, many platform back-ends, no lost unlocks.

## Gameplay-facing layer
```cpp
enum class Ach : uint16_t { FirstBoss, Collect100Coins, /*...*/ };
struct IAchievementBackend {
    virtual void unlock(Ach) = 0;
    virtual void setProgress(Ach, uint32_t cur, uint32_t max) = 0;
    virtual void setStat(StatId, int32_t) = 0;
    virtual void flush() = 0;
};
```
Gameplay raises *events* ("boss killed") to an achievement tracker; the tracker owns rules and
counters and calls the backend. Map internal ids to platform API names in data per platform.

## Platform specifics
- **Steam:** stats and achievements are defined in the Steamworks partner site. Call
  `SteamUserStats()->SetAchievement("ACH_X")` then `StoreStats()`; progress popups via
  `IndicateAchievementProgress`. Stats are typed (INT, FLOAT, AVGRATE) and validated server-side
  against max change. In recent SDKs current stats load automatically at init.
- **Xbox (GDK):** event-based achievements driven by stats events sent through the Events API, or
  title-managed achievements updated with `XblAchievementsUpdateAchievementAsync` (percentage).
- **PlayStation:** trophies via the trophy pack; unlock calls are asynchronous.

## Robustness
- Persist unlocked/progress state in the save file too and re-send on startup; platform calls fail
  offline and some platforms rate-limit stat writes (batch, flush on checkpoints, not every frame).
- Never unlock from cheat or debug modes in shipping branches; gate the backend on a flag.
- Retroactive unlock: when adding achievements in a patch, evaluate them from save data at load.

## Verify
- Steam: reset with `ResetAllStats(true)` in a dev build and replay a run.
- Pull the network mid-session, unlock, reconnect: unlock arrives.
