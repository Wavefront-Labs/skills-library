---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.rdp-bitmap-cache-and-client-artefacts
name: rdp-bitmap-cache-and-client-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [user-activity-artefacts, rdp-bitmap-cache, rdp-forensics, lateral-movement, bmc-tools, terminal-server-client, dfir]
level: advanced
status: docs-checked
description: "Recover fragments of what an RDP client user saw by parsing bitmap cache files (bcache*.bmc, cache????.bin) with bmc-tools; scope, options and corroboration."
sources: ["https://github.com/ANSSI-FR/bmc-tools", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDP bitmap cache and client artefacts

**Goal:** on a host used as an RDP source, partly reconstruct what the user saw on the remote screen from the RDP bitmap cache.

## Input
`bmc-tools` (ANSSI, CECILL-2.1 licence) processes `bcache*.bmc` and `cache????.bin` files found inside Windows user profiles. Collect them from the user profile of the account that ran the client, then process copies.

## Usage
```bash
./bmc-tools.py -s <cache file or directory> -d <output dir> -b
```
- `-s` source file or directory; `-d` destination directory for extracted bitmaps (it must exist: v3.02 added a check).
- `-b` builds a collage bitmap aggregating all tiles; `-w` sets tiles per line (default 64).
- `-o` extracts old bitmap data found in the cache file (supported from 3.05 per the changelog); `-c` limits the number of bitmaps; `-v` more output.
- `-k` splits the output of different inputs into separate folders, intended for KAPE output.
- Since 3.00 the tool decompresses tiles.

## Reading the output
Review collages for fragments of the remote screen (windows, paths, tool interfaces). Tiles are fragments, not full screenshots: treat anything read from them as a lead to corroborate, not as a complete record.

## Corroboration
Pair the cache with other client-side evidence for where the user connected and when. The SANS Windows Forensic Analysis poster maps artefacts to investigation questions (what files were opened, which programs ran, where the user connected); take artefact locations and timestamp rules from it and from vendor documentation, and test on a lab host before reporting.

## Gotchas
- Attackers using their own RDP client leave different source artefacts than the built-in client.
- Cache content is limited to what the client cached; absence of a cache file proves nothing on its own.

## Verify
Any destination or screen content drawn from the cache is matched against independent evidence (logon records on the destination host at consistent times).

## Checked
2026-11-08. Confirmed against the bmc-tools README (input files, options, changelog) and the SANS poster page (general description only). Removed as unconfirmed: cache path, 64x64 tile size, Terminal Server Client registry keys, Default.rdp, jump list, Prefetch and event log IDs, destination-side event IDs, and the `bitmapcachepersistenable` policy claim. The JPCERT/CC sheet cited earlier was an unreadable page and was dropped.
Method: documentation only; no commands were run.
