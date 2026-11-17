---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.linux-filesystem-timelines-with-crtime
name: linux-filesystem-timelines-with-crtime
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [linux-timeline, crtime, bodyfile, mactime, linux-forensics, dfir]
level: practitioner
status: docs-checked
description: "Build filesystem timelines with fls bodyfiles and mactime, read creation time (crtime/btime) with statx and debugfs, and avoid mactime option clashes."
sources: ["https://www.sleuthkit.org/sleuthkit/man/fls.html", "https://www.sleuthkit.org/sleuthkit/man/mactime.html", "https://man7.org/linux/man-pages/man2/statx.2.html", "https://man7.org/linux/man-pages/man8/debugfs.8.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linux filesystem timelines with crtime

Linux exposes modification (mtime), access (atime), status-change (ctime) and, through `statx`, a creation timestamp (`stx_btime`). The statx manual describes `stx_ctime` as the last status change time, so ctime is not creation time; `stx_btime` is the file's creation timestamp when the filesystem provides it.

## From an image (The Sleuth Kit)
```bash
fls -r -m / -o 2048 disk.dd > body.txt                    # bodyfile (time machine format), filesystem at sector 2048
mactime -b body.txt -d 2026-10-01..2026-10-18 > timeline.csv
```
- `fls -m mnt` prints entries in time machine format for `mactime`, prepending `mnt` to file names; `-r` recurses; `-o` is the sector offset where the filesystem starts; `-l` long format shows modified, accessed, changed and created times.
- `fls -s seconds` corrects a known clock skew of the original system (only used with `-l` or `-m`); `-z zone` gives the original time zone.
- `mactime` reads the body file from `-b` or stdin and writes to stdout. `-d` gives comma-delimited output for spreadsheets, `-y` shows ISO 8601 dates, `-m` shows the month as a number, `-h` prints header info.
- The date range is `yyyy-mm-dd` (start only) or `yyyy-mm-dd..yyyy-mm-dd`, optionally with `Thh:mm:ss`.
- Do not combine `-z` with `-y` or `-m` with `-y`: the manual says `-z` does not work with `-y`, and `-m` does not work with it either. Use `-z` to name the time zone of the collected data, or use `-y` alone.

## On a live system or mounted copy
The creation time comes from the `statx` system call (`STATX_BTIME` requests `stx_btime`). Whether a given filesystem records it is not stated in the man page; check that the field comes back before trusting it.

`debugfs` opens a filesystem read-only unless `-w` is given; `-c` (catastrophic mode) skips reading the inode and group bitmaps and forces read-only, for badly corrupted filesystems. Its `stat filespec` command displays the contents of the inode structure of that file.

## Reading the results
Compare the four times for key files and treat any oddity (for example a creation time later than the modification time) as a lead to confirm with other evidence, not a conclusion.

## Verify
For key files, times from the timeline agree with independent sources (auditd, package logs, shell history) or the discrepancy is explained.

## Checked
Checked 2026-11-09 against the fls and mactime manual pages, the statx(2) man page (stx_btime, stx_ctime, STATX_BTIME) and the debugfs(8) man page (-w, -c, stat). Removed: ext4, XFS and Btrfs support claims, TSK nanosecond support, coreutils and findutils versions, the find `%B@` recipe, the MACB behaviour table, relatime, overlayfs, package-install timestamp notes and the `-d -y -z UTC` command (mactime says `-z` does not work with `-y`).
Method: documentation only; no commands were run.
