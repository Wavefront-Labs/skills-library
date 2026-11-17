---
id: media-communication.online-community-management.discord.server-architecture-roles-permissions-and-automod
name: server-architecture-roles-permissions-and-automod
category: media-communication
field: online-community-management
product: discord
tags: [discord, discord-server, server-setup, channels, categories, roles, permissions, permission-overwrites, role-hierarchy, administrator, automod, auto-moderation, verification-level, community-server, onboarding, rules-screening, membership-screening, timeout, slow-mode, audit-log, moderation-bots, carl-bot, dyno, raid-protection, 2fa, online-community-management]
level: practitioner
status: draft
description: "Set up a Discord server that's safe and navigable: category/channel layout, role hierarchy and permission overwrites done right, AutoMod rules, verification, onboarding and moderation tools."
sources: ["Discord Help Center and Discord Moderator Academy (concepts paraphrased; check current UI)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discord: server architecture, roles, permissions and AutoMod

**Goal:** a server new members can navigate in seconds, where permissions don't leak, and
where spam and raids are mostly stopped by configuration before a moderator sees them.
Discord's UI and feature names change often — menu paths below were correct to my knowledge
but verify in the current client.

## 1. Architecture: fewer channels than you think
- Group channels into **categories**: Start here (rules, announcements, welcome), General
  chat, Topic channels, Events/voice, Staff (hidden).
- Start with ~5–10 channels; add more only when one channel is overflowing with a distinct
  topic. Ghost-town channels make a server feel dead.
- Use **forum channels** for Q&A or feedback (threads keep topics findable) and
  **announcement channels** for news members can follow into their own servers.
- Enable the **Community** setting (Server Settings › Enable Community) to unlock rules
  screening, onboarding, insights and announcement channels; it requires a rules channel,
  verification level and explicit-content filter to be set.

## 2. Roles and permission logic
How Discord resolves permissions (worth memorising):
1. Server-level: `@everyone` base permissions + all of the member's roles' permissions
   combined (any role that *allows* grants it).
2. **Administrator** bypasses everything, including channel overwrites. Give it to as few
   people as possible — ideally the owner and one backup; give mods specific permissions
   instead.
3. Channel **overwrites** then apply in order: `@everyone` overwrite, then role overwrites
   (denies, then allows — an allow on any of your roles beats a deny on another), then
   member-specific overwrites, which win.
4. **Hierarchy:** a member can only manage/kick/ban/assign roles *below* their own highest
   role. Bots too — put your moderation bot's role above the roles it must manage.
Practical setup:
- Strip `@everyone` of risky permissions (mention @everyone/@here, manage anything,
  create invites if you want controlled growth, embed links/attach files for brand-new
  members if spam is a problem).
- Roles: Owner/Admin › Moderator › Trial Mod › Bots › Trusted/Regular › Member › (verified)
  @everyone. Cosmetic/pronoun/notification roles at the bottom, with no permissions.
- To hide staff channels: deny View Channel for `@everyone` on the category, allow for
  Moderator; **sync** channel permissions to the category so new channels inherit it.
- Use **View Server as Role** to test what each role sees.

## 3. Safety settings
- **Verification level** (Server Settings › Safety Setup): ranges from none to requiring a
  verified phone. Medium or High (account age / membership time before posting) stops much
  drive-by spam.
- **Require 2FA for moderator actions** — protects against compromised mod accounts.
- **Explicit media content filter** on for all members in most communities.
- Know the **security actions** for raids: pause invites and DMs temporarily.
- **Audit Log** records role changes, bans, channel edits — check it after any incident.

## 4. AutoMod
Built-in AutoMod rules (Server Settings › Safety Setup › AutoMod) include:
- **Custom keyword filters** (with wildcards and allow lists) — block or flag;
- **Commonly flagged words** preset lists;
- **Spam** content detection and **mention spam** limits (e.g. block messages with more
  than N unique mentions — a common raid tactic);
- profile/username filters for members (where available).
Actions: block the message, send an alert to a mod-log channel, and/or time out the member.
Start rules in **alert-only** mode for a week to tune false positives, then switch to block.

## 5. Moderation tools and bots
- Native: **timeout** (up to 28 days), kick, ban (with option to delete recent messages),
  **slow mode** per channel, thread locking.
- Third-party bots (e.g. Carl-bot, Dyno, Wick and others) add logging of edits/deletes,
  reaction roles, warn/strike tracking, and anti-raid. Only add bots you trust, grant
  minimum permissions, and review them periodically — bots with admin are a takeover risk.
- Keep a private **#mod-log** channel and a **#mod-chat** for discussion.

## 6. Onboarding
Use **Onboarding** (Community servers) to ask new members 1–3 questions (interests, region,
experience) that assign roles and show relevant channels; plus **rules screening** so they
must accept rules before posting. Pair with a welcome message pointing to one action
(see media-communication.online-community-management.community-engagement.onboarding-rituals-and-hosting-community-events).

## Gotchas
- Giving mods Administrator "to save time" — and a phished mod nukes the server.
- Bot role sitting below the roles it must assign, so it silently fails.
- Per-channel tweaks drifting out of sync with their category.
- Public invite links posted widely with low verification — an open door for raids.

## Verify
- [ ] Only owner + one backup hold Administrator; 2FA required for mods.
- [ ] "View Server as Role" confirms new members can't see staff channels or ping @everyone.
- [ ] Bot roles are above the roles they manage.
- [ ] AutoMod has keyword, spam and mention-spam rules routed to a mod-log channel.
- [ ] Verification level and raid security actions are known by every mod.
