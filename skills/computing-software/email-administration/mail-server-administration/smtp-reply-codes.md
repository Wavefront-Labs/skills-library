---
id: computing-software.email-administration.mail-server-administration.smtp-reply-codes
name: smtp-reply-codes
category: computing-software
field: email-administration
product: mail-server-administration
tags: [smtp-reply-codes, enhanced-status-codes, 4xx, 5xx]
level: intro
status: docs-checked
description: "Read SMTP reply codes and enhanced status codes: 2xx success, 4xx temporary, 5xx permanent, and what to do for each."
sources:
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.rfc-editor.org/rfc/rfc3463
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Smtp reply codes

**Goal:** decide quickly if a failure is retried or final (RFC 5321 section 4.2; RFC 3463 for x.y.z codes).
## Reference
- First digit: 2yz positive completion; 3yz positive intermediate (more input needed); 4yz transient negative, where the SMTP client SHOULD try again; 5yz permanent negative, where the client SHOULD NOT repeat the exact request.
- 250 requested mail action okay; 354 start mail input after DATA; 421 service not available, closing the transmission channel.
- 450 mailbox unavailable; 451 error in processing (local error); 452 insufficient system storage. All are 4yz.
- 550 mailbox unavailable; 551 user not local; 552 exceeded storage allocation; 553 mailbox name not allowed; 554 transaction failed. All are 5yz.
- Enhanced codes (RFC 3463): the first digit 4 is persistent transient failure and 5 is permanent failure; `X.1.1` bad destination mailbox address, `X.2.2` mailbox full, `X.7.1` delivery not authorized, message refused.
## Failure modes
- Treating every 4yz as final: the client is expected to retry these.
- Repeating the identical command after a 5yz instead of fixing the cause.
## Verify
- Look the code up in RFC 5321 and RFC 3463 before acting, and compare the mail log line for a deferred message with one for a bounced message.

## Checked

2026-11-09. Confirmed on RFC 5321 section 4.2: the four reply classes and their retry wording, and the code list (250, 354, 421, 450, 451, 452, 550, 551, 552, 553, 554). Confirmed on RFC 3463: 4.X.X persistent transient failure, 5.X.X permanent failure, and X.1.1, X.2.2, X.7.1 meanings. Removed: the claims about greylisting and rate limits using specific codes, the queue bloat claim, the swaks mention, the sample Postfix log format, and the boilerplate notes.

Method: documentation only; no commands were run.
