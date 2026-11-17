---
id: creative-arts.game-design.game-mastering.foundry-vtt-campaign-setup
name: foundry-vtt-campaign-setup
category: creative-arts
field: game-design
product: game-mastering
tags: [game-design, game-mastering, foundry-vtt, virtual-tabletop, online-play, game-system, scenes, walls, dynamic-lighting, modules, hosting]
level: practitioner
status: draft
description: "Set up a campaign on Foundry Virtual Tabletop: hosting choice, game system and world creation, scenes with walls and lighting, actors and journals, modules and backups."
sources:
  - https://foundryvtt.com/kb/
  - https://foundryvtt.com/article/installation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foundry VTT campaign setup

**Goal:** a reliable online table on Foundry Virtual Tabletop, prepared so sessions start
on time and maps, tokens and handouts work.

Foundry VTT is a self-hosted virtual tabletop (one-time licence for the GM; players join
free through a browser). Its Knowledge Base documents installation, worlds, scenes,
walls, lighting and modules.

## Hosting options
| Option | Notes |
|---|---|
| Host on your PC | simplest; you must forward a port (default 30000) or use a tunnel; your machine must be on during sessions |
| Dedicated server / VPS | always-on; Node.js install per Foundry's docs |
| Partner hosting services | managed hosting for a fee |

## Setup procedure
1. **Install** Foundry (licence key), create a **world** with a **game system** (e.g.
   the D&D 5e system, Pathfinder 2e system, or another community system).
2. **Scenes:** import map images; set grid size to match the map; draw **walls** and
   doors for line of sight; set **lighting** and token vision if using dynamic lighting.
3. **Actors:** create PCs (players own their actors) and NPCs; configure token vision
   and disposition.
4. **Journals** for handouts and notes; show to players when needed.
5. **Compendiums** for reusable content; **playlists** for ambience.
6. **Modules:** add sparingly; each module is a potential update conflict.
7. **User permissions:** player accounts, ownership of actors, what players can see.
8. **Backups:** copy the user data folder (worlds, systems, modules) regularly and before
   updates.

## Session-day checklist
- Update Foundry/system/modules days before, not hours before.
- Test a player connection (invite link from Game Settings -> Invitation Links).
- Preload the first scene.

## Gotchas
- Major Foundry version updates can break modules; wait for module compatibility before
  updating.
- Large map images slow loading; compress (WebP) and size sensibly.
- Players behind strict networks may fail to connect to self-hosted servers; test early.

## Verify
- [ ] World created with the correct game system.
- [ ] First scenes have walls, grid and lighting configured.
- [ ] Player connection tested remotely.
- [ ] Backup taken and restore tested once.
