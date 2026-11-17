---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.feature-extraction-with-bulk-extractor
name: feature-extraction-with-bulk-extractor
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [bulk-extractor, feature-extraction, email-addresses, urls, histograms, carving, sleuthkit, dfir]
level: practitioner
status: draft
description: "Run bulk_extractor across disk or memory images to extract emails, URLs, domains, credit cards and network packets, and read the histograms for leads."
sources: ["https://github.com/simsong/bulk_extractor", "https://forensics.wiki/bulk_extractor/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feature extraction with bulk_extractor

**Goal:** sweep an entire image, ignoring filesystem structure, for identifiers (emails,
URLs, domains, IPs, phone numbers, card numbers, search terms) and decompress embedded data
along the way. It finds things in unallocated space, slack, pagefile and compressed blobs
that filesystem tools miss.

## Run it
```bash
bulk_extractor -o be_out image.E01                       # all default scanners, multi-threaded
bulk_extractor -o be_out -j 8 -S ssn_mode=1 image.raw
bulk_extractor -o be_mem -x accts mem.raw                 # disable a noisy scanner
bulk_extractor -o be_out -e wordlist image.raw            # enable a disabled scanner
bulk_extractor -o be_out -F keywords.txt image.raw        # find scanner with a regex list
bulk_extractor -H                                          # list scanners and settings
```
It handles raw, E01 and split raw directly, and recurses into ZIP, GZIP, PDF, base64,
hiberfil, and more, recording a "forensic path" (offset plus decoding steps) for each hit.

## Output files that matter
| File | Use |
|---|---|
| `email.txt`, `email_histogram.txt` | who communicated; the histogram ranks frequency |
| `url.txt`, `url_histogram.txt`, `url_searches.txt` | browsing and search terms, even from unallocated |
| `domain_histogram.txt` | quick view of contacted infrastructure |
| `ip.txt`, `ether.txt`, `packets.pcap` | IPs and network packets carved from memory/pagefile (open pcap in Wireshark) |
| `ccn.txt`, `pii.txt` | card numbers and PII (breach scoping) |
| `json.txt`, `exif.txt`, `gps.txt` | structured data, photo metadata |
| `aes_keys.txt` | AES key schedules (memory images) |
| `wordlist.txt` | dictionary for password cracking encrypted containers |
Each line: `offset<TAB>feature<TAB>context`. Offsets like `12345-GZIP-200` mean "200 bytes into
a GZIP stream found at offset 12345".

## Mapping hits back to files
`identify_filenames.py --image_filename image.raw be_out be_annotated` (needs a DFXML file
listing from `fiwalk`), or use the offset with TSK: `ifind -d <offset/blocksize> image.raw` then
`ffind`/`istat`. BEViewer (GUI) browses features and context.

## Gotchas
- Histograms are the time saver: start there, then drill into individual hits.
- Default runs on large images take hours; disable irrelevant scanners and use `-j`.
- Stop-lists (`-w stoplist.txt`) remove known-benign features (OS default emails/URLs) found in
  a clean baseline image.

## Self-check
Key identifiers are mapped back to a file or region with offset, and false positives are
filtered against a baseline.
