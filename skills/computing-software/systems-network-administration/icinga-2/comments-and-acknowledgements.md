---
id: computing-software.systems-network-administration.icinga-2.comments-and-acknowledgements
name: comments-and-acknowledgements
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, acknowledgement, comment, sticky, expiring-acknowledgement, add-comment, acknowledge-problem]
level: practitioner
status: docs-checked
description: "Add Icinga 2 comments and acknowledge problems via API actions, with sticky and expiring acknowledgements."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# comments and acknowledgements
**Comments** are added at runtime and persist across restarts. They record information for others on repeating incidents and show mainly in web interfaces. Use the API action `add-comment` or an external command.

**Acknowledgements** tell other users you are aware of a persisting problem that already triggered notifications, and suppress further notifications. An acknowledgement also adds a comment holding author and text. Use the API action `acknowledge-problem` or an external command.

**Sticky.** By default the acknowledgement is removed on any state change or recovery. For OK -> WARNING -> CRITICAL -> WARNING -> OK, acknowledging at CRITICAL is lost on the transition to WARNING. Set the `sticky` parameter to keep it until the OK recovery.

**Expiring.** An acknowledged problem may disappear from a "handled problems" dashboard and be forgotten. If you know it should be resolved by a defined time, set an expiration when acknowledging. Icinga 2 clears it when it expires and re-notifies if the problem persists.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Icinga 2 Advanced Topics chapter (about 39k characters): the Comments, Acknowledgements, Sticky and Expiring sections were read; other sections were not. Confirmed: comments persist over restarts and are mainly seen in web interfaces, add-comment and acknowledge-problem API actions or external commands, acknowledgements add a comment with author and text, sticky behaviour with the OK -> WARNING -> CRITICAL example, expiring acknowledgements and re-notification. Removed the remove-acknowledgement and remove-comment sentence, which the page does not mention.
