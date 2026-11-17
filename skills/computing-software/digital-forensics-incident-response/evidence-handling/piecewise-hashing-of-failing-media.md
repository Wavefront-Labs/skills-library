---
id: computing-software.digital-forensics-incident-response.evidence-handling.piecewise-hashing-of-failing-media
name: piecewise-hashing-of-failing-media
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [piecewise-hashing, sector-hashing, dcfldd, ddrescue, failing-drive, evidence-integrity, dfir]
level: advanced
status: draft
description: "Use piecewise (chunk or sector) hashing for failing media and partial images: dcfldd and ewfacquire chunk hashes, verifying good regions and explaining unreadable sectors."
sources: ["https://dcfldd.sourceforge.net/", "https://manpages.debian.org/testing/dcfldd/dcfldd.1.en.html", "https://github.com/libyal/libewf/wiki", "https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html", "https://github.com/simsong/hashdb"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Piecewise hashing of failing media

A whole-disk hash proves nothing when a failing drive returns different data on each read or has unreadable sectors: the acquisition hash will never match a re-read of the source. Piecewise hashing records a hash per chunk so you can prove which regions are stable and verify the image region by region.

## dcfldd
```bash
dcfldd if=/dev/sdb of=sdb.dd bs=4096 conv=noerror,sync \
  hash=sha256 hashwindow=1G hashlog=sdb.hashlog.txt \
  errlog=sdb.errors.txt
```
- `hashwindow=1G` writes one SHA-256 per 1 GiB window plus a total; `conv=noerror,sync` pads unreadable blocks with zeros so offsets stay aligned.
- Later, re-hash the image with the same window size and diff the logs: matching windows prove those regions of the image are unchanged.

## ddrescue first, then hash the image
For physically failing drives, use `ddrescue` (it retries smartly and keeps a mapfile). The mapfile records which ranges are finished, bad or untried; hash the image in windows and keep the mapfile as part of the evidence to show which windows contain zero-filled bad areas.

## E01
`ewfacquire` stores per-chunk checksums (Adler-32 for the chunk, plus optional MD5/SHA of the whole). `ewfverify` reports corrupted chunks by offset, so an E01 with a damaged section still verifies everywhere else.

## Sector-level hash sets
For finding known files in fragments or on damaged media, block hashes (e.g. 4 KiB sector hashes with `hashdb` / bulk_extractor's hashdb scanner) match known content sector by sector, independent of the file system.

## Reporting
State: total hash of the image (as acquired), window size, number of windows, which windows contain unreadable sectors (from the error log or mapfile), and that verification used window comparison. Findings located in clean windows are fully supported.

## Gotchas
- Never use `conv=noerror` without `sync`; dropped blocks shift every later offset.
- Choose window size before acquisition; changing it later means re-reading the failing source.
- Re-reading the source to "verify" stresses a dying drive; verify against the image instead.

## Verify
Re-hashing the image with the same window size reproduces every window hash in the acquisition log.
