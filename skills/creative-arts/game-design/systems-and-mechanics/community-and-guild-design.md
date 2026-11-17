---
id: creative-arts.game-design.systems-and-mechanics.community-and-guild-design
name: community-and-guild-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, community-design, guild-design, social-systems, online-communities, player-retention]
level: practitioner
status: draft
description: "Design community structures (guilds, clans, social hubs, moderation) that let players form groups, contribute and stay, following Schell's community lenses."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://mud.co.uk/richard/hcds.htm
  - https://www.amazon.com/Community-Building-Web-Strategies-Successful/dp/0201874849
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Community and guild design

**Goal:** players who find each other, form lasting groups and feel ownership, without
the game becoming a harassment vector.

Schell's communities chapter lists the drivers: a strong shared conflict that gives a
reason to group, room for self-expression, support for three levels of experience
(newcomer, regular, elder), regular community events, and interdependence. Amy Jo Kim's
*Community Building on the Web* adds purpose, places, profiles, roles, leadership,
etiquette, events and rituals.

## Steps
1. **State why groups exist:** content that needs N people (raids), shared goals
   (guild projects), or territory. No mechanical reason means no guilds.
2. **Define group primitives:** membership cap, ranks and permissions (invite, kick,
   bank access), shared storage, group chat, identity (name, tag, emblem).
3. **Create places:** social hubs where players idle and are seen; persistent spaces
   (guild hall) raise attachment.
4. **Interdependence:** roles that need each other (tank/healer/damage, crafter/gatherer).
5. **Elder path:** let veterans mentor (mentor rewards, recruitment tools) so the
   community renews itself.
6. **Rituals and events:** weekly resets, seasonal events, guild leaderboards.
7. **Moderation tooling:** report, block, mute, guild-leader tools, a clear code of conduct.

## Gotchas
- Guild-only rewards with steep entry make solo players feel locked out; offer
  pick-up-group paths.
- Leader burnout collapses guilds; allow leadership transfer and inactive-leader succession.
- Shared banks without per-rank limits get looted; log every withdrawal.
- Large caps flatten belonging; small subgroups (squads, parties) help.

## Verify
- [ ] Mechanical reason for groups written down.
- [ ] Rank/permission table and audit log.
- [ ] Newcomer, regular and elder each have a goal.
- [ ] Report/block/mute and leader-transfer flows exist.
