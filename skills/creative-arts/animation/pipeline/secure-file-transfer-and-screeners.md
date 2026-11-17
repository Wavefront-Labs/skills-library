---
id: creative-arts.animation.pipeline.secure-file-transfer-and-screeners
name: secure-file-transfer-and-screeners
category: creative-arts
field: animation
product: pipeline
tags: [secure-screeners, secure-transfer, screeners, watermarking, content-security, forensic-watermark, expiring-links]
level: practitioner
status: draft
description: "Send unreleased animation safely: approved transfer channels, encryption, expiring per-recipient access, watermarked screeners, DRM review platforms and audit logs."
sources:
  - https://www.motionpictures.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Secure file transfer and screeners

Unreleased episodes and shots must not leak. Choose controlled channels and add traceability.

## Approved channels
- Use the **platform your client or distributor specifies**, or a company-approved managed transfer system (managed SFTP, accelerated-transfer products, or a secure review platform). Do not use personal consumer file-sharing links or email attachments for unreleased content.
- **Encrypt in transit** (TLS or SSH) and, for sensitive deliverables, **at rest**.
- Use **per-recipient accounts or links** with an **expiry date**, optional **download limits**, and a **password sent through a different channel**.
- Keep an **audit log**: who sent what to whom, when, and whether it was downloaded.

## Screeners
- Prefer **streaming review** in a DRM-protected player over giving out files; the recipient watches but does not keep a copy.
- If files must go out, apply a **visible watermark** (recipient name or ID, date) and, where available, a **forensic (invisible) watermark** that identifies the recipient if the file leaks (`forensic-watermarking.md`).
- Use lower resolution or bitrate when quality does not matter, and a burn-in timecode for notes (`review-burn-ins.md`).
- Remove metadata that identifies internal paths or names.

## Process
1. Check the recipient is authorised (`access-control-and-need-to-know.md`).
2. Prepare the watermarked version, record the recipient ID and file checksum.
3. Send through the approved system with an expiry; confirm receipt through a separate channel if needed.
4. After the review window, revoke access and request deletion where appropriate; log it.
5. If a leak is suspected, follow the incident procedure: identify the version and watermark, notify the client according to the contract, and preserve logs.

## Gotchas
- Screen recording cannot be fully prevented; watermarks are your deterrent and tracing tool.
- Links forwarded to others bypass per-person checks; use authenticated access.

## Verify
- [ ] Each recipient has a unique, watermarked copy or authenticated stream.
- [ ] Links expire and access is revoked after review.
- [ ] Transfers are logged.
