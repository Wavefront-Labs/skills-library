---
id: computing-software.systems-network-administration.audiobookshelf.send-to-ereader-email
name: send-to-ereader-email
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [ebooks, e-reader, smtp, kindle, email, app-password]
level: practitioner
status: docs-checked
description: "Configure Audiobookshelf SMTP email and e-reader devices so users can send a primary e-book to a Kindle or other reader."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/4.ebooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An admin first configures the email provider. You need the SMTP hostname, port, username and password. Common ports are 587, 465 and 25; with 587 or 25 you will likely need to turn the **Secure** toggle off. The From Address can be plain `test@example.com` or `Name <test@example.com>`. Save the settings.

Some providers require an app password; Gmail required one rather than your normal password. The page warns that major providers are sunsetting app password login, and suggests a dedicated SMTP delivery service as another option.

Add each e-reader with a **Name** (shown in Audiobookshelf) and the destination **E-mail**. Choose who can use it: only admins, all users excluding guests, all users including guests, or specific users.

Users can then send the **primary** e-book to any e-reader they can access.

Kindle: the email Audiobookshelf sends from must be authorized in Amazon's Send to Kindle approved-sender list.

## Checked

Method: docs-checked 2026-11-09 against the E-books page (Send to e-reader section) of the Audiobookshelf docs repo, read in full from raw markdown.
