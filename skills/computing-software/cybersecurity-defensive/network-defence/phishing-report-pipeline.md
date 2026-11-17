---
id: computing-software.cybersecurity-defensive.network-defence.phishing-report-pipeline
name: phishing-report-pipeline
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [email-security, phishing-report-pipeline, report-message-button, user-reported-phishing, mailbox-purge, soar-phishing, phishing-triage-automation]
level: practitioner
status: draft
description: "Build the phishing report pipeline: one-click report button, triage automation, verdict feedback to users, and organisation-wide purge of confirmed campaigns."
sources: ["Microsoft Learn - User reported message settings and the Submissions page", "CISA Phishing Guidance: Stopping the Attack Cycle at Phase One", "NIST SP 800-61r3 (detection sources)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phishing report pipeline

**Goal:** users report suspicious mail in one click, the SOC triages fast (mostly automated),
confirmed campaigns are purged from every mailbox, and reporters get feedback.

## Reporting
- Deploy a built-in **Report** button (Outlook built-in Report button in Microsoft 365; Gmail "Report phishing" with Workspace routing) so reports arrive with full headers as attachments to a dedicated mailbox and to the vendor.
- Microsoft 365: Settings > Email & collaboration > User reported settings: send to Microsoft and a reporting mailbox; customise the user messages.

## Triage automation (SOAR or Defender AIR)
1. Parse: sender, auth results (SPF/DKIM/DMARC), URLs, attachments, reply-to, display name.
2. Enrich: URL and file reputation, sandbox detonation, sender history, similar messages in the tenant (same subject/sender/URL).
3. Cluster duplicates into one case per campaign.
4. Verdict: malicious / spam / simulation / clean. Auto-close known simulation campaigns and clean newsletters.
5. Analyst reviews malicious and uncertain ones.

## Response to a confirmed phish
- Find all recipients: Threat Explorer / `Get-MessageTrace` / Content search on sender, subject, URL.
- Purge: Explorer "Soft delete" or `New-ComplianceSearchAction -Purge -PurgeType SoftDelete`.
- Block sender/domain/URL in the tenant block list; add URL to proxy/DNS blocks.
- Check who clicked (Safe Links click logs, proxy logs) and who entered credentials (sign-in logs after click time) -> reset, revoke sessions.
- Notify reporters: "Thanks, this was phishing and has been removed from 214 mailboxes."

## Metrics
Report rate, time to purge, % of campaigns reported before the first click, simulation report rate.

## Gotchas
- Forward-as-attachment instructions confuse users; a button that does it is essential.
- Reporting mailbox must be excluded from filtering, or reports get quarantined.
- No feedback to users kills reporting culture quickly.

## Verify
- [ ] Test report reaches the queue with original headers within minutes.
- [ ] Time from first report to org-wide purge measured; target under 1 hour for confirmed phish.
