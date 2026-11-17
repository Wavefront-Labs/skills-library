---
id: computing-software.digital-forensics-incident-response.incident-response-process.contemporaneous-investigation-notes
name: contemporaneous-investigation-notes
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [investigation-notes, contemporaneous-notes, incident-documentation, case-notes, dfir]
level: practitioner
status: draft
description: "Keep contemporaneous investigation notes that hold up in review and court: what to record, UTC timestamps, tool versions, hashes, and note-taking discipline."
sources: ["https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.swgde.org/documents/published-complete-listing/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contemporaneous investigation notes

**Goal:** another examiner could repeat your work from your notes, and the notes withstand
cross-examination (SP 800-86 3.4: document every step; SWGDE best practices).

## Record for every action
- Date/time in **UTC** (and the local zone if relevant), examiner name.
- What you did, on which evidence item (evidence ID, hash), with which tool **and version**,
  command line or settings.
- What you observed, including negatives ("no Run key entries referencing ProgramData").
- Output files produced, with path and hash.
- Reasoning and next step; mark interpretations as such.

## Format
- Case notes file per examiner (Markdown or a case platform), append-only. Never rewrite
  earlier entries; add corrections with a new timestamp referencing the original.
- Commands: paste the exact command run, not a cleaned-up version.
- Screenshots named `<case>-<evid>-<UTC>-<what>.png` and listed in notes.
- Bound paper notebook with numbered pages for on-site work; scan at end of day.

## Example entry
```
2026-10-16T14:22Z  CJ  EVID-003 (sha256 9f2c...)  Volatility 3 2.7.0
vol -f EVID-003.raw windows.pstree > exports/EVID-003_pstree.txt (sha256 41ab...)
Observed: rundll32.exe PID 5124, parent WINWORD.EXE PID 4410, no command-line args.
Interpretation: likely macro-launched payload; next: malfind on 5124.
```

## Gotchas
- Notes written up days later are reconstructions, not contemporaneous; say so if it happens.
- Notes are discoverable. Write facts and professional assessments; no jokes or speculation
  about people.
- Keep notes per case; never mix two cases in one file.

## Verify
Pick a finding in your report and trace it back through notes to the original evidence
hash. Any break in that chain is a documentation failure.
