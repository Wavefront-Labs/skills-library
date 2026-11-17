---
id: computing-software.systems-network-administration.navidrome.navidrome-multi-library-setup
name: navidrome-multi-library-setup
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, multi-library, libraries, library-access, audiobooks, library-id, user-library]
level: practitioner
status: docs-checked
description: "Set up multiple Navidrome libraries (since 0.58): creating libraries in Settings, granting users access, data isolation rules for albums, artists and playlists, and folder layout."
sources: ["https://www.navidrome.org/docs/usage/features/multi-library/", "https://www.navidrome.org/docs/usage/admin/cli/user/", "https://www.navidrome.org/docs/usage/admin/cli/scan/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome multiple libraries

Since v0.58.0 Navidrome supports separate libraries, for example music versus audiobooks, lossy versus lossless, or per family member.

Behaviour:
- On start a default library is created from `MusicFolder` as library 1; existing users get it.
- Admins can access every library. Regular users need explicit access.
- Albums belong to one library. Artists can span libraries and their stats aggregate across them. Playlists can mix libraries the user can access; smart playlists can be scoped (`{"is":{"library_id":2}}`); search is filtered by the user's selected libraries.

Create: sign in as admin, Settings, Libraries, add a Name and Path, optionally make it default for new users, Save. The library scans automatically (watch the Activity panel). Assign users in Settings, Users, Libraries checkboxes. Users with several libraries get a selector at the top left of the UI.

CLI helpers: `navidrome user create --library-ids 1,3`, `navidrome user edit --library-ids 1,2`, `navidrome scan -t 2:Audiobooks`. Library IDs are shown by `navidrome user list`.

Operations: give the Navidrome user read access to every library folder, mount each one in Docker, and budget disk for each library's cache. Each library has its own root folder.

## Checked

2026-11-04. Confirmed against the Navidrome Multi-Library Support page (since v0.58.0, default library, access rules, data isolation, Settings steps, selector, permissions) and the `user` and `scan` CLI pages for the helper commands. Nothing removed.

Method: documentation only; no commands were run.
