---
id: computing-software.collaboration-platform-administration.mattermost.in-product-notices
name: in-product-notices
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [in-product-notices, admin-notices, air-gapped, site-configuration]
level: intro
status: docs-checked
description: "Control Mattermost admin and end-user in-product notices, which are on by default and need internet access."
sources: ["https://docs.mattermost.com/administration-guide/manage/in-product-notices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# In-product notices

In-product notices tell users and admins about product improvements, features and releases.

Administrator notices tell system admins when a new server version is available, when external dependencies are being deprecated, or when an upgrade is recommended because support for a version is ending. End user notices tell all users that new desktop app versions and enhancements are available or that Mattermost is collecting feedback to improve the experience.

Both kinds can be disabled in System Console > Site Configuration > Notices.

FAQ points:
- Notices are enabled by default for everyone.
- An air-gapped server will not receive notices, because the server needs an internet connection to fetch them.
- Frequency follows the monthly release cadence, and users only receive notices that apply to them; someone already on the latest desktop app version gets no desktop upgrade notice.

Typical admin decision: leave admin notices on so version and deprecation warnings reach the team that can act on them, and switch off end user notices if they would add noise or conflict with a managed desktop rollout. In an air-gapped deployment there is nothing to disable because nothing arrives, so rely on your own release monitoring instead of in-product notices for upgrade planning.

## Checked

Confirmed against the In-product notices page: admin and end user notice contents, the Notices setting path, default-on, air-gapped behaviour and frequency. The final paragraph is the author's advice, not a documented claim.

Method: docs-checked 2026-11-09 against the full administration-guide/manage/in-product-notices page (source rst from the mattermost/docs repo).
