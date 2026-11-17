---
id: computing-software.collaboration-platform-administration.nextcloud.share-expiration-defaults-and-enforcement
name: share-expiration-defaults-and-enforcement
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [share-expiration, enforce-expiration-date, public-shares, local-shares, sharing-settings]
level: practitioner
status: draft
description: "Set default and enforced expiration dates for Nextcloud local and link shares, and know that users can extend dates and the clock starts from today."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_sharing_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: make shares expire without surprising users.

There are two independent groups of settings in the Sharing section, one for local shares and one for link shares.

Local user and group shares:
- `Set default expiration date for shares` applies a default expiry.
- `Enforce expiration date` always enforces the configured date.

Public shares (link or email):
- `Set default expiration date for shares via link or email` sets a default on public shares.
- `Enforce expiration date` under it always enforces that date for them.

What the docs say about enforcement:
- Users cannot set an expiration date further in the future than the enforced one, but they can set a nearer date.
- Users can update the expiration date again later. The date is based on the current date, not the share creation date, so a user can extend the expiry again whenever the previous date is close to being reached.

So enforcement caps how far ahead a single setting can reach, but it is not an absolute lifetime ceiling for a share that is renewed repeatedly. If your compliance rule needs a hard cap, check whether the user-extension behaviour satisfies it, and consider the retention workflow rules instead.

Excluding groups from link shares (see sharing-policy-admin-settings) removes those groups from the link settings.

Check: create a link share as an ordinary user, confirm the default date is pre-filled, then try a date beyond the limit and confirm it is refused.
