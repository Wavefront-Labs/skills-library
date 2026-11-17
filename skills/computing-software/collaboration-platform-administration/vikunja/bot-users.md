---
id: computing-software.collaboration-platform-administration.vikunja.bot-users
name: bot-users
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, bot-users, bot-prefix, bot-api-token, bot-labels]
level: practitioner
status: docs-checked
description: "Create and use Vikunja bot users for automation: restrictions, the bot- prefix, ownership, scoped tokens, project sharing and label behaviour."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/bot-users.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bot users (2.4.0 and later) are accounts for scripts, CI jobs and agents, so machine work is attributed to a labelled account instead of a person's login.

Differences from a normal user:
- No password or email, so no web UI or CalDAV sign-in. It authenticates only with an API token.
- Owned by the human who created it; deleting the owner deletes the bot.
- Username must start with `bot-`; regular signups cannot use that prefix.
- Shown with a distinct avatar and badge.

Otherwise it can be shared into projects, assigned tasks, mentioned and searched.

Create: Settings, Bots (`/user/settings/bots`), name it, then mint API tokens scoped to what the automation needs. Then share each project with the bot as with any user. Flow: create bot, share project, mint scoped token, give the token to the automation.

Labels: an owner and their bots can find and attach each other's labels. A bot edits or deletes only labels it created; the owner can manage all. Labels on a task are visible to everyone who can read it, including link share users, so use bots with different owners if automations need isolated labels.

## Checked

2026-11-04. Confirmed against the Vikunja Bot users page (integrations/bot-users): 2.4.0 availability, no password or email, API-token-only sign-in, owner relationship, reserved bot- prefix, avatar and badge, Settings Bots path, scoped tokens, project sharing and label rules. Nothing removed.

Method: documentation only; no commands were run.
