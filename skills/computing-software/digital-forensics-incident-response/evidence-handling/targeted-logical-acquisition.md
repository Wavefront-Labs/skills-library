---
id: computing-software.digital-forensics-incident-response.evidence-handling.targeted-logical-acquisition
name: targeted-logical-acquisition
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [logical-acquisition, targeted-collection, forensic-acquisition, ftk-imager, robocopy, dfir]
level: practitioner
status: draft
description: "Perform targeted logical acquisition when full imaging is impossible: file selection, preserving metadata and timestamps, custom content images, and documenting scope."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.exterro.com/digital-forensics-software/ftk-imager"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Targeted logical acquisition

**Goal:** collect specific files and folders (with their metadata) when a full disk image is
too large, too slow, or not permitted (servers, NAS, cloud shares, legal scope limits).

## When it is appropriate
- Multi-TB file servers, SANs, mailbox stores; scope set by counsel; remote hosts on slow
  links; triage at scale (KAPE/Velociraptor is targeted logical acquisition of artefacts).
- Limitation: no unallocated space, slack, deleted files or filesystem metadata beyond what
  the tool preserves. State this in the report.

## Tools and metadata preservation
- **FTK Imager**: "Create Custom Content Image (AD1)" from selected files; preserves
  timestamps and hashes per file.
- **KAPE** target files collect locked files via raw access and keep MACB times in its
  copy log; **Velociraptor** collections record file metadata in JSON.
- **robocopy** for large shares (not forensic but preserves times):
  `robocopy \\srv\share \evid\share /E /COPY:DAT /DCOPY:T /R:1 /W:1 /B /LOG:\evid\copy.log /NP`
  (`/B` backup mode needs privilege; access times may still change on source).
- Linux: `tar --xattrs --acls -cpf` or `rsync -aHAX --times` read-only mount; hash every file.

## Process
1. Write the scope (paths, date ranges, file types, custodians) and get approval.
2. Produce a **file listing with metadata** of the source (paths, sizes, MACB times)
   before copying; it shows what existed even if not collected.
3. Copy, then hash every file (`hashdeep -r -c sha256 -l . > hashes.txt`) and compare with
   source hashes where possible.
4. Package into an evidence container (AD1, ZIP with manifest, or E01 logical L01).

## Verify
Source listing, collected set and hash manifest reconcile (counts and sizes), and the
report states scope and limitations.
