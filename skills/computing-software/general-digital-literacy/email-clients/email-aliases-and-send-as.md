---
id: computing-software.general-digital-literacy.email-clients.email-aliases-and-send-as
name: email-aliases-and-send-as
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-account-setup, email-alias, send-as, plus-addressing, outlook-alias, hide-my-email]
level: practitioner
status: docs-checked
description: "Send mail from another address in Gmail with Send mail as, use plus-addressing for filtering, and know the January 2027 end of third-party send-as."
sources:
  - https://support.google.com/mail/answer/22370
  - https://support.google.com/mail/answer/16604719
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Aliases and send-as addresses (Gmail)

## Plus addressing
Gmail delivers `yourname+shopping@gmail.com` to `yourname@gmail.com`. Pick a tag per category (work, news, shopping) and create filters to label, star, forward or archive by the address. Gmail's help also lists "Dots don't matter in Gmail addresses" as a separate article.

## Send mail as (computer)
1. Settings > **See all settings** > **Accounts and import** (or Accounts) > **Send mail as** > **Add another email address**.
2. Enter your name and the address, then Send verification. For school or work accounts, enter the SMTP server, username and password if asked (for example smtp.gmail.com or your organisation's server).
3. Open the confirmation message sent to that address (check Spam for send-as-noreply@google.com) and click the link.
4. In a message, click the **From** line and choose the address. You can have up to 99 addresses.
- To always send from the other address, use **Make default**. To send replies to a different address, use **Edit info** > **Specify a different "reply to" address**; changing only From leaves replies going to your Gmail address.
- Connection errors: choose a port and security type your other provider supports (SSL with 465, or TLS with 25 or 587).

## Important change
Starting January 2027 Gmail will no longer support Send as for third-party addresses such as @yahoo.com or @outlook.com. It does not affect Google Workspace aliases or other Gmail addresses you own.

## Gotchas
- Recipients on Outlook or other services may see "from yourname@gmail.com on behalf of other@domain", and may see your Gmail address if you set an out-of-office reply, use an auto-reply filter or your mailbox is full.
- To re-verify an address after a bounce, delete it from Send mail as and add it again.

## Verify
- [ ] Send a test from the alias to another account: From shows the alias and the reply arrives back.

## Checked
2026-10-27. Google Gmail Help "Send emails from a different address or alias" and "Learn about upcoming changes to Gmailify and POP". Confirmed menu paths, the 99-address limit, the January 2027 third-party end date, reply-to behaviour and plus addressing. Removed unconfirmed Outlook.com alias, iCloud alias, Hide My Email, custom-domain and plus-addressing-elsewhere claims.
Method: documentation only; no commands were run.
