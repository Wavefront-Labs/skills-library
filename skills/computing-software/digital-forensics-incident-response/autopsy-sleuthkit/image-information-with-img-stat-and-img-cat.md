---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.image-information-with-img-stat-and-img-cat
name: image-information-with-img-stat-and-img-cat
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [img-stat, img-cat, sleuth-kit, image-formats, dfir]
level: practitioner
status: docs-checked
description: "Use The Sleuth Kit img_stat to check image type, size and sector size, and img_cat to output the data of an embedded-format or split image as raw bytes."
sources: ["https://www.sleuthkit.org/sleuthkit/man/img_stat.html", "https://www.sleuthkit.org/sleuthkit/man/img_cat.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Image information with img_stat and img_cat

`img_stat` describes an image file; `img_cat` outputs its contents. Both read the image format themselves, so they work on split images and non-raw formats.

## img_stat
```bash
img_stat disk.001            # split image: later segments are found automatically
img_stat -t disk.001         # print only the image type
img_stat -i list             # list supported image types
img_stat -i raw disk.001     # force the type instead of autodetecting
```
The manual says the output is image-format specific; at a minimum it gives the size and, for split formats, the byte range of each segment file. `-b dev_sector_size` sets the device sector size in bytes: if not given, the value in the image format is used when it exists, otherwise 512 bytes is assumed. If you pass only the first file of a numbered split sequence (for example ending `.001`), the following segments are included automatically.

Use it at intake to confirm the type, size and segments match the acquisition paperwork.

## img_cat
```bash
img_cat disk.001 > disk.raw                     # convert an embedded format to raw (needs space)
img_cat disk.001 | md5sum                       # hash only the image data
img_cat -s 2048 -e 4095 disk.001 > range.bin    # start and stop sector
```
Non-raw images contain embedded data and metadata; `img_cat` outputs only the data. That lets you convert an embedded format to raw, or calculate the MD5 of the data by piping the output to a hashing tool. `-s start_sector` and `-e stop_sector` bound the range; `-i` and `-b` work as for `img_stat`.

## Gotchas
- A raw copy costs disk space equal to the media size; prefer piping when a tool can read stdin.
- Passing a wrong sector size with `-b` to later tools shifts offsets computed from sector numbers.
- Image metadata is whatever the acquirer entered; cross-check it with the custody record.

## Verify
The hash of the `img_cat` output matches the acquisition hash recorded for the source media, and the `img_stat` size matches the recorded capacity.

## Checked
Checked 2026-11-09 against the img_stat and img_cat manual pages (synopsis, options, defaults, descriptions). Removed: E01 metadata (case number, examiner, stored hashes), 4Kn sector-size statement, SHA-256 hash recipe, strings pipeline, ewfmount and ewfverify comparisons, and the libewf source, none of which the manual pages state.
Method: documentation only; no commands were run.
