---
id: computing-software.digital-forensics-incident-response.evidence-handling.imaging-failing-drives-with-ddrescue
name: imaging-failing-drives-with-ddrescue
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [ddrescue, disk-imaging, forensic-acquisition, damaged-media, dfir]
level: advanced
status: docs-checked
description: "Image failing or damaged drives with GNU ddrescue: mapfile, a first fast pass, reverse and retry passes, and marking unread sectors in the output."
sources: ["https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Imaging failing drives with ddrescue

**Goal:** get the maximum readable data off a degrading drive with minimum stress, and document exactly which sectors could not be read.

## Strategy
The mapfile records progress and bad areas. The manual calls it an essential part of ddrescue's effectiveness: only the blocks needed are read, and you can interrupt the rescue and resume at the same point. Use it.
```bash
# pass 1: fast copy, skip the scraping phase
ddrescue -n -d /dev/sdb image.dd image.map
# pass 2: retry bad sectors, reverse direction
ddrescue -d -r3 -R /dev/sdb image.dd image.map
```
- `-n` (`--no-scrape`) skips the scraping phase, avoiding long time on the most difficult parts.
- `-d` (`--idirect`) reads with direct disc access, bypassing the kernel cache; the sector size must be correct and not all systems support it.
- `-r n` (`--retry-passes`): number of retry passes, default 0. To retry bad sectors from a previous run you must give a nonzero number. Every bad sector is tried once per pass and the direction is reversed after each pass.
- `-R` (`--reverse`) reverses the direction of all passes.
- `-f` (`--force`) is needed when the output is a device or partition, not a regular file. Image to a regular file on a healthy drive.
- Never rescue a read-write mounted partition; best that the device is not mounted at all, even read-only.
- The algorithm has five phases: copying, trimming, sweeping, scraping, retrying. A bad drive can block ddrescue for a long time until the kernel gives up.

## Unread areas
- If the output is a regular file created by ddrescue, areas marked bad-sector contain zeros. ddrescue does not write zeros itself when it finds bad sectors, so rerunning on the same output fills gaps without wiping data already rescued.
- Fill mode (`--fill-mode`) can write a marker string into the blocks of a given mapfile status. The manual's example fills bad-sector blocks with a string such as "BAD-SECTOR" and notes `l` adds location data. Do this on a working copy, not on the master image.
- State in the report that the image hash is the reference for the copy, and keep the mapfile as an exhibit listing unreadable ranges.

## Physical considerations
Clicking or grinding drives: stop and consider a data recovery lab before reading. Use a write blocker or a direct connection with the device set read-only.

## Verify
Check the final status line ("rescued", "bad-sector", "bad areas") and record it with the bad-range list in the acquisition notes.

## Checked
Confirmed against the GNU ddrescue manual: mapfile description, `-n`, `-d`, `-r`, `-R`, `-f`, mounted-partition warning, five phases, zero-filled bad-sector note, and fill mode. Removed claims the manual does not give: `ddrescuelog -t`, `dd conv=noerror,sync` comparison, SSD behaviour, cooling advice, ewfacquire conversion, the "reverse helps some heads" rationale, and the NIST SP 800-86 source (no claims relied on it).

Method: docs-only read of cited page, 2026-11-09
