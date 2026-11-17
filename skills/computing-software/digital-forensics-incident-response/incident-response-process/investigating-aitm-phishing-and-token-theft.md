---
id: computing-software.digital-forensics-incident-response.incident-response-process.investigating-aitm-phishing-and-token-theft
name: investigating-aitm-phishing-and-token-theft
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [aitm-phishing, business-email-compromise, bec, entra-id, session-revocation, dfir]
level: advanced
status: docs-checked
description: "Investigate adversary-in-the-middle phishing that steals session cookies past MFA: session-ID correlation, follow-on BEC activity, revocation and phish-resistant MFA."
sources: ["https://www.microsoft.com/en-us/security/blog/2022/07/12/from-cookie-theft-to-bec-attackers-use-aitm-phishing-sites-as-entry-point-to-further-financial-fraud/", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins", "https://learn.microsoft.com/en-us/graph/api/user-revokesigninsessions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Investigating AiTM phishing and token theft

**Goal:** in adversary-in-the-middle (AiTM) phishing the attacker runs a proxy between the
user and the real site, so they capture the password and the session cookie. Microsoft
stresses this is not a vulnerability in MFA: with the cookie the attacker is authenticated
on the user's behalf regardless of sign-in method, so a password reset alone does not
remove them. Open-source kits named in Microsoft's analysis: Evilginx2, Modlishka, Muraena.

## Signals (from Microsoft's July 2022 analysis)
- The session ID in the attacker's later sign-ins is identical to the one from the
  authentication against the phishing site. Microsoft's hunting query looks for session IDs
  first seen on the OfficeHome application and later used on other applications from a
  different country.
- Stolen cookies can carry an MFA claim, so a sign-in showing MFA satisfied does not prove
  the real user.
- Entra ID Protection alerts Microsoft lists for this campaign: Anomalous Token, Unfamiliar
  sign-in properties, Unfamiliar sign-in properties for session cookies, Anonymous IP
  address. Defender for Cloud Apps: Suspicious inbox manipulation rule, Impossible travel,
  Activity from infrequent country.
- Entra sign-in logs record interactive user, non-interactive user, service principal and
  managed identity sign-ins in separate tabs, and entries cannot be changed or deleted.
  Reading them needs at least the Reports Reader role (Entra admin center > Monitoring &
  health > Sign-in logs).

## Follow-on activity to look for
In the documented campaign the attacker used the cookie in Outlook on the web within as
little as five minutes, then read finance-related mail and attachments every few hours,
deleted the original phishing email, created an Inbox rule to move replies from the fraud
target's domain to Archive and mark them read, replied in payment threads, deleted their
replies from Sent Items and Deleted Items, and updated the rule for each new target. Hunt
for suspicious Inbox rules, unusual mail-item access from untrusted IPs or devices, and
sign-ins with suspicious location, ISP, user agent or anonymiser use.

## Scope
Find the phishing message and every recipient who may have signed in to the lure site
(the observed lure was an HTML attachment redirecting through a redirector to the phishing
page), then search sign-in logs for the attacker's session IDs and sign-in properties.

## Contain
- Revoke sessions: the Microsoft Graph `revokeSignInSessions` API (PowerShell
  `Revoke-MgUserSignInSession -UserId <UPN or id>`) invalidates the user's refresh tokens
  and browser session cookies by resetting `signInSessionsValidFromDateTime`. Permission
  `User.RevokeSessions.All`. It can take a few minutes to take effect and does not revoke
  sessions for external users.
- Then reset the password and remove the attacker's Inbox rules. Cleanup beyond that
  (extra MFA methods, consents) is standard account-compromise practice; the cited pages
  do not detail it.
- Prevention per Microsoft: phish-resistant MFA (FIDO v2.0 and certificate-based
  authentication) and conditional access, such as compliant device or trusted IP
  requirements, which are evaluated each time a stolen cookie is used. Continuous Access
  Evaluation revokes access in real time when conditions change, such as a move to an
  untrusted location.

## Verify
After revocation, confirm no further sign-ins from the attacker's infrastructure and no new
mailbox changes.

## Checked
Dated 2026-11-08. Confirmed against Microsoft Threat Intelligence, "From cookie theft to BEC" (AiTM mechanics, kit names, session ID correlation, post-breach BEC steps, alerts, defences), the Entra sign-in logs concept page (log types, immutability, Reports Reader role, portal path) and the Graph revokeSignInSessions page (effect, delay, permission, external users, PowerShell cmdlet). Removed as unstated: Tycoon 2FA and EvilProxy, the SigninLogs KQL and its column names, "Attacker in the Middle" risk detection name, UrlClickEvents, audit operation names, user-agent and ASN heuristics, and the Set-Mailbox forwarding command.
Method: docs-only read of cited pages, 2026-11-08
