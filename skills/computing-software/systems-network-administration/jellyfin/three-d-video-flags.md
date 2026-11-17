---
id: computing-software.systems-network-administration.jellyfin.three-d-video-flags
name: three-d-video-flags
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, 3d-video, hsbs, fsbs, htab, ftab, mvc, filename-flags]
level: practitioner
status: docs-checked
description: "Mark 3D movies and episodes in file names with the 3D tag plus hsbs, fsbs, htab, ftab or mvc."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# 3D video flags in file names

Jellyfin recognises 3D content from tags in the file name. The first tag is `3D`, followed by a format tag:

| Format | Flag |
| --- | --- |
| half side by side | `hsbs` |
| full side by side | `fsbs` |
| half top and bottom | `htab` |
| full top and bottom | `ftab` |
| Multiview Video Coding | `mvc` |
| Anaglyph | not supported |

Tags are case-insensitive and must be surrounded by a space, hyphen, dot or underscore.

Movie examples:

```txt
Awesome 3D Movie (2022).3D.FTAB.mp4
Awesome 3D Movie (2022)_3D_htab.mp4
Awesome 3D Movie (2022)-3d-hsbs.mp4
```

Show examples follow the episode name, such as `Series Name A (2022) S01E01 Some Episode.3d.ftab.mp4`.

3D flags combine with the grouping used for versions in movie and music video libraries; all text before the hyphen must match the folder name:

```txt
Awesome 3D Movie (2022)
├── Awesome 3D Movie (2022) - 3D_FTAB.mp4
├── Awesome 3D Movie (2022) - 3D.hsbs.mp4
└── Awesome 3D Movie (2022) - 1080p.mp4
```

Verify by opening the item in a client that supports 3D and checking that each file is offered as a separate version with the right format.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: 3D tag plus hsbs, fsbs, htab, ftab, mvc, anaglyph unsupported, case-insensitive and separator rules, movie and show examples, grouping with a hyphen. Page read in full.

Method: documentation only; no commands were run.
