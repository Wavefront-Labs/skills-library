---
id: computing-software.collaboration-platform-administration.matrix-synapse.user-directory-search-and-regenerate
name: user-directory-search-and-regenerate
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, user-directory, search-all-users, show-locked-users, prefer-local-users, regenerate-directory, tables]
level: advanced
status: docs-checked
description: "How the Synapse user directory decides who is visible and ranks results, the search_all_users, show_locked_users and prefer_local_users options, and regenerate_directory."
sources:
  - https://element-hq.github.io/synapse/latest/user_directory.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The user directory covers users who are visible to the homeserver: local users, and any users a local user shares a room with. Its tables can drift out of sync, which the docs consider a bug. The current fix is to run the `regenerate_directory` job through the background updates admin API, which flushes and rebuilds the tables as a background task; on a large server this takes a while.

**Data model.** Five tables: `user_directory` (user ID, display name, avatar), `user_directory_search` (full text search data), `user_directory_stream_pos` (set when the initial population finishes, after which Synapse listens for room changes and updates incrementally), `users_in_public_rooms`, and `users_who_share_private_rooms` (triples `(L, M, room id)`, so two local users sharing a room produce two rows). Support users, appservice users and deactivated users are excluded. Because there is one entry per user, it must hold only publicly visible information, or a private-room nickname or avatar would leak.

**Who can be found.** With `search_all_users` false, results are limited to users found in `users_in_public_rooms` or who share a private room with the requester. If true, every known matching user is returned. Locked users are hidden unless `show_locked_users` is true.

**Search terms** are lowercased, NFKC-normalised and split into segments with the ICU segmenter, which uses per-language dictionaries and models.

**Ranking on PostgreSQL.** Exact and prefix `to_tsquery` queries are combined with a weighted score: 4x if a user ID exists, 1.2x each for a display name and an avatar, plus full-text rank contributions (the display name weighs 0.9, localpart and domain 0.1 each), and 2x for local users when `prefer_local_users` is true. SQLite orders by match rank, then local users first if configured, then users with a display name, then those with an avatar.

## Checked

2026-11-04. Confirmed against the Synapse User Directory API Implementation page: visibility, regenerate_directory, five tables and exclusions, search_all_users, show_locked_users, NFKC and ICU segmentation, PostgreSQL weights, SQLite ordering. Removed a closing tip.
Method: documentation only; no commands were run.
