---
id: computing-software.email-administration.mailcow.mailcow-sender-permissions-and-acl-model
name: mailcow-sender-permissions-and-acl-model
category: computing-software
field: email-administration
product: mailcow
tags: [send-as, alias-domains, catch-all-alias, delegation, domain-admin-acl, sender-check]
level: advanced
status: docs-checked
description: "Understand which addresses a mailcow mailbox may send as and receive for, and how domain-administrator and mailbox ACLs combine."
sources: ["https://docs.mailcow.email/models/model-sender_rcv/", "https://docs.mailcow.email/models/model-acl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow sender/receiver and ACL model

A new mailbox may send from and receive for only its own address. `me@example.org` is known as `me@example.org` only. A mailbox cannot be created in an alias domain.

Adding the alias domain `alias.com` to `example.org` makes `me@example.org` also known as, and allowed to send as, `me@alias.com`. Adding a mailbox alias `alias@example.org` adds that address. Alias addresses do not multiply across alias domains: `me@example.org` is not `alias@alias.com` unless that alias is created.

A catch-all alias `@example.org` receives mail for the domain and, via an alias domain, mail sent to `alias.com`, but it does not add send-as options; the mailbox stays known only as its own address.

Administrators and domain administrators can delegate: allow specific mailbox users to send as other mailbox users, or switch the sender check off for a domain. In SOGo, mailbox users can pick their own address and their aliases (including those via alias domains) as "mail from"; sending as another mailbox user also needs delegation in SOGo plus the administrator grant above.

ACL rules for accounts: for modules that both domain admins and mailbox users may hold (such as sync jobs), a domain administrator who logs in as a mailbox user inherits the domain administrator's permission, whether it is more or less than the mailbox's own. Permissions that do not exist in a domain administrator's ACL (for example time-limited aliases or TLS policy) are granted automatically in that session.

## Checked

2026-11-09. Confirmed against the mailcow Sender and receiver model and ACL pages. Reworded the SOGo sentence to match the page.

Method: docs-checked 2026-11-09 against docs.mailcow.email/models/model-sender_rcv/ and docs.mailcow.email/models/model-acl/ (whole pages).
