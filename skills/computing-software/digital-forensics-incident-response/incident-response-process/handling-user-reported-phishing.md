---
id: computing-software.digital-forensics-incident-response.incident-response-process.handling-user-reported-phishing
name: handling-user-reported-phishing
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [user-reported-phishing, phishing-triage, report-message, abuse-mailbox, incident-triage, dfir]
level: practitioner
status: docs-checked
description: "Run the Microsoft 365 user-reported phishing pipeline: SecOps reporting mailbox, destinations, third-party button format, Submissions triage and reporter feedback."
sources: ["https://learn.microsoft.com/en-us/defender-office-365/submissions-user-reported-messages-custom-mailbox"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Handling user-reported phishing (Microsoft 365)

User reports feed analysts a stream of suspect mail. A correct intake pipeline keeps the original
message intact and gets a verdict back to the reporter. This skill covers the Microsoft 365 /
Defender for Office 365 pipeline described on the "User reported settings" Learn page.

## Intake design
- Reporting works through the built-in Report button in Outlook, or a supported non-Microsoft
  add-in. "Monitor reported messages in Outlook" must be selected for the integrated experience.
- **Send reported items to** one of: Microsoft and the reporting mailbox, reporting mailbox
  only, or Microsoft only (the last is not available with a non-Microsoft add-in). In US
  Government clouds (GCC, GCC High, DoD) only "reporting mailbox only" is available.
- If no mailbox is chosen, the default reporting mailbox is the global admin's Exchange Online
  mailbox. Distribution groups and external or on-premises mailboxes are not allowed.
- With the built-in button, reports appear in Submissions, User reported tab
  (security.microsoft.com/reportsubmission?viewid=user) whatever the destination.
- With "reporting mailbox only" the Result shows **Not Submitted to Microsoft** until an admin
  manually submits the message.
- With Defender for Office 365 Plan 2, a phishing report triggers an automated investigation
  and response (AIR) investigation, and notification emails to the reporter can be sent
  (phishing or malware, spam, no threats found).
- Configure the reporting mailbox as a **SecOps mailbox** in the advanced delivery policy so
  reports are not filtered, and exclude it from DLP. Not doing the SecOps step can make a user
  report trigger a training assignment in phishing-simulation products.

## Non-Microsoft report buttons
Messages sent to the reporting mailbox must:
- carry the original message **unmodified as an uncompressed .EML or .MSG attachment**; do not
  forward it (forwarding strips required headers); a message with multiple attached messages is
  discarded;
- include headers X-Microsoft-Antispam-Message-Info, Message-Id,
  X-Ms-Exchange-Organization-Network-Message-Id and X-Ms-Exchange-Crosstenant-Id (the tenant id);
- start the Subject with `1|` or `Junk:`, `2|` or `Not junk:`, or `3|` or `Phishing:`; with no
  prefix the message is always treated as phishing.
- Do not run Microsoft and non-Microsoft buttons together (duplicate submissions); the report
  must come from the recipient user, not a service account.
- Simulation messages reported through non-Microsoft tools are not captured in attack
  simulation reports.

## Triage and feedback
1. Work the User reported tab; for reporting-mailbox-only entries decide whether to submit to
   Microsoft.
2. Use **Mark as and notify** to send the reporter the outcome. The default result email is
   localized to the recipient's language and can be customized for Phishing, Junk and
   No threats found.
3. Customize the sender address (default submissions@messaging.microsoft.com) and logo if
   wanted.
4. Reporters can also report from quarantine when releasing items ("Allow reporting for
   quarantined items").

## Verify
Submit a test report and confirm it appears on the User reported tab with full headers and the
expected Subject prefix, the result email reaches the reporter, and simulation reports do not
create training assignments.

## Checked
Checked 2026-11-08 against the cited Microsoft Learn page. Removed because it is not on that
page: the time targets, header analysis steps, hunting tables and queries for scoping clicks,
purge and block steps, credential-reset steps, metrics, the Google Workspace report-phishing
claim (the Google page cited is about attachment, link and spoofing protection settings, not
reporting), and the NIST 800-61r3 landing page.
Method: docs-only read of cited pages, 2026-11-08
