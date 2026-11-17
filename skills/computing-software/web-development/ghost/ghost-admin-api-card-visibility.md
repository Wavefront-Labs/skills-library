---
id: computing-software.web-development.ghost.ghost-admin-api-card-visibility
name: ghost-admin-api-card-visibility
category: computing-software
field: web-development
product: ghost
tags: [ghost, lexical, card-visibility, html-card, call-to-action, members]
level: advanced
status: docs-checked
description: "Control per-card visibility in Ghost Lexical JSON for HTML and Call to Action cards by web and email member segments."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/posts/card-visibility.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show parts of a post to some members only, without breaking it during programmatic edits.

HTML and Call to Action cards support a `visibility` property. Card visibility only applies to cards inside a post the viewer can already access through the post's top-level `visibility`. Typical uses: premium content for paid members, an upgrade prompt for free members, hiding a sponsored block from paid subscribers.

Structure: `visibility` has two sub-objects.
- `web`: `nonMember` (true means everyone including non-members, false means members only) and `memberSegment` (an NQL filter, for example `status:free,status:-free` for all members or `status:-free` for paid only).
- `email`: `memberSegment`, an NQL filter for which members receive the card in email.

With all toggles enabled (the default) the card is visible to everyone everywhere.

Important rule for migrations and find-and-replace scripts: preserve the `visibility` property on cards. Stripping it resets the card to default visibility and can unintentionally make members-only content public.

Card visibility is a Lexical JSON feature: with `source=html` Ghost creates cards itself and visibility settings are not available.

Verify: diff the Lexical JSON before and after your edit and confirm every card that had `visibility` still has identical values.

## Checked

2026-11-04. Confirmed: the visibility structure, nonMember and memberSegment meanings, the default, the preserve-on-migration rule and the source=html limitation (card-visibility page). Removed: nothing; added the source=html limitation the page states.

Method: documentation only; no commands were run.
