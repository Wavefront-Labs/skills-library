---
id: creative-arts.game-design.playtesting-and-balance.rules-versioning-and-change-logs
name: rules-versioning-and-change-logs
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, rules-versioning, change-log, version-control, rulebook, playtest-builds, iteration]
level: practitioner
status: draft
description: "Version your rules and playtest builds: label every build, keep a change log with the reason for each change, and tie feedback to the version tested."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rules versioning and change logs

**Goal:** know which rules every playtest used, why they changed, and how to roll back.

## Procedure
1. **Give every build an ID** such as v0.3.2 or a date-stamped label, printed on cards, boards, rulebook footer and file names. Pick a convention (major for rule overhauls, minor for new content, patch for fixes) and keep to it.
2. **Keep rules in text under version control** (a Git repository or a dated folder) so diffs show exactly what changed; generate printed components from the source.
3. **Write a change log entry per change:** what changed, why (link the playtest finding), expected effect, and what to watch next.
4. **Change few things at once.** Two simultaneous changes make results unreadable.
5. **Record in session notes which build was played,** including house-rules or fixes made at the table.
6. **Tag stable builds** (the version sent to a publisher, a convention demo) so you can return to them.
7. **Publish a short readable change summary** for returning testers.

## Gotchas
- Mixed old and new cards at a table produce phantom bugs; destroy old printouts.
- Silent edits between sessions make comparison meaningless.
- A log that says what changed but not why cannot guide later decisions.

## Verify
- [ ] Every printed component shows the build ID.
- [ ] Each log entry cites the finding that caused it.
- [ ] Old versions are retrievable.
