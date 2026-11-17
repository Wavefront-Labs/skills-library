---
id: computing-software.messaging-and-integration.apache-camel.mail-component
name: mail-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, mail, imap, smtp, pop3]
level: practitioner
status: docs-checked
description: "Camel mail component: smtp, imap and pop3 schemes and ports, consumer defaults (unseen, peek, delay 60000), producer from and contentType, and header override safety flags."
sources:
  - https://camel.apache.org/components/next/mail-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mail:

Schemes: `smtp`, `pop3`, `imap`; secure variants `smtps`, `pop3s`, `imaps`. Ports: SMTP 25, SMTPS 465, POP3 110, POP3S 995, IMAP 143, IMAPS 993. Prefer IMAP; POP3 has limitations.

Consumer (defaults): `delete` false (sets SEEN instead of DELETED), `unseen` true, `disconnect` false, `closeFolder` true, `mapMailMessage` true (false = raw `jakarta.mail.Message` body), `peek` true (mail not marked SEEN until processed, so errors can roll back), `maxMessagesPerPoll` unlimited, `fetchSize` -1 (0 consumes none), `folderName` `INBOX`, `copyTo`/`moveTo` unset, `delay` 60000 ms, `initialDelay` 1000 ms.

Producer: `from` `camel@localhost`, `contentType` `text/plain` (use `text/html` for HTML). `useHeaderFrom`, `useHeaderRecipients`, `useHeaderSubject`, `useHeaderReplyTo` all false; only when true do the headers `From`, `To`/`Cc`/`Bcc`, `Subject`, `Reply-To` override the endpoint.

Other headers: `CamelMailCopyTo`, `CamelMailMoveTo`, `CamelMailDelete` (consumer overrides), `CamelMailMessageId` (set on producer output), `CamelMailAlternativeBody` (plain-text alternative for multipart/alternative).

Security: enable the header-override flags only for trusted sources, since untrusted input could redirect or forge mail.

Verify: an IMAP consumer with defaults picks up only unseen mail and leaves it marked SEEN after processing.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org mail-component page (URI formats, default ports table, consumer and producer option tables, message headers and body sections).
