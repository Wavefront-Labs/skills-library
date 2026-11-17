---
id: computing-software.general-digital-literacy.digital-communication.managing-contacts-and-spam-calls
name: managing-contacts-and-spam-calls
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, contacts, spam-calls, robocalls, smishing, caller-id, block-list, silence-unknown-callers, do-not-call-registry, scam-texts, duplicate-contacts, vcard, contact-sync]
level: intro
status: docs-checked
description: "Keep a contacts list clean across devices and apps, and cut down robocalls, spam texts and smishing without missing calls that matter."
sources:
  - https://support.apple.com/guide/iphone/merge-or-hide-duplicate-contacts-iph2ab28320d/ios
  - https://support.google.com/contacts/answer/7078226
  - https://support.google.com/messages/answer/9061432
  - https://support.apple.com/en-us/111106
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing contacts and spam calls - a clean address book and a quiet phone

**Goal:** stop a contacts list from fragmenting into duplicates, and cut spam calls and texts down without silencing someone who needs to reach you.

## 1. Where contacts live
- Contacts are synced from accounts (a Google account on Android, iCloud on iPhone) and apps usually read the device's list. Edit the source, not an app's copy.

## 2. Fixing duplicates
- **iPhone:** open Contacts; below **My Card**, tap **Duplicates Found** (older versions say View Duplicates) to review or **Merge All**. Linking cards keeps them separate but shows them as one.
- **Android (Google Contacts):** use **Merge duplicates** (under "Fix & manage" or "Merge and fix", depending on version). Contacts saved in different Google Accounts cannot be merged.
- If a name appears twice with different numbers, merge rather than deleting one, so you keep both numbers.
- Exporting and importing a vCard (.vcf) file moves contacts between services.

## 3. Silencing unknown callers
- **iPhone:** Settings > Apps > Phone > **Screen Unknown Callers**, option **Silence** (sent to voicemail and shown in Recents; Never and Ask Reason for Calling are the other options). A genuine call from a new number is silenced too, so check voicemail and Recents.
- Your carrier may offer a spam-filtering service; check its app or settings.

## 4. Spam and scam texts
- Never tap a link in an unexpected text about a "missed delivery", "unpaid toll" or "account suspended"; go to the real organisation's app or type its known address yourself.
- **Google Messages:** touch and hold the conversation, then Block > Report spam > OK, or open the conversation > Details > **Block & report spam**. Reporting also blocks the sender and moves the thread to Spam & blocked, and sends the number and recent messages to Google (and possibly to your carrier). You can block without reporting.
- A link plus urgency from an unfamiliar number is the pattern, whichever brand it claims to be.

## Verify
- [ ] Contacts are edited at the synced source, not inside one app only.
- [ ] A duplicate-merge check has been run.
- [ ] You know your phone's unknown-caller setting.
- [ ] A suspicious text was reported or blocked rather than tapped.

## Checked
Date: 2026-10-27. Documentation: Apple Support (merge duplicate contacts; manage unknown callers), Google Contacts Help (merge duplicates), Google Messages Help (report spam), all via search results. Confirmed: iPhone and Android merge paths, Silence setting path and options, Google Messages block and report flow. Removed unconfirmed claims (iCloud and Google sync toggles, Android call-blocking paths, iPhone block-caller steps, Do Not Call Registry statements, carrier label names, Android Caller ID setting).
Method: documentation only; no commands were run.
