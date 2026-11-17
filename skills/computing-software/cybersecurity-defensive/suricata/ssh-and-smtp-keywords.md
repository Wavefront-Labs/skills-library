---
id: computing-software.cybersecurity-defensive.suricata.ssh-and-smtp-keywords
name: ssh-and-smtp-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [ssh-keywords, hassh, smtp-keywords, smtp-rcpt-to]
level: practitioner
status: docs-checked
description: "Match SSH banners and hassh fingerprints and SMTP helo, mail_from and rcpt_to fields with their sticky buffers."
sources: ["https://docs.suricata.io/en/latest/rules/ssh-keywords.html", "https://docs.suricata.io/en/latest/rules/smtp-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH and SMTP keywords

## SSH (sticky buffers, fast_pattern capable)
`ssh.proto` (old name `ssh_proto` still works), `ssh.software`, `ssh.hassh` (MD5 of client algorithms), `ssh.hassh.string`, `ssh.hassh.server`, `ssh.hassh.server.string`. The `.string` forms match the raw algorithm list.

Inspectable only after a valid banner; client data at `request_kex`, server at `response_kex`. An invalid banner or record raises `ssh.invalid_banner` and `ssh.invalid_record`. Rules relying on the old `ssh:request_complete` hook no longer match well-formed flows.

Example: `ssh.software; content:"openssh"; nocase;`

## SMTP
- `smtp.helo`: first HELO parameter, matched per transaction.
- `smtp.mail_from`: first MAIL FROM parameter.
- `smtp.rcpt_to`: any RCPT TO parameter (multi buffer).
- Frames: `smtp.command_line`, `smtp.response_line`, `smtp.data`, `smtp.stream`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/ssh-keywords and rules/smtp-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Removed the hassh app-layer config requirement (not on the pages) and the deprecated label.

Method: documentation only; no commands were run.
