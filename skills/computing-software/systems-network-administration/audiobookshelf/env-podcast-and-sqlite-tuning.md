---
id: computing-software.systems-network-administration.audiobookshelf.env-podcast-and-sqlite-tuning
name: env-podcast-and-sqlite-tuning
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [environment-variables, podcasts, sqlite, query-logging, pragma, debugging]
level: advanced
status: docs-checked
description: "Use the Other environment variables: NODE_ENV, SOURCE, podcast timeout and failed-check limits, query logging and SQLite pragmas."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/podcast-library/1.podcast-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables from the "Other" table:

| Variable | Default | Meaning |
| --- | --- | --- |
| `SOURCE` | unset | Install source label (e.g. `docker`, `debian`, `rpm`), shown in the web client. |
| `NODE_ENV` | `production` | Keep as `production` unless developing. |
| `PODCAST_DOWNLOAD_TIMEOUT` | 30 seconds | Time to wait for a podcast download to start. |
| `MAX_FAILED_EPISODE_CHECKS` | `24` | Failed episode checks before the RSS feed is disabled. `0` disables the limit. |
| `QUERY_LOGGING` | unset | `log` logs SQL queries; `benchmark` also logs runtime. |
| `QUERY_PROFILING` | unset | Experimental profiling; not implemented on most queries. |
| `SQLITE_MMAP_SIZE` | unset | Sets the SQLite `mmap_size` pragma. |
| `SQLITE_CACHE_SIZE` | unset | Sets the `cache_size` pragma. |
| `SQLITE_TEMP_STORE` | unset | Sets the `temp_store` pragma. |

The 24 default matches the podcast docs: after 24 failed checks in a row the download schedule for that podcast is disabled and must be re-enabled. Set `QUERY_LOGGING=benchmark` temporarily when chasing slow database behaviour, and remove it afterwards.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Environment Configuration page (Other table) and the podcast library structure page (schedule section).

Method: documentation only; no commands were run.
