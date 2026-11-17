---
id: computing-software.systems-network-administration.jellyfin.parental-controls-and-access-schedule
name: parental-controls-and-access-schedule
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, parental-control, content-rating, tags, access-schedule, restrictions]
level: practitioner
status: docs-checked
description: "Hide content by maximum rating, unrated items or tags and limit login hours with Jellyfin's parental control tab."
sources: ["https://jellyfin.org/docs/general/server/users/adding-managing-users/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parental control and access schedules

The `Parental Control` tab of a user restricts what they see and when. Content matching a restriction is hidden; the time window effectively disables the user.

- **Maximum allowed parental rating:** the highest rating allowed to show up for this user.
- **Block items with no or unrecognized rating information:** always hides items lacking usable ratings.
- **Block items with tags:** always hides items containing the given tags. You add tags to items by editing their metadata.
- **Allow items with tags:** shows only items containing the given tags.
- **Access Schedule:** the timeframes when the user may log in. Media can only play within them and is stopped past the end.

The Dashboard splash screen image is a separate setting (see `computing-software.systems-network-administration.jellyfin.general-server-settings`).

Changes on any tab need `Save`.

## Checked

2026-11-03. Confirmed against the Jellyfin Managing Users page, Parental Control section: maximum rating, block unrated, block/allow tags, access schedule. Removed: unsupported advice on ratings and tagging schemes, an unsupported splash-screen claim and the invented check step.

Method: documentation only; no commands were run.
