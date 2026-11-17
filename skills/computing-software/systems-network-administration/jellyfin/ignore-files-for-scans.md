---
id: computing-software.systems-network-administration.jellyfin.ignore-files-for-scans
name: ignore-files-for-scans
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, ignore-file, gitignore, library-scan, exclude, directories]
level: practitioner
status: docs-checked
description: "Exclude directories or specific files from Jellyfin library scans with empty or gitignore-style .ignore files."
sources: ["https://jellyfin.org/docs/general/server/media/excluding-directory/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Excluding files and directories with .ignore

Place `.ignore` files inside library directories to keep items out of scans. Always rescan the library after creating or changing one.

**Exclude a whole directory.** Put an **empty** file named `.ignore` in it. The directory and everything under it is excluded. In the docs' example, `Season 03` and `OST` each contain an empty `.ignore` and are skipped:

```txt
Series (2010)
├── Season 02
├── Season 03
│   └── .ignore
└── OST
    └── .ignore
```

**Exclude specific files or subdirectories.** If `.ignore` is **not empty**, it is read as a list of patterns in the same format as a Git `.gitignore`. For example:

```txt
*.avi
sample.mkv
specials/
```

ignores any file ending in `.avi`, any file named exactly `sample.mkv`, and the `specials` subdirectory with all files below it.

Warning from the docs: Jellyfin 10.11.x and later interpret the contents of `.ignore`; older versions did not look at them. Legacy non-empty `.ignore` files must be manually corrected or they stop working as intended.

## Checked

2026-11-03. Confirmed against the Jellyfin Excluding Files and Directories page: empty .ignore excludes a directory, non-empty uses .gitignore format, 10.11.x change, the example patterns, rescan tip. Removed: invented check step.

Method: documentation only; no commands were run.
