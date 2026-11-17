---
id: computing-software.digital-forensics-incident-response.evidence-handling.hash-manifests-with-hashdeep
name: hash-manifests-with-hashdeep
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hashdeep, hash-verification, evidence-integrity, hashing, dfir]
level: practitioner
status: draft
description: "Build and audit recursive hash manifests with hashdeep: multiple algorithms, relative paths, audit mode to prove a collection is complete and unaltered."
sources: ["https://github.com/jessek/hashdeep", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hash manifests with hashdeep

**Goal:** prove that a directory of evidence (a triage package, a log export, extracted files)
is complete and unchanged, file by file, months later.

## Create the manifest
```bash
hashdeep -c sha256,md5 -r -l ./CASE-014-007 > CASE-014-007.hashdeep.txt
```
- `-r` recursive, `-l` relative paths (manifest works after the folder moves), `-c` algorithms.
- Store the manifest beside the evidence and in the case record; hash the manifest itself too.

## Audit later
```bash
hashdeep -a -k CASE-014-007.hashdeep.txt -r -l ./CASE-014-007        # pass/fail
hashdeep -a -vv -k CASE-014-007.hashdeep.txt -r -l ./CASE-014-007    # list each problem
```
Audit reports: files matched, files moved, new files (not in manifest), known files not present,
and hash mismatches. "Audit passed" is your integrity statement.

## Matching mode (finding known files)
```bash
hashdeep -m -k known_malware.txt -r /mnt/image_root   # print files whose hashes are in the set
hashdeep -x -k nsrl_subset.txt -r /mnt/image_root      # negative match: files NOT known-good
```

## Windows alternative
```powershell
Get-ChildItem -Recurse -File | Get-FileHash -Algorithm SHA256 | Export-Csv manifest.csv -NoType
```
(no audit mode; compare with `Compare-Object` against a re-run).

## Gotchas
- Absolute paths in the manifest make audits fail after copying; always use `-l` (or `-b` bare names when paths do not matter).
- Line-ending conversion or antivirus quarantine silently alters files on copy; audit after each transfer.
- md5deep/hashdeep projects are old but stable; record the version used.

## Verify
`hashdeep -a` returns "Audit passed" on the evidence store copy and on every working copy distributed.
