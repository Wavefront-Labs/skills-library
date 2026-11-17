---
id: computing-software.general-digital-literacy.file-management.finder-tags-and-colour-labels
name: finder-tags-and-colour-labels
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, finder-tags, colour-labels, file-tags]
level: intro
status: docs-checked
description: "Tag files with colours and words in macOS Finder, find them from the sidebar or search, and set favourite tags and keyboard shortcuts."
sources:
  - https://support.apple.com/guide/mac-help/tag-files-and-folders-mchlp15236/mac
  - https://support.apple.com/guide/mac-help/change-finder-settings-on-mac-mchlp2803/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finder tags and colour labels

## macOS Finder
- Select an item, open the File menu (or Control-click) and choose a colour above **Tags**, or click **Tags** to pick or enter a tag. In a Finder window you can also use the tag button in the toolbar. When saving a document, use the Tags field in the Save dialog.
- Keyboard: `Control+1` to `Control+7` adds or removes your favourite tags; `Control+0` removes all tags.
- Find tagged items: click the tag in the Finder sidebar, or type the tag colour or name in the search field and choose the tag from the suggestions. Group by a tag from the toolbar group button; sort by Tags via View > Show View Options.
- Finder > Settings > **Tags**: choose which tags appear in the sidebar, change colours and names, create or delete tags. **Favourite Tags** sets the (up to seven) tags in the Control-click menu.
- Remove tags from a file via Edit Tags then Delete.
- Tags work with files stored on the Mac or in iCloud.

## Gotchas
- Tags are metadata, not folders: removing a tag does not delete files.
- For cross-platform sharing, put the label in the file name or folder instead.

## Verify
- [ ] Clicking the tag in the sidebar lists every file you tagged.

## Checked
Date: 2026-10-27. Documentation: Apple Mac User Guide "Use tags to organise files on Mac" and "Change Finder settings on Mac" (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: tag: search syntax, tags lost on FAT/exFAT or email, the 5-7 tag rule, and the Windows ratings and tags section.
Method: documentation only; no commands were run.
