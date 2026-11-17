---
id: computing-software.systems-network-administration.restic.faq-resume-interrupted
name: faq-resume-interrupted
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, faq, interrupted-backup, resume, unreferenced-packs, prune]
level: intro
status: docs-checked
description: "Resume an interrupted restic backup by rerunning it, and handle the harmless check warning about packs not referenced in any index."
sources:
  - https://restic.readthedocs.io/en/stable/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interrupted backups

## Resuming

Restic resumes simply: run the same backup command again. Restic periodically writes index files that record data already uploaded. These persist even if no snapshot was made, so the re-run skips re-uploading that data. Expect to lose only roughly the last few minutes of work. This holds for Ctrl-C, power loss and dropped connections.

Until a first snapshot exists for the backup set, restic re-scans local files on each run. That is normal and much faster than uploading.

## "Not referenced in any index"

`restic check` may report packs "not referenced in any index" after an interruption. The FAQ says this is not critical: it indicates surplus data, usually duplicates from an interrupted backup or upload. The fix is:

```
restic prune
```

## Related

- A stuck or killed run can leave locks; see `restic unlock`.
- If `restic check` reports other errors, follow the repair-damaged-repo skill.

## Checked

Checked 2026-11-08 against the restic FAQ page (faq) and Troubleshooting page (077_troubleshooting), both read in full. Confirmed: interrupted backups resume when re-run, periodic index files, up to a few minutes lost, the initial re-scan until a first snapshot exists, the harmless not-referenced-in-any-index check message fixed by prune, and manual unlock. Removed: the parent-snapshot hostname advice and the claim that check is clean after prune.

Method: documentation only; no commands were run.
