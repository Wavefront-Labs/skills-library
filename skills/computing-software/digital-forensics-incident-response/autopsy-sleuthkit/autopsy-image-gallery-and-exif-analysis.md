---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.autopsy-image-gallery-and-exif-analysis
name: autopsy-image-gallery-and-exif-analysis
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [image-gallery, exif, autopsy, picture-analyzer, media-review, dfir]
level: practitioner
status: docs-checked
description: "Review pictures in Autopsy: Image Gallery grouping, categories and tagging, hash-hit triage, the Picture Analyzer module and EXIF cross-checking."
sources: ["https://sleuthkit.org/autopsy/docs/user-docs/4.21.0/image_gallery_page.html", "https://exiftool.org/TagNames/EXIF.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Autopsy Image Gallery and EXIF analysis

Picture review matters in insider leaks, fraud, harassment and child-exploitation cases (the
last handled under law-enforcement procedures only). The Image Gallery was designed with
child-exploitation cases in mind but works for any case involving images and videos.

## Ingest setup
Per the user guide: enable the Hash Lookup module with the NSRL and known-bad hash sets, the
Picture Analyzer module and the File Type module. Image Gallery can collect data as ingest runs
or all at once after ingest (Tools > Options > Image /Video Gallery); the setting is saved per
case and cannot be changed during ingest.

## Image Gallery
Open it with the "View Images/Videos" button or Tools > View Images/Videos (new window).
- Groups are presented as background ingest analyses them, and the default grouping is by
  folder; you must keep it grouped by folder while ingest is still running.
- The next group shown follows a sort criterion; the default is density of hash set hits.
  You can also sort by group size to see which folders hold the most images.
- Hash-set hit images have a dashed border. Hits are not tagged or categorized automatically;
  after ingest, group by hash sets and categorize a whole group from its header.
- Each image has one category and any number of tags. Categories are hard coded to the Project
  Vic names: CAT-0 Uncategorized, CAT-1 Child Abuse Material, CAT-2 Child Exploitative / Age
  Difficult, CAT-3 CGI / Animation, CAT-4 Comparison Images, CAT-5 Non-pertinent. A built-in
  "Follow Up" tag also exists.
- Shortcuts: digits 0-5 assign a category to the selected files; alt + 0-5 to the whole focused
  group. Double-click opens slide show mode.
- Standard Autopsy report generation produces a report of every tagged or categorized file.
- Multi-user cases: results from ingest run on another cluster node may not appear until you
  close and reopen Image Gallery, which may ask you to rebuild its database. You can turn off
  its listening for database changes if it hurts performance.

## EXIF review
Picture Analyzer extracts EXIF metadata and creates events for image timestamps. Useful EXIF
tags are documented on the ExifTool EXIF tag page (for example DateTimeOriginal, Make, Model,
Software). Cross-check key images with a second tool such as ExifTool before relying on a
value.

## Interpreting
- EXIF times come from the camera clock; compare with file system times and known-time events
  to estimate any offset.
- EXIF is easily edited; treat it as supporting evidence and corroborate it.

## Verify
Key images in the report show EXIF from two tools with matching values, and any camera-clock
offsets are documented.

## Checked
2026-11-09. Confirmed on the Autopsy 4.21.0 Image Gallery page (read in full): required ingest modules, options setting, grouping and default sort, dashed border, no automatic categorization, one category plus many tags, CAT-0 to CAT-5 names, shortcuts, report generation, multi-user behaviour. Confirmed on the ExifTool EXIF tag page that DateTimeOriginal, Make, Model, Software exist as tag names (tag-name table searched, not read in full). Removed: group-by EXIF camera model, GPS and serial-number tags, OffsetTimeOriginal, `exiftool -a -G1 -s` command, thumbnail-mismatch and messaging-app claims, Embedded File Extractor, object/face modules, the exiftool.org landing source.
Method: documentation only; no commands were run.
