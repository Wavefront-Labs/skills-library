---
id: computing-software.general-digital-literacy.email-clients.checking-for-malicious-forwarding-rules
name: checking-for-malicious-forwarding-rules
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, forwarding-rules, inbox-rules, connected-apps, oauth-apps]
level: practitioner
status: docs-checked
description: "Audit Gmail and Outlook.com for unexpected auto-forwarding, forwarding filters and rules, and unknown delegates, and know what the forwarding notices mean."
sources:
  - https://support.google.com/mail/answer/10957
  - https://support.google.com/mail/answer/138350
  - https://support.microsoft.com/en-us/outlook/turn-on-or-off-automatic-forwarding-in-outlook-com
  - https://support.microsoft.com/en-us/outlook/mail/use-rules-to-automatically-forward-messages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Check for malicious forwarding rules and delegates

Run this after any phishing click, password leak, or suspicious activity.

## Gmail (computer)
- Settings > **See all settings** > **Forwarding and POP/IMAP**: forwarding should be off or point to an address you own. Click **Disable forwarding** and Save Changes to turn it off.
- Review **Filters and Blocked Addresses**: a filter can use **Forward it** to send selected mail elsewhere. Delete filters you did not create.
- Gmail shows a notice in the inbox for the first week after forwarding or a forwarding filter is created ("You are forwarding your email to ..."). If you see one and never set it up, change your password immediately and turn forwarding off.
- Settings > **Accounts and Import** > **Grant access to your account**: remove delegates you do not recognise (Delete next to the account). A delegate can read, send and delete mail. On work or school accounts an admin can also add delegates, so ask the admin; change your password if you see one you did not add.

## Outlook.com
- Settings > **Mail** > **Forwarding**: if forwarding is enabled and you did not set it up, turn it off. You may be asked to verify your identity again.
- Settings > **Mail** > **Rules**: a rule can use **Forward to** (appears to come from you) or **Redirect to** (appears to come from the original sender). Delete rules you did not create.
- Work or school accounts: your administrator can see and block external forwarding; ask IT.

## Gotchas
- Deleting a rule does not recall mail already forwarded; assume it was read.

## Verify
- [ ] No forwarding address, filter or rule you do not recognise, and no unexpected delegates.

## Checked
2026-10-27. Google Help "Automatically forward Gmail messages" and "Delegate and collaborate on email"; Microsoft Support "Turn on or off automatic forwarding in Outlook.com" and "Use rules to automatically forward messages". Confirmed paths, the first-week forwarding notice, forward vs redirect behaviour and delegate capabilities. Removed unconfirmed third-party-app, classic Outlook, iCloud and rule-folder claims.
Method: documentation only; no commands were run.
