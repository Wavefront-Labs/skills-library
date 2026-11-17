---
id: computing-software.digital-forensics-incident-response.evidence-handling.known-bad-hash-set-matching
name: known-bad-hash-set-matching
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [known-bad-hashes, hash-sets, nsrl, hashdeep, autopsy-hash-lookup, ioc-matching, dfir]
level: practitioner
status: docs-checked
description: "Match evidence against known-bad hash sets with Autopsy's Hash Lookup (notable, known, no change; MD5 lookup) and hashdeep, and know the limits of exact hashes."
sources: ["https://github.com/jessek/hashdeep", "https://sleuthkit.org/autopsy/docs/user-docs/4.21.0/hash_db_page.html", "https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl", "https://bazaar.abuse.ch/export/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Known-bad hash set matching

Known-good sets remove noise; known-bad sets flag files you must look at. Both are exact matches only, so they complement rather than replace YARA and behavioural analysis.

## Building a known-bad set
- Incident IOCs: hashes from malware analysis and EDR alerts in this case.
- Threat intelligence feeds. MalwareBazaar offers hash exports (CSV, plain text and others); every download needs a free abuse.ch Auth-Key, and the page asks you not to fetch recent additions more often than every 5 minutes or full dumps more than hourly.
- Record the source and date of each set.

## Autopsy Hash Lookup
- The module calculates MD5 for each file and looks it up in the hash sets. It also calculates SHA-256, but SHA-256 is not used in lookups, so the set you import must be MD5.
- Set types: **known** (safe to ignore; often standard OS and application files), **notable** (known bad: raise awareness, for example contraband images or malware) and **no change** (reveals information but is not notable).
- Import formats: text (one hash starting each line, such as md5, md5sum or md5deep output; `.txt`), index only (`.idx`), Autopsy `.kdb` SQLite sets, EnCase `.hash` and HashKeeper `.hsh`. Set the type when importing. Only `.kdb` sets can be edited locally.
- Most set types need an index; unindexed sets show in red and Autopsy can create one (or use `hfind` from The Sleuth Kit). The `.idx` file alone is sufficient to identify known files.
- Hits appear in the results tree as "Hashset Hits", grouped by set name, with any comments. "Send ingest inbox message for each hit" cannot be enabled for a known set.
- NSRL: Autopsy treats NSRL matches as simply "known" without calling them good or bad, because the NSRL covers software that may be good or bad depending on the investigation. NIST says the reference data set holds signatures of known, traceable applications, some of which may be considered malicious (for example steganography tools and hacking scripts), and none of illicit data such as child abuse images.

## hashdeep
The README describes md5deep as a set of cross-platform tools to compute hashes for any number of files, optionally recursing through directories, and to take a list of known hashes and display the filenames of input files whose hashes do or do not match. This version supports MD5, SHA-1, SHA-256, Tiger and Whirlpool. See its man page for the exact matching flags; this skill does not repeat them.

## Interpreting hits
- A hit means an identical file exists; confirm by context (path, timestamps, execution evidence) before concluding anything.
- Zero hits prove little: any change to the file defeats an exact hash. Follow with other methods (fuzzy hashing, YARA).

## Gotchas
- Generic files in bad sets (legitimate admin tools) give false positives; prune or treat as context.
- Keep set versions per case so results are reproducible.

## Verify
Re-running the match with the recorded set version reproduces the same hit list, and each hit is reviewed and annotated.

## Checked
Confirmed against the Autopsy 4.21.0 Hash Lookup page (MD5 lookup, SHA-256 not used, set types, import formats, indexing, results, NSRL handling), the hashdeep README, the NIST NSRL page and the MalwareBazaar export page (Auth-Key and fetch-frequency notes). Removed or corrected: the "SHA-256 preferred" advice (Autopsy looks up MD5), hashdeep `-m/-x/-k/-w` flags and commands, CISA IOC files, Project VIC/CAID, the empty-file hash, archive extractor and carver remarks, and fuzzy hashing tool names. The MalwareBazaar page hides its CSV and plain-text export details behind login, so only the stated notes are used.

Method: docs-only read of cited pages, 2026-11-09
