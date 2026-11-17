---
id: computing-software.it-support-helpdesk.remote-support-tools.responding-to-a-remote-access-scam-victim
name: responding-to-a-remote-access-scam-victim
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, scam-remote-access-response, tech-support-scam, social-engineering, incident-response, anydesk]
level: practitioner
status: draft
description: "Contain and clean up after a user let a scammer remote in: isolate, remove tools and persistence, reset credentials from a clean device, check money and report it."
sources:
  - "https://reportfraud.ftc.gov/"
  - "https://www.ncsc.gov.uk/collection/phishing-scams"
  - "https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# responding-to-a-remote-access-scam-victim

## First minutes
1. Stay calm and blame-free; users who feel safe report faster. Get the facts: when, what
   tool, what they typed, whether they logged into banking or entered card details.
2. **Isolate**: disconnect Wi-Fi/Ethernet, or use EDR network isolation (Defender for
   Endpoint "Isolate device") which keeps your management channel. Do not power off if
   security wants memory evidence; ask them.
3. Tell the security team; this is a security incident, not a desktop ticket.

## Credentials (from a clean device)
- Reset the user's password and revoke sessions (`Revoke-MgUserSignInSession` or the Entra
  portal), then re-register MFA if they may have approved prompts or shared codes.
- Any password saved in the browser on that PC is compromised; list sites and reset.
- If they did online banking during or after the session, they must call the bank's fraud
  line now.

## The device
- Remove the remote tool (AnyDesk, UltraViewer, ScreenConnect client) and look for more:
  other remote tools, new local admin accounts, scheduled tasks, startup items, browser
  extensions, new services. Run a full EDR scan.
- Corporate policy is usually reimage; it is faster than proving the PC is clean.
- Check mail rules and forwarding on the account; scammers sometimes set them.

## Reporting
- Personal fraud: FTC (US) at reportfraud.ftc.gov, Action Fraud (UK), or local police;
  bank first if money moved.
- Internal: incident record with timeline, tool used, data at risk.

## Follow-up
Short, kind coaching on how the scam worked (pop-up, cold call, fake refund) and how real
IT contacts them; see security-awareness-coaching-after-incidents.

## Verify
Device reimaged or confirmed clean, credentials reset and sessions revoked, no rogue mail
rules, bank notified where relevant, and the incident record is complete.
