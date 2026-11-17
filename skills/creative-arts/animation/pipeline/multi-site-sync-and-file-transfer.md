---
id: creative-arts.animation.pipeline.multi-site-sync-and-file-transfer
name: multi-site-sync-and-file-transfer
category: creative-arts
field: animation
product: pipeline
tags: [file-transfer, multi-site-sync, rsync, rclone, robocopy, aspera, replication, transfer-verification]
level: practitioner
status: draft
description: "Move production data between sites: choosing rsync, rclone, robocopy or accelerated transfer, verifying with checksums, handling deletes, bandwidth and resumability."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Multi-site sync and transfer

Studios with several sites, remote artists or vendors need to move big files reliably. Pick the tool for the job and always verify.

## Tool choice
- **rsync** (Linux/macOS, and available on Windows through WSL or ports): delta transfer over SSH, resumable (`--partial`), preserves times and permissions. Good for one-way mirroring between servers.
- **rclone**: copies to and from cloud object storage and many remote protocols; supports `--checksum`, parallel `--transfers`, bandwidth limits (`--bwlimit`) and `rclone check` for verification.
- **robocopy** (Windows): robust local and network copies with `/R:` retries, `/W:` wait, `/MT:` threads, and `/MIR` mirror (which **deletes** files at the destination that are not in the source).
- **Accelerated transfer products** (IBM Aspera, Signiant and similar): UDP-based or tuned protocols for long, high-latency links with encryption, often required for delivery to broadcasters and studios. Licences and platform access are needed.
- **Replicated storage or sync services** can keep two sites in near-sync but need careful conflict handling.

## Practice
1. **Define direction**: one-way (source of truth to mirror) is safe; two-way sync needs conflict rules.
2. **Dry run** deletes: `rsync -n` or robocopy `/L` before using mirror options.
3. **Verify** after transfer: compare checksums (`checksum-fixity.md`), file counts and sizes. Examples: `rsync -c` for checksum comparison, `rclone check src dst`.
4. Transfer **in manifest order** and keep a log; for sequences, verify the frame count (`missing-frame-detection.md`).
5. Handle **bandwidth**: schedule heavy transfers off hours, apply bandwidth limits so interactive work is not starved.
6. Make transfers **resumable**; avoid single huge archives for unreliable links.
7. **Security**: encrypt in transit (SSH, TLS), use per-vendor credentials, expire them after the job (`secure-file-transfer-and-screeners.md`).

## Gotchas
- Case sensitivity and illegal characters differ between Windows, macOS and Linux file systems.
- Timestamp resolution differences can cause endless re-copies; use size and checksum.
- Mirroring the wrong direction can delete the source of truth; label the roles of the sites.

## Verify
- [ ] Dry run reviewed before any delete-capable command.
- [ ] Checksums or counts match at destination.
- [ ] Credentials revoked when the transfer is finished.
