---
id: computing-software.collaboration-platform-administration.google-workspace-admin.gmail-spf-dkim-dmarc
name: gmail-spf-dkim-dmarc
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [gmail-spf-dkim-dmarc]
level: practitioner
status: draft
description: Authenticate outbound mail.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPF, DKIM and DMARC for Google Workspace
**Goal:** Authenticate outbound mail.

- SPF: `v=spf1 include:_spf.google.com ~all`, merging other senders.
- DKIM: Apps > Gmail > Authenticate email > Generate new record (2048-bit); add TXT at google._domainkey; Start authentication.
- DMARC: `_dmarc` TXT starting p=none with rua, then enforce.
- Check with the Admin Toolbox CheckMX.

## Gotchas
- Wait for DNS to propagate before 'Start authentication'.
- Other services need their own DKIM selectors.

## Self-check
Message headers show spf=pass, dkim=pass, dmarc=pass.
