---
id: computing-software.systems-network-administration.audiobookshelf.podcast-auto-download-schedule
name: podcast-auto-download-schedule
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [podcasts, auto-download, schedule, max-episodes, retention, rss]
level: advanced
status: docs-checked
description: "Schedule Audiobookshelf podcast checks, understand the slow one-per-check deletion of Max episodes to keep, and the 24-failure disable."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/podcast-library/1.podcast-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Auto download is disabled by default and set per podcast on the **Schedule** tab: how often to check for episodes, and whether to delete the oldest after download.

**Max episodes to keep:** the default keeps all. With a positive number, the server deletes **at most one** local episode per download check, and listen state is ignored, so unlistened episodes can be deleted.

Example: 20 files, limit set to 5, hourly checks. Nothing is deleted until the next check; then one file per hour, so it takes 15 hours to reach the 5 newest.

**After-date downloads:** the **Episodes** tab downloads episodes released after a date. Use a limit of 0 to download all. Set the date in the past to get older episodes.

**Failure disable:** if the RSS feed cannot be reached 24 times in a row, the schedule is disabled and must be enabled again. `MAX_FAILED_EPISODE_CHECKS` changes that count; `0` disables the limit. `PODCAST_DOWNLOAD_TIMEOUT` defaults to 30 seconds.

Deleting an episode file also deletes users' progress for it.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Podcast Library Structure page and Environment Configuration page.

Method: documentation only; no commands were run.
