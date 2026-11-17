---
id: computing-software.digital-privacy-hygiene.vpn-tools.imessage-contact-key-verification
name: imessage-contact-key-verification
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, contact-key-verification, imessage, key-verification, end-to-end-encryption, ios, apple-account, high-risk-users]
level: practitioner
status: docs-checked
description: "Turn on iMessage Contact Key Verification, compare or publish verification codes, and read the validation-error alert in a conversation."
sources:
  - "https://support.apple.com/en-us/118246"
  - "https://security.apple.com/blog/imessage-contact-key-verification/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iMessage Contact Key Verification

**Goal:** detect when the key directory that maps a contact's address to device keys returns something wrong, which
would let an attacker add a device to eavesdrop on an iMessage conversation. Apple describes the directory service
as a single point of failure that this feature guards against.

## Requirements
From Apple's support article: iOS 17.2, iPadOS 17.2, watchOS 10.2, macOS 14.2 or visionOS 1.1 or later on all
devices signed in to iMessage with your Apple Account; the same Apple Account for iCloud and iMessage; iCloud
Keychain on for all devices; two-factor authentication on; a passcode or password on all devices. Managed Apple
Accounts are not supported. If a device cannot update, sign out of iMessage on it before turning the feature on.

## Turn on
Settings (System Settings on Mac), your name, Contact Key Verification, turn on Verification in iMessage, tap
Continue. It turns on for all devices signed in to your Apple Account.

## Verify a contact manually
The person must be saved in Contacts.
- On-device comparison: both of you need cellular or Wi-Fi and open Verify Contact at the same time (Messages,
  the thread, contact name for Conversation Details, Verify Contact). Compare the code in person, over FaceTime or
  another secure call. If it matches, tap Mark as Verified; if not, you might not be messaging the person you
  intend, so consider pausing until you are sure.
- Public Verification Code: a code that contains no private information and can be posted publicly. Show yours in
  Settings, your name, Contact Key Verification, Show Public Verification Code, then Copy. To verify someone else,
  paste their code into the verification code field of their contact card (Edit, Edit Contact Info; add it via
  More Fields if the field is hidden). A checkmark appears if it matches what is stored on Apple servers and is
  verified.
- Conversation Details shows the status: Turn On Contact Key Verification, Verification Off for that contact,
  Verify Contact, a checkmark once verified, or an alert on a validation error.

## Alerts
If your device detects a validation error and both you and the contact have the feature on, iMessage tells you in
the conversation transcript (and shows the error in the Contact Key Verification pane in Apple Account settings).
Apple has a separate support article for what to do on an alert; contact the person through another channel
before continuing a sensitive conversation (this last step is a precaution, not from the cited pages).

## Who needs it
Apple's blog says it is designed for people facing targeted threats to their digital security, and adds hardening in
the Messages app when enabled.

## Verify
- [ ] Contact Key Verification on; key contacts show a checkmark.

## Checked
Method: docs-checked 2026-11-09 against Apple Support article 118246 (published May 2026; requirements, turn-on, verification and status sections read in full) and the Apple Security Research blog post on iMessage Contact Key Verification (validation-error, directory-service and audience statements found by targeted search of the downloaded page). Dropped as unconfirmed: the SMS/RCS fallback gotcha and the "Send as Text Message" advice, and the exact wording of the unknown-device error.
