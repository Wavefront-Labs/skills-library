---
id: computing-software.general-digital-literacy.email-clients.forwarding-mail-to-another-address
name: forwarding-mail-to-another-address
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, email-forwarding, auto-forward, consolidate-inboxes]
level: intro
status: docs-checked
description: "Automatically forward all or some email from Gmail or Outlook.com to another address, verify it, and use a rule or filter to forward only some mail."
sources:
  - https://support.google.com/mail/answer/10957
  - https://support.microsoft.com/en-us/outlook/turn-on-or-off-automatic-forwarding-in-outlook-com
  - https://support.microsoft.com/en-us/outlook/mail/use-rules-to-automatically-forward-messages
  - https://support.google.com/mail/answer/16604719
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Forward mail to another address

## Gmail (computer)
1. Settings > **See all settings** > **Forwarding and POP/IMAP** > **Add a forwarding address**, enter the address and proceed.
2. Gmail sends a verification link to that address; click it, then refresh Gmail settings.
3. Select **Forward a copy of incoming mail to** and choose what happens to Gmail's copy; Google recommends keeping it in the inbox. Archiving the copy is the other option listed. Save Changes.
- All new mail is forwarded except spam. To forward only some mail, turn off automatic forwarding and create a filter with **Forward it** (one filter per forwarding address).
- Turn off: Disable forwarding > Save Changes.

## Outlook.com
- Settings > **Mail** > **Forwarding** > **Enable forwarding**, enter the address, Save. Tick **Keep a copy of forwarded messages** if wanted. You may be asked to verify your identity or turn on two-step verification.
- Forwarded messages appear to come from your account, so replies go to your account, not the original sender. A rule with **Redirect to** makes the message appear to come from the original sender so replies go to them. Rules: Settings > Mail > Rules.
- Check Junk at the destination when testing.

## Alternatives
- Gmail is retiring "Check mail from other accounts" (POP fetching) and Gmailify: no new users after the first quarter of 2026; existing users keep it until January 2027. Alternatives are forwarding set up at the other provider, or adding the account in the Gmail mobile app (IMAP).
- Moving providers: forward for a while and tell contacts the new address.

## Gotchas
- Forwarding both ways between two accounts can loop and bounce.
- A forwarding notice you did not expect in Gmail means change your password and turn forwarding off.
- Work accounts may restrict forwarding; ask IT.

## Verify
- [ ] A test to the old address arrives at the new one, and the copy behaviour is as chosen.

## Checked
2026-10-27. Google Gmail Help "Automatically forward Gmail messages" and "Upcoming changes to Gmailify and POP"; Microsoft Support "Turn on or off automatic forwarding in Outlook.com" and "Use rules to automatically forward messages". Confirmed paths, options, dates and forward vs redirect behaviour. Removed iCloud and "delete Gmail's copy" claims, which the pages do not support, and the unconfirmed bounce text.
Method: documentation only; no commands were run.
