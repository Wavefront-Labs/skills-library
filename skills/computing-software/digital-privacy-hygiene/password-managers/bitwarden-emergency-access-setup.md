---
id: computing-software.digital-privacy-hygiene.password-managers.bitwarden-emergency-access-setup
name: bitwarden-emergency-access-setup
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, bitwarden-emergency-access, emergency-access, digital-legacy]
level: practitioner
status: docs-checked
description: "Configure Bitwarden emergency access with a trusted contact: view vs takeover, wait time, and how to reject a request."
sources:
  - "https://bitwarden.com/help/emergency-access/"
  - "https://bitwarden.com/help/fingerprint-phrase/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bitwarden emergency access setup

**Goal:** someone you trust can reach your vault if you die or are incapacitated, and can't do it silently while
you're fine.

## Requirements
The grantor needs a premium account (members of paid organisations count). The trusted contact can hold a free or
premium account on the same Bitwarden server.

## Set up (grantor)
1. Web vault > Settings > Emergency access > add an emergency contact by email.
2. Choose the access level:
   - **View:** read access to the items in your individual vault.
   - **Takeover:** the contact creates a new master password, giving permanent read/write access to your vault.
3. Choose a **wait time**: how long the contact must wait after requesting, which is your window to reject.
4. The contact accepts the emailed invite (it expires after a few days, so tell them to act promptly); you then
   confirm them.

## Using it (grantee)
Request access from the emergency access page. If the grantor does not act, access is granted when the wait
time lapses; the grantor can also approve early.

## Rejecting
If you get a request you didn't expect, open Emergency access and **Reject**. Rejecting does not remove the
contact, so also remove them if you no longer trust them, and talk to the person: their account may be
compromised.

## Choosing settings
- Match the level to the role: View for someone who only needs to read items, Takeover for someone who must run
  your accounts.
- Two contacts is better than one.

## Gotchas
- Takeover replaces your master password and removes your existing two-step login methods.
- Keep your account email reachable or you won't see a request.

## Checked
2026-11-01. Confirmed against bitwarden.com/help/emergency-access/: premium requirement incl. paid
organisations, contact account type, View vs Takeover meaning, grantor-specified wait time, automatic grant at
lapse, manual approval, reject leaves the contact in place, takeover replaces the master password and removes
two-step methods. Removed as unstated: the 1-90 day range, the fingerprint-phrase comparison step (the fingerprint
page does not tie it to emergency access), the typical-settings advice and the organisation-items note.
Method: documentation only; no commands were run.
