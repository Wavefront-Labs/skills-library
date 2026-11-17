---
id: computing-software.cybersecurity-defensive.system-hardening.log-integrity-and-tamper-evidence
name: log-integrity-and-tamper-evidence
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [audit-log-management, log-integrity, tamper-evidence, worm-storage, cloudtrail-log-file-validation, journald-seal, log-clearing-detection]
level: advanced
status: docs-checked
description: "Make logs trustworthy as evidence: fast off-host shipping, immutable storage, signed digests (CloudTrail validation, journald FSS), duty separation, tamper detection."
sources: ["https://csrc.nist.gov/pubs/sp/800/92/final", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html", "https://www.freedesktop.org/software/systemd/man/latest/journalctl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log integrity and tamper evidence

Attackers clear or edit logs. Logs used in investigations, audits or court must be shown complete
and unaltered.

## 1. Get logs off the host quickly
Local logs are only as trustworthy as the host. Forward in near real time (syslog over TLS, WEF, agents)
to a collector the host's admins cannot modify. A gap between attack time and forwarding time is the window
for tampering.

## 2. Immutable storage
- Store log archives in write-once (WORM) or object-lock storage from your platform; check the vendor's
  documentation for the exact retention-lock mode.
- CloudTrail log and digest files can be kept in Amazon S3 or Amazon Glacier; S3 MFA Delete can further protect
  the digest files.
- SIEM retention with restricted delete rights, held by a separate role with alerting.

## 3. Cryptographic integrity
- **CloudTrail log file integrity validation**: SHA-256 hashing and SHA-256 with RSA signing; every hour CloudTrail
  delivers a signed digest file to the trail's S3 bucket, with different key pairs per Region. Enabling it only
  delivers digests; you must validate with the AWS CLI:
  `aws cloudtrail validate-logs --trail-arn <arn> --start-time <UTC_TIMESTAMP>`.
- **journald Forward Secure Sealing**: `journalctl --setup-keys` generates a sealing key (stays on the host) and a
  verification key (store it externally); verify with `journalctl --verify --verify-key=<key>`. The sealing key
  change interval defaults to 15 minutes; shorter intervals cost CPU but shorten the window of undetectable edits.
- Hash manifests for exported evidence (SHA-256 per file, recorded in chain-of-custody notes).

## 4. Separation of duties
System admins must not administer the log platform; log platform admins should not administer the systems
they monitor. Break-glass for both with alerting.

## 5. Detect tampering
- Windows: alert on log-clear events, audit policy changes and the Event Log service stopping (look up the event
  IDs in Microsoft documentation).
- Linux: truncation of log files (file size drop), auditd stopped, history files deleted; auditd rules watching
  the log directory.
- Cloud: trail stop/delete and event-selector changes, diagnostic setting deletion.
- Silence detection: per-source heartbeat alerts when expected events stop.

## Gotchas
- Time integrity matters too: NTP authenticated sources; record clock offsets.
- Agents with local caching may lose data on host compromise before upload; tune buffer flushing.

## Verify
`aws cloudtrail validate-logs` reports all digests valid for the period, a test log-clear in a lab
raises an alert, and deleting a locked archive object fails.

## Checked
2026-10-31. Confirmed on the CloudTrail log file validation page: SHA-256 and SHA-256 with RSA, hourly signed digest
files in the trail bucket, per-Region key pairs, S3 MFA Delete, enabling does not validate. Confirmed on the
journalctl man page: `--setup-keys`, `--verify`, `--verify-key=`, sealing key stays on host, verification key stored
externally, 15 min default interval. Removed as not confirmed: ATT&CK ID, vendor WORM and SIEM role names, RFC 5848
remark, Windows event IDs, `wevtutil`/`auditctl` command lines, specific cloud API names, and the 30-day figure.
Method: documentation only; no commands were run.
