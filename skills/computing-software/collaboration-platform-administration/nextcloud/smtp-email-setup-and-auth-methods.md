---
id: computing-software.collaboration-platform-administration.nextcloud.smtp-email-setup-and-auth-methods
name: smtp-email-setup-and-auth-methods
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [email, smtp, starttls, sendmail, mail-provider]
level: practitioner
status: draft
description: "Connect Nextcloud to an existing mail server with the Basic settings wizard, know the values required, the Nextcloud 26 mailer changes, and the send test."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/email_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: send password resets, share notices and activity mail.

Nextcloud has no mail server of its own; it connects to an existing one, local or remote. As admin open your avatar, *Settings*, then *Administration -> Basic settings*. The wizard writes the values into `config/config.php`, so you can use either.

Connection types: SMTP, qmail or Sendmail. Use SMTP for a remote server and Sendmail when the mail server is on the same machine. Any drop-in Sendmail replacement such as Postfix, Exim or Courier works, as each includes a `sendmail` binary. SMTP is usually best because it gives you the most control.

Collect from the mail administrator:
- encryption type, None/STARTTLS or SSL
- the From address
- whether authentication is required
- server name or IP and the SMTP port
- login credentials if needed

The mailer tries authentication methods in order: CramMd5, Login, Plain, XOAuth2.

Changes in Nextcloud 26 (new mailer library):
- STARTTLS cannot be enforced. It is used automatically when the server supports it, so choose None/STARTTLS.
- NTLM for Microsoft Exchange is not supported.
- Outlook and Exchange have dropped Basic authentication, so you can no longer use them as your default email handler that way.

Mail providers (added in version 30): an app such as Nextcloud Mail 4.1 or later can send calendar invitations through a user's own configured account.

Check: click Send Email. A message arrives at the address on your Personal page, saying the settings seem to be correct.
