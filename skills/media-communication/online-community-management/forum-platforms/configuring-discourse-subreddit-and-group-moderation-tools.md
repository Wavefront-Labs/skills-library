---
id: media-communication.online-community-management.forum-platforms.configuring-discourse-subreddit-and-group-moderation-tools
name: configuring-discourse-subreddit-and-group-moderation-tools
category: media-communication
field: online-community-management
product: forum-platforms
tags: [forum-platforms, discourse, trust-levels, watched-words, review-queue, flags, reddit, subreddit, automoderator, automod-yaml, modqueue, removal-reasons, crowd-control, ban-evasion-filter, modmail, facebook-groups, admin-assist, membership-questions, post-approval, circle, community-platform, forum-moderation, online-community-management]
level: practitioner
status: draft
description: "Configure moderation on forum platforms: Discourse trust levels, watched words and the review queue; Reddit AutoModerator, removal reasons and filters; Facebook Groups screening and Admin Assist."
sources: ["Discourse Meta documentation, Reddit Mod Help Center, Meta Groups help (concepts paraphrased; check current settings names)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuring Discourse, subreddit and group moderation tools

**Goal:** use each platform's built-in machinery so that most spam and bad posts are caught
automatically, trusted members carry some of the load, and human moderators handle only the
judgement calls. Settings names drift across versions; treat names below as pointers.

## The common pattern (any platform)
1. **Gate new accounts** — screening questions, approval, or limited abilities until trusted.
2. **Automate the obvious** — word lists, link limits, spam filters.
3. **Let the crowd flag** — and make flags route somewhere monitored.
4. **One queue** — everything flagged or filtered lands in a single review place.
5. **Explain removals** — templated reasons citing the rule.

## Discourse
- **Trust levels (TL0–TL4)** are the core idea: new users (TL0) can't post links/images
  much, or message freely; they gain levels automatically by reading and participating.
  TL3 ("regular") users can recategorise and rename topics and their flags carry more
  weight. Tune the thresholds in Admin › Settings (search "tl1", "tl2" etc.) for your
  community's size; in small communities defaults can be too slow to promote people.
- **Flags:** when enough members flag a post it is hidden automatically pending review.
  Flags and auto-hidden posts land in the **Review** queue.
- **Watched words** (Admin › Customize › Watched Words): lists that **block**, **censor**,
  **require approval** or **flag** posts containing terms; also auto-tag and link
  replacements. Regex is available if enabled.
- **Approval:** require approval for new users' first posts, or for all users in specific
  categories.
- **Category permissions** (see/reply/create per group) and **slow mode** per topic.
- **Silence** (read-only) vs **suspend** (no login) as escalation steps; both logged in staff
  action logs.
- Akismet or similar spam plugins are widely used on self-hosted instances (check what your
  hosting plan supports).

## Reddit (subreddit mod tools)
- **Rules** (up to a limit — 15 when last checked) appear in the sidebar and in report
  reasons; write them so report reasons map 1:1 to rules.
- **AutoModerator**: YAML rules in the subreddit's AutoModerator config page. Typical rules:
  remove/filter posts from accounts younger than N days or below a karma threshold, filter
  link shorteners, require flair, auto-comment reminders. Test changes with `action: filter`
  (sends to modqueue) before `action: remove`. Example:
  ```yaml
  type: submission
  author:
      account_age: "< 3 days"
  action: filter
  action_reason: "New account - manual review"
  ```
- **Modqueue** gathers reports and filtered items; **mod log** records every action;
  **modmail** handles appeals and messages.
- **Removal reasons**: saved templates that message the user with the rule.
- Safety filters such as **Crowd Control** (collapses comments from non-members during
  surges), the **ban evasion** filter, and **harassment/reputation** filters — enable and set
  sensitivity under the Safety settings.
- Reddit's sitewide Content Policy and Moderator Code of Conduct apply over your rules.

## Facebook Groups
- **Membership questions** and rules agreement at join; require answers before approval.
- **Post approval** for all posts, or for new members; **Admin Assist** automates decisions
  (decline posts with links from new members, keyword declines, etc.).
- **Keyword alerts** notify admins; **mute/suspend/remove** members with an audit trail in
  the admin activity log.
- Group roles: admins (full) vs moderators (narrower) — keep at least two admins.

## Circle and similar paid community platforms
Generally simpler: space-level privacy, member approval, reporting and removal. Fewer
automatic filters, so lean on access gating (paid/invite) and clear guidelines. (My hands-on
detail here is thin; check the vendor's current docs.)

## Gotchas
- AutoModerator rules that remove silently — users never learn why; prefer filter + message.
- Discourse thresholds left at defaults in a tiny forum, so nobody ever reaches TL2.
- Report reasons that don't match the rules list.
- Single admin who goes inactive — on Reddit, inactive top mods can block changes.

## Verify
- [ ] New accounts face at least one gate (approval, trust level, account-age filter).
- [ ] Word/link filters run in flag/filter mode first, then tightened.
- [ ] All flags and filtered items land in one monitored queue.
- [ ] Removals send a templated reason citing a rule.
- [ ] At least two people hold the top admin role.
