---
id: computing-software.cybersecurity-defensive.security-operations.automated-phishing-response-playbook
name: automated-phishing-response-playbook
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soar, phishing-automation, phishing-triage, user-reported-phishing, url-detonation, mailbox-purge, playbooks, verdict-automation]
level: practitioner
status: docs-checked
description: "Automate user-reported phishing: ingest, parse and detonate, auto-close benign, find all recipients, purge, block, notify the reporter, and when to hand to a human."
sources: ["https://learn.microsoft.com/en-us/defender-office-365/air-about"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated phishing response playbook

User-reported phishing is the most automatable SOC workload: high volume, structured input,
repeatable decisions.

## Stages
1. **Ingest**: Report button submissions (for example Defender's "Email reported by user as
   malware or phish" alert, or a phishing@ mailbox). Pull the original as an `.eml`/`.msg` attachment, never
   the forwarded copy (headers are lost).
2. **Parse**: sender, return-path, reply-to, SPF/DKIM/DMARC results, sending IP, subject, URLs
   (including from QR codes and HTML attachments), attachment hashes.
3. **Enrich**: URL/domain reputation, domain age (newly registered = suspicious), sender history
   in your mail logs (first time sender?), internal or external.
4. **Detonate**: URLs in a sandbox/URL scanner, files in the sandbox. Respect privacy: do not
   send internal links to public scanners.
5. **Verdict**:
   - Known simulation (phish-sim headers/sender) -> thank reporter, close.
   - Marketing/spam with good auth and no malicious indicators -> close as benign, reply to user.
   - Malicious (detonation hit, credential-harvest page, known bad) -> respond.
   - Unclear -> analyst queue with all enrichment attached.
6. **Respond (malicious)**: search for all copies (same sender/URL/hash), remove them, block
   sender/domain/URL at the gateway, check click logs; if anyone clicked or submitted, open an
   identity incident (revoke sessions, reset password, review MFA methods).
7. **Notify**: tell the reporter the outcome (feedback drives reporting rates).

## Guardrails
- Auto-purge only on high-confidence verdicts and cap the number of mailboxes per automatic action
  (above the cap needs human approval) to avoid deleting a legitimate company-wide email.
- Never auto-block whole consumer domains (gmail.com) or partner domains.
- Log every automatic action with a link to the evidence.

## Built-in options
Automated investigation and response (AIR) in Microsoft Defender for Office 365 Plan 2 investigates
alerts automatically and queues remediation actions that the SecOps team approves or rejects in
the investigation, the incident or the Action center; SOAR playbooks wrap it or replace it for
other mail platforms.

## Metrics
Reports per week, % auto-closed, median time from report to purge, number of clicks after first
report (the number you are trying to drive to zero).

## Gotchas
- Forwarded reports strip headers; unwrap rewritten (safe-link) URLs before reputation checks.
- Sandbox evasion: credential pages can depend on URL parameters; detonate with the original URL
  including parameters.

## Verify
Monthly test: send a benign test campaign plus a lab "malicious" sample; confirm correct verdicts,
complete purge, and reporter notifications.

## Checked
2026-11-09. Read the Microsoft Learn page on AIR in Defender for Office 365 Plan 2: Plan 2
requirement, remediation actions queued for SecOps approval, review in the investigation, incident or
Action center, and the "Email reported by user as malware or phish" alert name. Removed: Google
Workspace, urlscan.io, Proofpoint and geo-fencing claims, the 500-mailbox example, and the Splunk
SOAR and CISA sources (blocked, 403). The stage order and guardrails are practitioner judgement.
Method: documentation only; no commands were run.
