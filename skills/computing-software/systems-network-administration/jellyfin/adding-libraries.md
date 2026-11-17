---
id: computing-software.systems-network-administration.jellyfin.adding-libraries
name: adding-libraries
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, libraries, dashboard, content-type, paths, mixed-library]
level: intro
status: docs-checked
description: "Add a library in the Dashboard, choose a content type, add several paths, and avoid the discouraged mixed type."
sources: ["https://jellyfin.org/docs/general/server/libraries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding and configuring libraries

Libraries are virtual collections of media and can contain files from several locations. The first-run wizard offers to add them, and you can add or remove them any time.

**Steps**
1. Log in to the web interface.
2. Click `Admin` > `Dashboard`.
3. In the left menu go to `Server` > `Libraries`.
4. Click "Add Media Library".
5. The server adds the media; a progress bar at the top shows progress.

**Content type.** Movies, shows and music are the most common and have the best client support. You can also add books or photos. A folder with several media types can be labelled mixed, which is a generic folder view. The mixed type is discouraged because metadata results are unreliable; use dedicated library types.

**Paths.** A library can have multiple paths, all shown under the same library. The dialog lets you browse to folders; if you cannot find a location, type the path manually.

Naming rules per type are in `computing-software.systems-network-administration.jellyfin.movie-library-naming`, `computing-software.systems-network-administration.jellyfin.show-library-naming` and `computing-software.systems-network-administration.jellyfin.music-library-organization`.

## Checked

2026-11-03. Confirmed against the Jellyfin Libraries page: Admin > Dashboard > Server > Libraries > Add Media Library steps, content types, mixed type discouraged, multiple paths and manual path entry. Removed: unsupported claim about the mixed movies-and-shows type and the invented check step.

Method: documentation only; no commands were run.
