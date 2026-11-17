---
id: computing-software.digital-privacy-hygiene.phishing-awareness.cleaning-up-after-a-remote-access-scam
name: cleaning-up-after-a-remote-access-scam
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, remote-access-scam-cleanup, phishing-incident-response, tech-support-scam, anydesk, teamviewer, quick-assist, malware-removal, bank-fraud]
level: practitioner
status: draft
description: "After a scammer had remote control (AnyDesk, TeamViewer, Quick Assist): disconnect, call banks, remove tools and persistence, rebuild if unsure, and rotate everything typed since."
sources:
  - "https://consumer.ftc.gov/articles/how-spot-avoid-and-report-tech-support-scams"
  - "https://www.microsoft.com/en-us/security/blog/2024/05/15/threat-actors-misusing-quick-assist-in-social-engineering-attacks-leading-to-ransomware/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cleaning up after a remote-access scam

**Goal:** a "support agent" or "bank" got remote control of a computer or phone. Assume
they looked at everything, may have installed more tools, and may have logged into banking.

## Immediately
1. **Disconnect** the device from the internet (Wi-Fi off / cable out).
2. From a different phone, **call your bank(s)** fraud lines: tell them remote access
   occurred, check for transfers or new payees, freeze online banking if needed.
3. Note what happened (time, tool used, what they asked you to do, phone numbers).

## Remove access
- Uninstall remote tools you didn't use before: AnyDesk, TeamViewer, UltraViewer,
  ScreenConnect/ConnectWise, LogMeIn, Supremo, RustDesk; Windows **Quick Assist** is built
  in (they used it, nothing to uninstall, but check other tools installed during the session).
- Check Settings > Apps sorted by **install date** for anything from that day.
- Check startup items, scheduled tasks, new user accounts, browser extensions.
- On phones: remove the screen-sharing app; check accessibility services and device admin.
- If any doubt (they ran commands, installed unknown software): **back up documents and
  reinstall** (see
  `computing-software.digital-privacy-hygiene.device-hardening.cleaning-an-infected-computer`).

## Rotate
From a clean device, change passwords for email, banking, and anything typed or open during
the session; revoke sessions; consider a credit freeze if they saw ID documents.

## Report
FTC (reportfraud.ftc.gov), IC3, and the bank.

## Verify
- [ ] No remote tools installed; bank confirmed no unauthorised transfers.
- [ ] Credentials rotated from a clean device.
